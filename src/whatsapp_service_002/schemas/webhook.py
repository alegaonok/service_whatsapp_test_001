from pydantic import BaseModel, Field

class Text(BaseModel):
    body: str

class Status(BaseModel):
    id: str
    status: str
    timestamp: str | None = None
    recipient_id: str | None = None

class Message(BaseModel):
    value_from: str = Field(alias="from")
    type: str
    text: Text

class Value(BaseModel):
    messages: list[Message] | None = None
    statuses: list[Status] | None = None

class Changes(BaseModel):
    field: str
    value: Value

class Entry(BaseModel):
    changes: list[Changes] = Field(min_length=1)

class WebhookPayload(BaseModel):
    object: str
    entry: list[Entry] = Field(min_length=1)

