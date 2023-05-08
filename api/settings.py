from typing import List, Optional

from pydantic import BaseSettings, validator

from utils.log import logger


class ApiSettings(BaseSettings):
    """Api settings that can be derived using environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # Api title and version
    title: str = "Api"
    version: str = "1.0"

    # Runtime env derived using the `runtime_env` environment variable.
    # Valid values are "dev", "stg", "prd"
    runtime_env: str = "dev"

    # Set to False to disable docs server at /docs and /redoc
    docs_enabled: bool = True

    # Host and port to run the api server on.
    host: str = "0.0.0.0"
    port: int = 9090
    # Create tables on startup
    create_tables: bool = False
    # Upgrade database on startup using alembic
    upgrade_db: bool = False

    # Database configuration
    db_host: Optional[str]
    db_port: Optional[str]
    db_user: Optional[str]
    db_pass: Optional[str]
    db_schema: Optional[str]
    db_driver: str = "mysql+mysqlconnector"

    # Cors origin list to allow requests from.
    cors_origin_list: List[str] = [
        "http://localhost",
        "http://localhost:3000",  # React dev server
        "http://localhost:9095",  # Streamlit dev server
    ]

    def get_db_uri(self) -> str:
        uri = "{}://{}{}@{}:{}/{}".format(
            self.db_driver,
            self.db_user,
            f":{self.db_pass}" if self.db_pass else "",
            self.db_host,
            self.db_port,
            self.db_schema,
        )
        if "None" in uri:
            logger.warning("No database provided, using sqlite")
            return "sqlite:///./sqlite.db"
        return uri

    @validator("runtime_env")
    def validate_runtime_env(cls, runtime_env):
        """Validate runtime_env."""

        valid_runtime_envs = ["dev", "stg", "prd"]
        if runtime_env not in valid_runtime_envs:
            raise ValueError(f"Invalid runtime_env: {runtime_env}")

        return runtime_env

    @validator("docs_enabled")
    def validate_docs_enabled(cls, docs_enabled, values):
        """Disable docs server in production."""

        runtime_env = values.get("runtime_env")
        if runtime_env == "prd":
            return False

        return docs_enabled


# Create ApiSettings object
api_settings = ApiSettings()
