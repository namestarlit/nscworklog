"""worklog class"""

from worklog.base import Base


class Worklog(Base):
    """Worklog class implementantion"""

    def __init__(
        self, title, user_id, description=None, status="pending", *args, **kwargs
    ):
        """Initializes an instance of Resource class"""
        super().__init__(*args, **kwargs)
        self.title = title
        self.description = description
        self.user_id = user_id
        self.status = status

    def __str__(self):
        """String representation of the worklog"""
        return "[Worklog] (id='{}', title='{}')".format(self._id, self.title)
