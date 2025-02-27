from django_mongoengine import Document
from mongoengine import ReferenceField, ListField
from ..models.item import Item


class Cluster(Document):
    """
    MongoDB Document for Cluster
    Usage: from api.models.cluster import Cluster
    """

    core_point = ReferenceField(Item, required=True)
    list_of_items = ListField(ReferenceField(Item), required=True)

    meta = {
        "collection": "clusters",
        "indexes": [
            "core_point",
            {"fields": ["list_of_items"], "sparse": True}
        ]
    }
