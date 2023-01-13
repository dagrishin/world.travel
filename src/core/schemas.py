from pydantic import BaseModel


class ContentCreate(BaseModel):
    content_type: str
    content_id: str
    data: str
    image_urls: dict


class TagsCreate(BaseModel):
    name: str
