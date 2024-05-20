from abc import ABC
from typing import TypeVar

from google.cloud import firestore
from google.cloud.firestore import CollectionReference
from pydantic import BaseModel
from google.cloud.firestore_v1 import DocumentSnapshot

T = TypeVar("T", bound=BaseModel)


class FirestoreConnectionProvider:
    def __init__(self):
        self._client = None

    def get_connection(self) -> firestore.Client:
        if self._client is None:
            self._client = firestore.Client()
        return self._client


class GenericFirestore(ABC):
    key = "id"
    model: type[T] = None
    collection_name: str = None

    def __init__(self, client: FirestoreConnectionProvider):
        self.client = client

    @property
    def collection(self) -> CollectionReference:
        db = self.client.get_connection()
        return db.collection(self.collection_name)

    def fetch_all(self) -> list[T]:
        docs = self.collection.stream()
        return [self.deserialize(d) for d in docs]

    def upsert(self, item: T) -> str:
        item_id, serialized_item = self.serialize(item)

        if not item_id:
            _, ref = self.collection.add(serialized_item)
        else:
            ref = self.collection.document(item_id)
            ref.set(serialized_item)
        return ref.id

    def serialize(self, item: T) -> tuple[str | None, dict[str, str | int | float | dict | list | None]]:
        validated_item = self.model.model_validate(item)
        serialized_item = validated_item.model_dump()
        item_id = serialized_item[self.key]
        del serialized_item[self.key]
        return item_id, serialized_item

    def deserialize(self, document_snapshot: DocumentSnapshot) -> T:
        serialized_item = document_snapshot.to_dict()
        serialized_item[self.key] = document_snapshot.id
        return self.model.model_validate(serialized_item)
