"""Worklog Base class"""

from bson import ObjectId
from datetime import datetime


class Base:
    """worklog Base class implementantion"""

    def __init__(self, *args, **kwargs):
        """Initializes Base class instantances"""
        # Set a random unique ID to the instance attribute 'id'
        self._id = str(ObjectId())

        # Handle additional keyword arguments
        if kwargs:
            ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    try:
                        value = datetime.strptime(value, ISO_FORMAT)
                    except ValueError as e:
                        raise e

                setattr(self, key, value)

        if not hasattr(self, "created_at") or self.created_at is None:
            self.created_at = datetime.utcnow()
        if not hasattr(self, "updated_at") or self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def __repr__(self):
        """Formal string representation of the LinkHubBase class."""
        return "<{}: (id='{}', created_at='{}', updated_at='{}')>".format(
            self.__class__.__name__, self._id, self.created_at, self.updated_at
        )

    def to_dict(self):
        """Returns a dictionary of all the key/value pairs."""
        # Copy the instance's dictionary
        new_dict = dict(self.__dict__)

        # Convert 'created_at' and 'updated_at' into ISO format.
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()

        # Delete unwanted keys
        for key in [""]:
            new_dict.pop(key, None)

        return new_dict
