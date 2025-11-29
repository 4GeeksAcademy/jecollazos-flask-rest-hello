from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Like"]] = relationship(back_populates="author")
    likes: Mapped[list["Like"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
 

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column( nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    likes: Mapped[list["Like"]] = relationship(back_populates="post")

    def serialize(self):
        return {
        "id": self.id,
        "title": self.title
        }
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
   

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text
        }
    


class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="likes")
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }

class Notification(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "user_id": self.user_id
        }
    

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id
        }



    
