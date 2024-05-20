from datetime import datetime
from pydantic import BaseModel


class Project(BaseModel):
    project_name: str
    project_description: str
    project_images: list[str]
    project_url: str | None
    project_start: datetime
    project_end: datetime


class Contact(BaseModel):
    instagram: str
    github: str
    linkedin: str


class HomePageInfo(BaseModel):
    id: str
    introduction: str
    photo: str
    highlighted_projects: list[Project]
    contact_info: Contact
