"""Base state for Twitter example. Schema is inspired by https://drawsql.app/templates/twitter."""
from typing import Optional,List,Union
from sqlmodel import Field
import reflex as rx

class message(rx.Model, table = True):
    send_user:str = Field() # 메시지를 보낸 사람을 저장하는 영역
    receive_user:str = Field() # 메시지를 받은 사람을 저장하는 영역
    message:str = Field() # 메시지 내용
    created_at : str = Field() # 메시지를 보낸 시각

class GPT(rx.Model, table=True):
    user_id:str = Field()
    content: str = Field() #유저의 질문내용, KoGPT의 답변을 저장하는 영역
    author: str = Field() #유저의 아이디, KoGPT를 저장하는 영역
    created_at : str = Field() #질문 시각을 저장하는 영역

class Dday(rx.Model,table = True):
    user_id :str = Field()
    dday:str = Field()
    dday_content:str = Field()

class Calendar_Memo(rx.Model,table=True):
    user_id : str = Field()
    day:str = Field()
    memo:str = Field()

class Music_Playlist(rx.Model, table = True):
    user_id : str = Field()
    music_title : str = Field()
    music_album : str = Field()
    music_artist : str = Field()

class Video_Playlist(rx.Model,table = True):
    user_id : str = Field()
    video_url : str = Field()
    video_title : str = Field()

class Hotplace(rx.Model,table=True):
    search_at:str = Field()
    search_place:str=Field()
    

class Follows(rx.Model, table=True):
    """A table of Follows. This is a many-to-many join table.

    See https://sqlmodel.tiangolo.com/tutorial/many-to-many/ for more information.
    """

    followed_username: str = Field(primary_key=True)
    follower_username: str = Field(primary_key=True)


class User(rx.Model, table=True):
    """A table of Users."""

    user_realname : str = Field()
    user_email : str = Field()
    user_birthday_year : str = Field()
    user_birthday_month : str = Field()
    user_birthday_day : str = Field()
    username: str = Field()
    password: str = Field()


class Crater(rx.Model, table=True):
    """A table of Tweets."""

    content: str = Field()
    created_at: str = Field()
    author: str = Field()
    image_content: str = Field()


class State(rx.State):
    """The base state for the app."""

    user: Optional[User] = None

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/login")

    @rx.var
    def logged_in(self):
        """Check if a user is logged in."""
        return self.user is not None
