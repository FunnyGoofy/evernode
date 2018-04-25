"""
    User Model
"""

from sqlalchemy import Column, String
from ..classes.security import Security
from ..classes.session import Session
from .base_model import BaseModel
from .password_reset_model import PasswordResetModel


class BaseUserModel(BaseModel):
    """ user db model """

    __abstract__ = True
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    email = Column(String(255), unique=True)
    password = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))
    exclude_list = ['password', 'updated_at', 'created_at', 'id']

    @classmethod
    def get_by_username(cls, username):
        """ get db model by username """
        return cls.query.filter_by(email=username).first()

    @classmethod
    def get_by_email(cls, email):
        """ get db model by username """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, user_id):
        """ get db user model by id """
        return cls.query.get(user_id)

    def set_password(self, password):
        """ set user password with hash """
        self.password = Security.hash(password)
        self.save()

    def create_password_reset(self) -> str:
        """
        Create a password reset request in the user_password_resets
        database table. Hashed code gets stored in the database.
        Returns unhashed reset code
        """
        if self.email is None:
            return None
        PasswordResetModel.delete_by_email(self.email)
        code = Security.random_string(6)
        password_reset_model = PasswordResetModel()
        password_reset_model.code = Security.hash(code)
        password_reset_model.email = self.email
        password_reset_model.user_id = self.id
        password_reset_model.save()
        return code

    def validate_password_reset(self, code, new_password):
        """
        Validates an unhashed code against a hashed code.
        Once the code has been validated and confirmed
        new_password will replace the old users password
        """
        if self.email is None:
            return None  # needs user email
        password_reset_model = PasswordResetModel.get_by_email(self.email)
        if password_reset_model is None:
            return False
        if Security.verify_hash(code, password_reset_model.code):
            self.set_password(new_password)
            PasswordResetModel.delete_by_email(self.email)
            return True
        return False

    @classmethod
    def by_current_session(cls):
        session = Session.current_session()
        if session is None:
            return None
        return cls.get_by_id(session.user_id)

    def __repr__(self):
        return super().json()
