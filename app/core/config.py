from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PrivateConfig(BaseModel):
    bot_token: str


class DBConfig(BaseModel):
    user: str
    password: str
    host: str
    port: str
    schema: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.schema}"


class RedisConfig(BaseModel):
    host: str
    port: str
    schema: str

    @property
    def url(self):
        return f"redis://{self.host}:{self.port}/{self.schema}"


class ProxyConfig(BaseModel):
    ip: str
    port: int
    login: str
    password: str

    @property
    def url(self):
        return f"socks5://{self.login}:{self.password}@{self.ip}:{self.port}"


class Config(BaseSettings):
    private: PrivateConfig
    db: DBConfig
    redis: RedisConfig
    proxy: ProxyConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__"
    )


config = Config()
