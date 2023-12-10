"""The state for the home page."""
from datetime import datetime
import tkinter as tk
import reflex as rx
from sqlmodel import select
import os
from .base import Follows, State, Tweet, User
from tkinter import filedialog


class HomeState(State):
    """The state for the home page."""

    tweet: str
    tweets: list[Tweet] = []

    friend: str
    search: str

    img: list[str]                                                             
    files: list[str] = []
    imgshow:bool=False

    def handle_file_selection(self):                                          
        root = tk.Tk()
        root.withdraw()  # 화면에 창을 보이지 않도록 함
        root.attributes('-topmost', True)
        file_paths = filedialog.askopenfilenames(master=root)

        # 선택된 파일 경로에 대한 처리
        for file_path in file_paths:
            file_name = os.path.basename(file_path)                           # 파일 이름과 확장자를 추출
            file_extension = os.path.splitext(file_name)[1]
            
            upload_data = open(file_path, "rb").read()                        # 선택한 파일을 저장
            outfile = f".web/public/{file_name}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file_name)

            # Set the files attribute
            self.files.append(file_name)
        if len(self.img)>0:
            self.change()

    #파일 업로드 함수
    async def handle_upload(                                                 
        self, files: list[rx.UploadFile]
    ):
        for file in files:
            upload_data = await file.read()
            outfile = f"/{file.filename}"

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)

    def change(self):
        self.imgshow = not (self.imgshow)

    #story 파일 선택 취소 함수        
    async def file_select_cancel(self):
        self.img=[]
        self.files=[]
        self.change()
    

    #게시물 업로드 함수
    async def post_tweet(self):
        if not self.logged_in:
            return rx.window_alert("Please log in to post a tweet.")                 # 로그인이 되어있지 않을 시 경고 메시지
        if len(self.tweet)==0:
            return rx.window_alert('Please write at least one character!')           # story 추가시 최소 한 글자 입력 경고 메시지
        if len(self.tweet)>70:
            return rx.window_alert('Please enter within 70 characters!')            # 150글자 이내로 입력제한
        
        await self.handle_upload(rx.upload_files())                                  # 이미지 추가
        
        with rx.session() as session:                                                # session에 생성한 story 모델 저장
            tweet = Tweet(
                author=self.user.username,                                           # author : 유저 아이디
                content=self.tweet,                                                  # content : 유저 story 입력 내용
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),             # created_at : stroy 작성 시간
                image_content=", ".join(self.files),                                 # image_content : 이미지 파일
            )
            
            session.add(tweet)
            session.commit()
            self.tweet = ""                                                          # session에 저장 후 story내용 초기화
            self.img=[]
            self.files=[]
            
        return self.get_tweets()

    #story 내용 불러오는 함수
    def get_tweets(self):
        """Get tweets from the database."""
        with rx.session() as session:
            if self.search:                                                          # story 검색 입력어가 있을경우
                self.tweets = (
                    session.query(Tweet)
                    .filter(Tweet.content.contains(self.search))                     # story 검색 입력단어가 포함된 story를 모두 가져옴
                    .all()[::-1]
                )
            else:
                self.tweets = session.query(Tweet).all()[::-1]                       # session에 저장된 모든 story를 가져옴

    def set_search(self, search):
        """Set the search query."""
        self.search = search
        return self.get_tweets()

    def follow_user(self, username):
        """Follow a user."""
        with rx.session() as session:
            friend = Follows(
                follower_username=self.user.username, followed_username=username
            )
            session.add(friend)
            session.commit()

    @rx.var
    def following(self) -> list[Follows]:
        """Get a list of users the current user is following."""
        if self.logged_in:
            with rx.session() as session:
                return session.exec(
                    select(Follows).where(
                        Follows.follower_username == self.user.username
                    )
                ).all()
        return []

    @rx.var
    def followers(self) -> list[Follows]:
        """Get a list of users following the current user."""
        if self.logged_in:
            with rx.session() as session:
                return session.exec(
                    select(Follows).where(
                        Follows.followed_username == self.user.username
                    )
                ).all()
        return []

    @rx.var
    def search_users(self) -> list[User]:
        """Get a list of users matching the search query."""
        if self.friend != "":
            with rx.session() as session:
                current_username = self.user.username if self.user is not None else ""
                users = session.exec(
                    select(User).where(
                        User.username.contains(self.friend),
                        User.username != current_username,
                    )
                ).all()
                return users
        return []
