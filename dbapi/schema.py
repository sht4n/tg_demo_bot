from pydantic import BaseModel, ConfigDict


class SForm(BaseModel):
    user_id: str
    lat: float
    long: float
    goal: str
    city: str
    gender: str
    preference: str
    name: str
    age: int
    description: str
    first_photo_id: str
    second_photo_id: str | None
    third_photo_id: str | None

class SFormId(BaseModel):
    id: int

class SFormUserId(BaseModel):
    user_id: str

class SFormStatus(BaseModel):
    is_existed: bool

class SFeed(BaseModel):
    feed: list[SForm] | None