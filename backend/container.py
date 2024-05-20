import firebase_admin
from dependency_injector import containers, providers

from backend.api.home import HomeController
from backend.services.home.db import HomeFirestoreDB
from core.generic_firestore import FirestoreConnectionProvider
from core.http_api_controller import HTTPApiController


class AppContainer(containers.DeclarativeContainer):
    # firebase app
    admin_app_name = providers.Object("FirebaseAdminApp")
    admin_credential = providers.Singleton(firebase_admin.credentials.Certificate, "keys.json")
    firebase_app = providers.Singleton(firebase_admin.initialize_app, credential=admin_credential, name=admin_app_name)

    # firestore DB connections
    firestore_client = providers.Singleton(
        FirestoreConnectionProvider
    )
    home_page_db = providers.Singleton(
        HomeFirestoreDB,
        client=firestore_client
    )

    # routers
    home_router = providers.Singleton(
        HTTPApiController,
        controller=HomeController,
        base_prefix="/",
        db=home_page_db
    )
