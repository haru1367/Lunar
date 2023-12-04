"""The authentication state."""
import reflex as rx
from sqlmodel import select

from .base import State, User


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

       

    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Passwords do not match.")
            if session.exec(select(User).where(User.username == self.username)).first():
                return rx.window_alert("Username already exists.")
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
