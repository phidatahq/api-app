from phidata.app.fastapi import FastApiServer
from phidata.aws.config import AwsConfig
from phidata.aws.resource.group import AwsResourceGroup, DbInstance, DbSubnetGroup
from phidata.docker.config import DockerConfig, DockerImage

from workspace.settings import ws_settings

#
# -*- Resources for the Production Environment
#
# Skip resource creation when running `phi ws up`
skip_create: bool = False
# Skip resource  deletion when running `phi ws down`
skip_delete: bool = False

# -*- Production Api Image
prd_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}",
    tag=ws_settings.prd_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    platform="linux/amd64",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
    use_cache=ws_settings.use_cache,
)

# -*- RDS Database Subnet Group
prd_db_subnet_group = DbSubnetGroup(
    name=f"{ws_settings.prd_key}-db-sg",
    enabled=ws_settings.prd_db_enabled,
    subnet_ids=ws_settings.subnet_ids,
    skip_create=skip_create,
    skip_delete=skip_delete,
)

# -*- RDS Database Instance
db_engine = "mysql"
prd_db = DbInstance(
    name=f"{ws_settings.prd_key}-db",
    enabled=ws_settings.prd_db_enabled,
    db_name="prd",
    engine=db_engine,
    engine_version="8.0.32",
    allocated_storage=64,
    # NOTE: For production, use a larger instance type.
    # Last checked price: $0.0320 per hour = ~$25 per month
    db_instance_class="db.t4g.small",
    availability_zone=ws_settings.aws_az1,
    db_subnet_group=prd_db_subnet_group,
    # enable_performance_insights=True,
    # vpc_security_group_ids=ws_settings.security_groups,
    # Read database username and password from secrets file
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/prd_mysql_secrets.yml"
    ),
    skip_create=skip_create,
    skip_delete=skip_delete,
)

# -*- FastApiServer running on ECS
launch_type = "FARGATE"
prd_fastapi = FastApiServer(
    name=ws_settings.prd_key,
    enabled=ws_settings.prd_api_enabled,
    image=prd_image,
    command=["api", "start"],
    ecs_task_cpu="512",
    ecs_task_memory="1024",
    aws_subnets=ws_settings.subnet_ids,
    # aws_security_groups=ws_settings.security_groups,
    env={
        "RUNTIME_ENV": "prd",
        # Database configuration
        "DB_HOST": "",
        "DB_PORT": "3306",
        "DB_USER": prd_db.get_master_username(),
        "DB_PASS": prd_db.get_master_user_password(),
        "DB_SCHEMA": prd_db.get_db_name(),
        # "UPGRADE_DB": True,
        # Wait for database to be available before starting the server
        "WAIT_FOR_DB": True,
    },
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/api_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/api_secrets.yml"),
)

# -*- DockerConfig defining the prd resources
prd_docker_config = DockerConfig(
    env=ws_settings.prd_env,
    network=ws_settings.ws_name,
    images=[prd_image],
)

# -*- AwsConfig defining the prd resources
prd_aws_config = AwsConfig(
    env=ws_settings.prd_env,
    apps=[prd_fastapi],
    resources=AwsResourceGroup(
        db_subnet_groups=[prd_db_subnet_group],
        db_instances=[prd_db],
    ),
)
