from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings


class PathSettings(BaseModel):
    locales: str


class Settings(YamlBaseSettings):
    paths: PathSettings
    use_proxy: bool

    model_config = SettingsConfigDict(
        yaml_file="settings.yml"
    )


settings = Settings()
