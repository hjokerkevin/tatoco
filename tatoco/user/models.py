# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
import hashlib
from flask_login import UserMixin

from tatoco.database import Column, PkModel, db, reference_col, relationship
from tatoco.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    reset_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None


    def check_password(self, value):
        """Check password."""
        return self.password == hashlib.md5(str(self.value).encode('utf8')).hexdigest()

    def save(self):
        self.active = False
        try:
            self.password = hashlib.md5(str(self.password).encode('utf8')).hexdigest()
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            
    def modify(self, _user):
        pass


    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
