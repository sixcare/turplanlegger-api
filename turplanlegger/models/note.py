from typing import Dict

from flask import g

from turplanlegger.app import db

JSON = Dict[str, any]


class Note:
    """A Note object. An object containing information.

    Args:
        owner (str): The UUID4 of the owner of the object
        content (str): The contents of the note
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        id (int): Optional, the ID of the object
        owner (str): The UUID4 of the owner of the object
        content (str): The contents of the note
        private (bool): Flag if the trip is private
                        Default so False (public)
        name (str): The name or title of the note
        create_time (datetime): Time of creation,
                                Default: datetime.now()
    """

    def __init__(self, owner: str, content: str, private: bool = True, **kwargs) -> None:
        if not owner:
            raise ValueError('Missing mandatory field \'owner\'')
        if not isinstance(owner, str):
            raise TypeError('\'owner\' must be str')
        if not content:
            raise ValueError('Missing mandatory field \'content\'')
        if not isinstance(content, str):
            raise TypeError('\'content\' must be string')
        if not isinstance(private, bool):
            raise TypeError("'private' must be boolean")

        self.owner = owner
        self.content = content
        self.private = private
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.create_time = kwargs.get('create_time', None)

    @classmethod
    def parse(cls, json: JSON) -> 'Note':
        """Parse input JSON and return an Note object.

        Args:
            json (Dict[str, any]): JSON input object

        Returns:
            A Note object
        """
        return Note(
            id=json.get('id', None),
            owner=g.user.id,
            content=json.get('content', None),
            private=json.get('private', None),
            name=json.get('name', None)
        )

    @property
    def serialize(self) -> JSON:
        """Serialize the Note instance, returns it as Dict(str, any)"""
        return {
            'id': self.id,
            'owner': self.owner,
            'name': self.name,
            'content': self.content,
            'private': self.private,
            'create_time': self.create_time
        }

    def create(self) -> 'Note':
        """Creates the Note object in the database"""
        note = self.get_note(db.create_note(self))
        return note

    def delete(self) -> bool:
        """Deletes the Note object from the database
        Returns True if deleted"""
        return db.delete_note(self.id)

    def rename(self) -> 'Note':
        """Change name of the Note
        Won't change name if new name is the same as current

        Args:
            owner (str): id (uuid4) of the new owner

        Returns:
            The updated Note object
        """
        return db.rename_note(self.id, self.name)

    def update(self) -> 'Note':
        """Updates the Note content or privacy object in the database"""
        return db.update_note(self.id, self.content, self.private)

    @staticmethod
    def find_note(id: int) -> 'Note':
        """Looks up an Note based on id

        Args:
            id (int): Id of Note

        Returns:
            An Note
        """
        return Note.get_note(db.get_note(id))

    @staticmethod
    def find_note_by_owner(owner_id: str) -> '[Note]':
        """Looks up Notes by owner

        Args:
            owner_id (str): Id (uuid4) of owner

        Returns:
            A list of Note objects
        """
        return [Note.get_note(note) for note in db.get_note_by_owner(owner_id)]

    def change_owner(self, owner: str) -> 'Note':
        """Change owner of the Note
        Throws ValueError if new owner is the same as current

        Args:
            owner (str): id (uuid4) of the new owner

        Returns:
            The updated Note object
        """
        if self.owner == owner:
            raise ValueError('new owner is same as old')

        return Note.get_note(db.change_note_owner(self.id, owner))

    @classmethod
    def get_note(cls, rec) -> 'Note':
        """Converts a database record to an Note object

        Args:
            rec (NamedTuple): Database record

        Returns:
            An Note object
        """
        if rec is None:
            return None

        return Note(
            id=rec.id,
            owner=rec.owner,
            name=rec.name,
            content=rec.content,
            private=rec.private,
            create_time=rec.create_time
        )
