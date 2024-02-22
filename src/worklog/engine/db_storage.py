from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DATABASE


class DBStorage:
    """Connects with MongoDB database"""

    # Singleton instance
    _instance = None

    def __new__(cls):
        """Enforce single object"""
        print("creating object...")
        if cls._instance is None:
            cls._instance = super(DBStorage, cls).__new__(cls)
            cls._instance.__count = 1
        return cls._instance
        
    def __init__(self):
        """Initializes the DBStorage instance"""
        if not hasattr(self, '_initialized'):
            self.__client = MongoClient(MONGODB_URI)
            self.__db = self.__client[MONGODB_DATABASE]
            self._initialized = True

    def all(self, collection: str = None, user_id: str = None):
        """Retrieve all documents"""
        if collection is not None and not isinstance(collection, str):
            raise TypeError("Collection must be a string")
        if user_id is not None and not isinstance(user_id, str):
            raise TypeError("User ID must be a string")
        if not self.__is_collection(collection):
            return "Collection not found"

        documents = []
        
        # Retrieve both users and worklogs if collection and user ID are None
        if collection is None and user_id is None:
            return None

        if collection and user_id is None:
            all_docs = self.__db[collection].find()
            documents = list(all_docs)

        if collection and user_id:
            docs = self.__db[collection].find({"_id": user_id})
            documents = list(docs)
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

        # Retrieve a document
        doc = self.__db[collection].find_one({"_id": doc_id})
        return doc

    def add(self, collection, obj: dict):
        """Add a new document"""
        if not isinstance(obj, dict):
            raise TypeError("Object must be a dictionary")
        if not self.__is_collection(collection):
            return "Collection not found"

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
        
        # Remove _id key in the obj
        obj_keys = obj.keys
        if "_id" in obj_keys:
            obj.pop("_id", None)
                    
        # Update a document using $set and $currentDate
        self.__db[collection].update_one({"_id": doc_id}, {"$set": obj, "$currentDate": {"updated_at": True}})

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

    def __is_collection(self, collection):
        return collection in ["users", "worklogs"]

    def close(self):
        """Close the MongoDB client"""
        self.__client.close()
