"""The authentication state."""
import reflex as rx
from sqlmodel import select,and_,or_
from .base import State, User
import re


class AuthState(State):
    """The authentication state for sign up and login page."""

    # 비밀번호 찾기 화면에서 유저가 입력한 아이디를 저장할 변수
    user_find_password_id:str

    # 비밀번호 찾기 화면에서 유저가 입력한 이메일을 저장할 변수
    user_find_password_email_address:str

    # 비밀번호 찾기 화면에서 유저가 입력한 생일을 저장할 변수1
    user_find_password_year:str

    # 비밀번호 찾기 화면에서 유저가 입력한 생일을 저장할 변수2
    user_find_password_month:str

    # 비밀번호 찾기 화면에서 유저가 입력한 생일을 저장할 변수3
    user_find_password_day:str


    # 태어난 연도를 선택하기 위한 리스트
    year : list[str] = ['1960','1961','1962','1963','1964','1965','1966','1967','1968','1969','1970',
                        '1971','1972','1973','1974','1975','1976','1977','1978','1979','1980',
                        '1981','1982','1983','1984','1985','1986','1987','1988','1989','1990',
                        '1991','1992','1993','1994','1995','1996','1997','1998','1999','2000',
                        '2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                        '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020',
                        '2021','2022','2023']
    
    # 태어난 달을 선택하기 위한 리스트
    month : list[str] = ['1','2','3','4','5','6','7','8','9','10','11','12']

    # 태어난 일을 선택하기 위한 리스트
    day : list[str] = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',
                       '21','22','23','24','25','26','27','28','29','30','31']

    # 유저의 실제 이름을 저장하는 변수
    user_realname : str

    # 유저의 아이디를 저장하는 변수
    username: str

    # 유저의 비밀번호를 저장하는 변수
    password: str

    # 유저의 태어난 연도를 저장하는 변수
    user_birthday_year : str

    # 유저의 태어난 달을 저장하는 변수
    user_birthday_month : str

    # 유저의 태어난 일을 저장하는 변수
    user_birthday_day : str

    # 비밀번호 확인값을 저장하는 변수
    confirm_password: str

    # 유저의 이메일 주소를 저장하는 변수
    user_email_address:str

    # 유저가 입력한 정보가 유효한 값인지 체크하는 변수
    user_password_valid:bool=False
    user_realname_valid:bool=False
    user_confirm_password_valid:bool=False
    user_email_address_valid:bool=False
    user_birthday_year_valid:bool = False
    user_birthday_month_valid:bool = False
    user_birthday_day_valid:bool = False

    # 설정한 회원가입정보 입력값이 유효한지 실시간으로 확인하는 함수
    @rx.var
    def time_valid_user_password(self)->bool:
        return self.user_password_valid
    
    @rx.var
    def time_valid_user_realname(self)->bool:
        return self.user_realname_valid
    
    @rx.var
    def time_valid_confirm_password(self)->bool:
        if (self.confirm_password != self.password) or self.confirm_password=='':
            self.user_confirm_password_valid=False
        else:
            self.user_confirm_password_valid=True
        return (self.confirm_password != self.password) or self.confirm_password==''
    
    @rx.var
    def time_valid_email_address(self)->bool:
        if '@' not in self.user_email_address:
            self.user_email_address_valid = False
        else :
            self.user_email_address_valid = True
        return '@' not in self.user_email_address
    
    @rx.var
    def time_valid_user_birthday_year(self)->bool:
        if self.user_birthday_year == '':
            self.user_birthday_year_valid = False
        else :
            self.user_birthday_year_valid = True
        return self.user_birthday_year==''
    
    @rx.var
    def time_valid_user_birthday_month(self)->bool:
        if self.user_birthday_month == '':
            self.user_birthday_month_valid = False
        else :
            self.user_birthday_month_valid = True
        return self.user_birthday_month==''
    
    @rx.var
    def time_valid_user_birthday_day(self)->bool:
        if self.user_birthday_day == '':
            self.user_birthday_day_valid = False
        else :
            self.user_birthday_day_valid = True
        return self.user_birthday_day==''
    
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
            else :
                return rx.window_alert('Username is available.')

    # 회원가입을 하는 버튼
    def signup(self):
        # 사용자가 입력한 모든 정보가 유효한 값일때때
        if (self.user_password_valid == True) and (self.user_confirm_password_valid == True) and (self.user_realname_valid==True) and (self.user_email_address_valid == True) and (self.user_birthday_year_valid == True) and (self.user_birthday_month_valid==True) and (self.user_birthday_day_valid == True):
            year = int(self.user_birthday_year)
            month = int(self.user_birthday_month)
            day = int(self.user_birthday_day)
            if year%4==0 and month ==2 and day >=29:
                return rx.window_alert('invalid birthday')
            if month in [2,4,6,9,11] and day ==31:
                return rx.window_alert('invalid birthday') 
            
            with rx.session() as session:

                # 아이디 중복체크를 했는지 판별
                if session.exec(select(User).where(User.username == self.username)).first():
                    return rx.window_alert('The ID that already exists. Please check ID duplicates first.')
                
                # 서버에 데이터 저장
                self.user = User(
                    username=self.username, 
                    password=self.password,
                    user_realname=self.user_realname,
                    user_email = self.user_email_address,
                    user_birthday_year = self.user_birthday_year,
                    user_birthday_month = self.user_birthday_month,
                    user_birthday_day= self.user_birthday_day
                    )
                session.add(self.user)
                session.expire_on_commit = False
                session.commit()
                return rx.redirect("/")
        else :
            return rx.window_alert('Please enter the information accurately')
        
    # 유저 비밀번호를 찾는 함수
    def find_user_password(self):
        with rx.session() as session:
            user_query = select(User).where(and_(User.username == self.user_find_password_id, User.user_email == self.user_find_password_email_address
                                                 ,User.user_birthday_year == self.user_find_password_year,User.user_birthday_month == self.user_find_password_month,
                                                 User.user_birthday_day == self.user_find_password_day))
            found_user = session.exec(user_query).one_or_none()

            if found_user:
                password_list = list(found_user.password)
                for i in range(3, len(password_list)):
                    password_list[i] = '*'
                password_hint = "".join(password_list)
                return rx.window_alert(f'Password Hint: {password_hint}')
            else:
                return rx.window_alert('There is no matching user information.')



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
