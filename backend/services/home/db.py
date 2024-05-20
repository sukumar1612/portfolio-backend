from backend.services.home.models import HomePageInfo
from core.generic_firestore import GenericFirestore


class HomeFirestoreDB(GenericFirestore):
    model = HomePageInfo
    collection_name = "HomePage"
