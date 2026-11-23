from pydantic import BaseModel, Field

class Status(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str

class Message(BaseModel):
    value_from: str = Field(alias="from")
    type: str
    text: dict

class Value(BaseModel):
    messages: list[Message] | None = None
    statuses: list[Status] | None = None

class Changes(BaseModel):
    field: str
    value: Value

class Entry(BaseModel):
    changes: list[Changes]

class WebhookPayload(BaseModel):
    object: str
    entry: list[Entry]

