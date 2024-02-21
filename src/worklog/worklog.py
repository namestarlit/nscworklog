"""worklog class"""

import re
from worklog.base import Base


class Worklog(Base):
    """Worklog class implementantion"""

    def __init__(self, title, description, user_id, *args, **kwargs):
        """Initializes an instance of Resource class"""
        super().__init__(*args, **kwargs)
        self.title = title
        self.description = description
        self.user_id = user_id

    def __str__(self):
        """String representation of the worklog"""
        return "[Worklog] (id='{}', title='{}')".format(self._id, self.title)
