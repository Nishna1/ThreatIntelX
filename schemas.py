from pydantic import BaseModel

class IOCBase(BaseModel):
    type: str
    value: str
    source: str
    severity: str

class IOC(IOCBase):
    id: int

    class Config:
        from_attributes = True
