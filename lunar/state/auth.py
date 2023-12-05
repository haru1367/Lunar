"""The authentication state."""
import reflex as rx
from sqlmodel import select
from .base import State, User
import re


class AuthState(State):
    """The authentication state for sign up and login page."""

    year : list[str] = ['1960','1961','1962','1963','1964','1965','1966','1967','1968','1969','1970',
                        '1971','1972','1973','1974','1975','1976','1977','1978','1979','1980',
                        '1981','1982','1983','1984','1985','1986','1987','1988','1989','1990',
                        '1991','1992','1993','1994','1995','1996','1997','1998','1999','2000',
                        '2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                        '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020',
                        '2021','2022','2023']
    month : list[str] = ['1','2','3','4','5','6','7','8','9','10','11','12']
    day : list[str] = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',
                       '21','22','23','24','25','26','27','28','29','30','31']

    user_realname : str
    username: str
    password: str
    user_birthday_year : str
    user_birthday_month : str
    user_birthday_day : str
    confirm_password: str
    user_email_address:str
    user_password_valid:bool=False
    user_realname_valid:bool=False

    # 설정한 회원가입정보 입력값이 유효한지 실시간으로 확인하는 함수
    @rx.var
    def time_valid_user_password(self)->bool:
        return self.user_password_valid
    
    @rx.var
    def time_valid_user_realname(self)->bool:
        return self.user_realname_valid
    
    @rx.var
    def time_valid_confirm_password(self)->bool:
        return self.confirm_password != self.password
    
    @rx.var
    def time_valid_email_address(self)->bool:
        return '@' not in self.user_email_address
    
    # 유저의 실제 이름 입력값이 유효한지 실시간으로 확인하는 함수
    @rx.var
    def time_valid_username(self)->bool:
        if len(self.user_realname) >=2 and len(self.user_realname)<=20:
            self.user_realname_valid=True
        else :
            self.user_realname_valid=False
        return len(self.user_realname)>20 or len(self.user_realname)<2
    
    # 유저가 입력한 비밀번호가 유효한지 실시간으로 확인하는 함수
    @rx.var
    def time_valid_password(self)->bool:
        pattern = re.compile(r'^[a-zA-Z0-9]{8,16}$')
        if bool(pattern.match(self.password)) == True:
            self.user_password_valid=True
        else:
            self.user_password_valid=False
        return not bool(pattern.match(self.password))
    
    # 설정한 아이디가 유효한 값인지 확인하는 함수
    def is_valid_string(self,text):
        pattern = re.compile("^[a-z][a-z0-9]*$")
        return bool(pattern.match(text))

    # 아이디 중복체크를 하는 함수
    def id_check(self):
        if len(self.username) < 6 :
            return rx.window_alert('The Nickname must contain at least 6 characters.')
        if self.username.islower() == False:
            return rx.window_alert('The Nickname must be composed of lowercase letters or a combination of lowercase letters and numbers.')
        if self.username.isalnum() == False:
            return rx.window_alert('Special characters and spaces cannot be included.')
        if self.is_valid_string(self.username) == False:
            return rx.window_alert('Characters other than alphabets and numbers cannot be entered.')
        self.user_id_valid=False
        with rx.session() as session:
            if session.exec(select(User).where(User.username == self.username)).first():
                return rx.window_alert('User nickname already exists.')


    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Passwords do not match.")
            self.user = User(username=self.username, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        """Log in a user."""
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.username == self.username)
            ).first()
            if user and user.password == self.password:
                self.user = user
                return rx.redirect("/")
            else:
                return rx.window_alert("Invalid username or password.")
