from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DATABASE, DB_COLLECTIONS

from worklog.user import User
from worklog.worklog import Worklog


def import_models():
    """Dynamic import of models"""
    return {"users": User, "worklogs": Worklog}


class DBStorage:
    """Connects with MongoDB database"""

    # Singleton instance
    _instance = None
    object_mappings = import_models()

    def __new__(cls):
        """Enforce single object"""
        if cls._instance is None:
            cls._instance = super(DBStorage, cls).__new__(cls)
            cls._instance.__count = 1
        return cls._instance

    def __init__(self):
        """Initializes the DBStorage instance"""
        if not hasattr(self, "_initialized"):
            self.__client = MongoClient(MONGODB_URI)
            self.__db = self.__client[MONGODB_DATABASE]
            self._initialized = True

    def all(self, collection: str = None, user_id: str = None):
        """Retrieve all documents"""
        if collection is not None and not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if user_id is not None and not isinstance(user_id, str):
            raise TypeError("User ID must be a string")
        if collection is not None and not self.__is_collection(collection):
            return "Collection not found"

        documents = []

        # Retrieve both users and worklogs if collection and user ID are None
        if collection is None and user_id is None:
            for coll in DB_COLLECTIONS:
                all_docs = self.__db[coll].find()
                for doc in all_docs:
                    documents.append(self.__get_instance(coll, doc))

        if collection and user_id is None:
            all_docs = self.__db[collection].find()
            for doc in all_docs:
                documents.append(self.__get_instance(collection, doc))

        if collection and user_id:
            docs = self.__db[collection].find({"_id": user_id})
            for doc in docs:
                documents.append(self.__get_instance(collection, doc))

        if not documents:
            return None

        return documents

    def get(self, collection: str, doc_id: str):
        """Retrieve the document"""
        if not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if not isinstance(doc_id, str):
            raise TypeError("Document ID must be a string")
        if not self.__is_collection(collection):
            return "Collection not found"

        # Get a document
        doc = self.__db[collection].find_one({"_id": doc_id})
        if doc:
            # Convert the document to an object based on the collection
            return self.__get_instance(collection, doc)
        return None

    def add(self, collection: str, obj: dict):
        """Add a new document"""
        if not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if not isinstance(obj, dict):
            raise TypeError("Object must be a dictionary")
        if not self.__is_collection(collection):
            return "Collection not found"

        # Modify object keys
        obj = self.__modify_keys(obj)

        # Insert the document and return the _id of the inserted document
        return self.__db[collection].insert_one(obj).inserted_id

    def update(self, collection: str, doc_id: str, obj: dict):
        """Update a document"""
        if not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if not isinstance(doc_id, str):
            raise TypeError("Document ID must be a string")
        if not isinstance(obj, dict):
            raise TypeError("Object must be a dictionary")

        # Remove keys not to update from the obj
        obj = self.__modify_keys(obj)
        for key, value in obj.items():
            if key in ["_id", "created_at", "updated_at"]:
                obj.pop(key, None)

        # Update a document using $set and $currentDate
        self.__db[collection].update_one(
            {"_id": doc_id}, {"$set": obj, "$currentDate": {"updated_at": True}}
        )

    def delete(self, collection: str, doc_id: str):
        """Delete a document"""
        if not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if not isinstance(doc_id, str):
            raise TypeError("Document ID must be a string")
        if not self.__is_collection(collection):
            return "Collection not found"

        # Delete a document
        self.__db[collection].delete_one({"_id": doc_id})

    def count(self, collection: str, user_id: str = None):
        """Count the number of documents"""
        if not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if user_id is not None and not isinstance(user_id, str):
            raise TypeError("User ID must be a string or None")
        if not self.__is_collection(collection):
            return "Collection not found"

        # Create the query based on whether user_id is provided
        query = {} if user_id is None else {"user_id": user_id}

        # Use count_documents to count the matching documents
        count = self.__db[collection].count_documents(query)

        return count

    def close(self):
        """Close the MongoDB client"""
        self.__client.close()

    def __is_collection(self, collection):
        return collection in DB_COLLECTIONS

    def __modify_keys(self, obj):
        """Modify keys by removing class prefix"""
        modified_obj = {}

        for key, value in obj.items():
            # Check if the key has a class prefix
            if "__" in key:
                # Remove the class prefix from the key
                new_key = key.split("__")[-1]
            else:
                new_key = key

            # Add the modified key-value pair to the new dictionary
            modified_obj[new_key] = value

        return modified_obj

    def __get_instance(self, collection, data):
        """Converts a dictionary to an object based on the collection"""
        if collection in self.object_mappings:
            instance_class = self.object_mappings[collection]
            instance = instance_class(**data)
            return instance
        else:
            # Handle the case where the collection is not mapped to any class
            raise ValueError(f"Collection '{collection}' is not mapped to any class.")
