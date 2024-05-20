from litestar import Controller, get, Router
from pydantic import BaseModel

from backend.services.home.db import HomeFirestoreDB
from backend.services.home.models import HomePageInfo


class Item(BaseModel):
    name: str
    description: str


class HomeController(Controller):
    path = "/"
    tags = ["Home Page"]

    def __init__(self, owner: Router, db: HomeFirestoreDB):
        super().__init__(owner)
        self.db = db

    @get("hello")
    def get_home_page_info(self) -> list[HomePageInfo]:
        return self.db.fetch_all()
