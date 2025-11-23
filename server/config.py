from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TRELLO_API_KEY: str
    TRELLO_TOKEN: str
    MCP_SERVER_NAME: str = "Trello MCP Server"
    MCP_SERVER_HOST: str = "127.0.0.1"
    MCP_SERVER_PORT: int = 8952
    USE_CLAUDE_APP: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
