from phidata.app.mysql import MySQLDb
from phidata.app.fastapi import FastApiServer
from phidata.docker.config import DockerConfig
from phidata.docker.resource.image import DockerImage

from workspace.settings import ws_settings

#
# -*- Resources for the Development Environment
#

# -*- Development API Image
dev_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}",
    tag=ws_settings.dev_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    # platform="linux/amd64",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
    use_cache=ws_settings.use_cache,
)

# -*- MySQL database
dev_db = MySQLDb(
    name=f"{ws_settings.dev_key}-db",
    enabled=ws_settings.dev_db_enabled,
    mysql_database="dev",
    mysql_root_password=ws_settings.ws_name,
    # Connect to this db on port 3306
    container_host_port=3306,
)

# -*- FastApiServer running on port 9090
dev_fastapi = FastApiServer(
    name=ws_settings.dev_key,
    enabled=ws_settings.dev_api_enabled,
    image=dev_image,
    command="api start -r",
    env={
        "RUNTIME_ENV": "dev",
        # Database configuration
        "DB_HOST": dev_db.get_db_host_docker(),
        "DB_PORT": dev_db.get_db_port_docker(),
        "DB_USER": dev_db.get_db_user(),
        "DB_PASS": dev_db.get_db_password(),
        "DB_SCHEMA": dev_db.get_db_schema(),
        # Upgrade database on startup
        # "UPGRADE_DB": True,
        # Wait for database to be available before starting the server
        # "WAIT_FOR_DB": True,
    },
    mount_workspace=True,
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/api_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/api_secrets.yml"),
)

# -*- DockerConfig defining the dev resources
dev_docker_config = DockerConfig(
    env=ws_settings.dev_env,
    network=ws_settings.ws_name,
    apps=[dev_db, dev_fastapi],
)
