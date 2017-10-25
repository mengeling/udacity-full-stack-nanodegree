from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return data for each instance of Genre in serializeable format"""

        return {
            'id': self.id,
            'name': self.name,
        }


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return data for each instance of Movie in serializeable format"""

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rating': self.rating,
            'genre_id': self.genre_id,
        }


engine = create_engine('sqlite:///moviecatalog.db')
Base.metadata.create_all(engine)
