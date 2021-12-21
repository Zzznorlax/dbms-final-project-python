from pydantic import BaseModel


class GeneralAPIResp(BaseModel):
    status: int
    message: str
