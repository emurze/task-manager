from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        populate_by_name=True,
    )
