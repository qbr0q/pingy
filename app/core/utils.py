from pydantic import BaseModel, ConfigDict


class DataTransfer(BaseModel):
    model_config = ConfigDict(extra="allow")
