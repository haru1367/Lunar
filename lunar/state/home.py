"""The state for the home page."""
from datetime import datetime,timedelta
import tkinter as tk
import reflex as rx
from sqlmodel import select
import os
from .base import Follows, State, Crater, User,Hotplace,Video_Playlist,Music_Playlist
from tkinter import filedialog
import folium
from folium.plugins import MiniMap
import requests
import pandas as pd
import numpy as np
import json
import asyncio
from sqlalchemy.sql import func,desc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime
from datetime import datetime
from melon import *
import time
from PIL import Image
from bs4 import BeautifulSoup as bs

class HomeState(State):
    """The state for the home page."""

    # 데이터 베이스 저장된 crater 불러오기
    crater: str
    craters: list[Crater] = []

    # 친구,crater 검색
    friend: str
    search: str

    # 파일 선택 변수
    img: list[str]                                                             
    files: list[str] = []
    imgshow:bool=False

    # map 키워드 검색
    map_count:int=1
    map_search_input:str=''
    map_html:str='/map.html'
    map_iframe:str
    df : pd.DataFrame
    start_location_x:str
    start_location_y:str
    end_location_x:str
    end_location_y:str
    KAKAO_REST_API_KEY:str
    taxi_fee:str
    toll_fee:str
    distance:str
    path_time:str
    map_hotplaces : list[Hotplace] = []

    # video 검색
    search_video:str
    youtube_results: list[str]=[]
    saved_video_results : list[Video_Playlist]
    show : bool = False
    popup_video_url:str
    popup_video_title:str

    # music 검색
    search_singer:str
    search_singer_result:list[dict]
    music_chart_info : list[dict]
    saved_music_results : list[Music_Playlist]

    #재난문자 저장
    weather_message_result : list[dict]

    #날씨 웹 크롤링
    weather_search_show : bool = False
    weather_search:str
    status_climate:str
    status_climate_icon_url:str
    status_temperature:str
    status_feel_temperature:str
    today_min_temperature:str
    today_max_temperature:str
    status_humidity:str
    status_atmospheric_pressure:str
    status_wind_direction:str
    status_wind_speed:str
    image:str

    @rx.var
    def time_map_iframe(self)->str:
        self.map_iframe=f'<iframe src="{self.map_html}" width="100%" height="500px"></iframe>'
        return self.map_iframe

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

    # 파일 업로드 함수
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

    # 파일선택창 화면띄우는 함수
    def change(self):
        self.imgshow = not (self.imgshow)

    # Crater 파일 선택 취소 함수        
    async def file_select_cancel(self):
        self.img=[]
        self.files=[]
        if len(self.img)>0:
            self.change()
    

    # Crater 업로드 함수
    async def post_crater(self):
        if not self.logged_in:
            return rx.window_alert("Please log in to post a crater.")                 # 로그인이 되어있지 않을 시 경고 메시지
        if len(self.crater)==0:
            return rx.window_alert('Please write at least one character!')           # story 추가시 최소 한 글자 입력 경고 메시지
        if len(self.crater)>70:
            return rx.window_alert('Please enter within 70 characters!')            # 150글자 이내로 입력제한
        
        await self.handle_upload(rx.upload_files())                                  # 이미지 추가
        
        with rx.session() as session:                                                # session에 생성한 story 모델 저장
            crater = Crater(
                author=self.user.username,                                           # author : 유저 아이디
                content=self.crater,                                                  # content : 유저 story 입력 내용
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),             # created_at : stroy 작성 시간
                image_content=", ".join(self.files),                                 # image_content : 이미지 파일
                heart_list='',
                comment_list='',
                heart_num=0,
                comment_num=0,
                
            )
            
            session.add(crater)
            session.commit()
            self.crater = ""                                                          # session에 저장 후 story내용 초기화
            self.img=[]
            self.files=[]
            
        return self.get_craters()

    # Crater 내용 불러오는 함수
    def get_craters(self):
        """Get craters from the database."""
        with rx.session() as session:
            if self.search:                                                          # story 검색 입력어가 있을경우
                self.craters = (
                    session.query(Crater)
                    .filter(Crater.content.contains(self.search))                     # story 검색 입력단어가 포함된 story를 모두 가져옴
                    .all()[::-1]
                )
            else:
                self.craters = session.query(Crater).all()[::-1]                       # session에 저장된 모든 story를 가져옴



    def set_search(self, search):
        """Set the search query."""
        self.search = search
        return self.get_craters()

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
    
    # KaKao Rest API Key를 받아오는 함수     
    def kakao_api(self): 
        key=''
        with open('kakaoapikey.json','r')as f:                                               
            key = json.load(f)
        self.KAKAO_REST_API_KEY = key['key']
    
    # kakao api 검색으로 장소 목록을 받는 함수   
    def elec_location(self,region,page_num):
        self.kakao_api()                                                                    
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': region,'page': page_num}                                         
        headers = {"Authorization": f'KakaoAK {self.KAKAO_REST_API_KEY}'}                   
        places = requests.get(url, params=params, headers=headers).json()['documents']                                                                         
        return places  
    
    # 장소목록의 정보를 가져오는 함수
    def elec_info(self,places):
        X = []    # 경도                                                        
        Y = []    # 위도                                                                    
        stores = []                                                                        
        road_address = []                                                                   
        place_url = []                                                                      
        ID = []                                                                             

        for place in places:                                                                
            X.append(float(place['x']))
            Y.append(float(place['y']))
            stores.append(place['place_name'])
            road_address.append(place['road_address_name'])
            place_url.append(place['place_url'])
            ID.append(place['id'])

        ar = np.array([ID,stores, X, Y, road_address,place_url]).T                          
        df = pd.DataFrame(ar, columns = ['ID','stores', 'X', 'Y','road_address','place_url']) 
        return df

    #사용자가 입력한 키워드로 정보를 받아와 데이터 프레임 생성
    def keywords(self):
        df = None
        for loca in self.locations:                                                         
            for page in range(1,4):                                                         
                local_name = self.elec_location(loca, page)                                
                local_elec_info = self.elec_info(local_name)                                

                if df is None:                                                              
                    df = local_elec_info
                elif local_elec_info is None:                                               
                    continue
                else:                                                                       
                    df = pd.concat([df, local_elec_info],join='outer', ignore_index = True)
        return df

    # 데이터 프레임을 기준으로 지도를 생성하는 함수
    def make_map(self,dfs):
        m = folium.Map(location=[37.5518911,126.9917937],                                   
                    zoom_start=7)

        minimap = MiniMap()                                                                 
        m.add_child(minimap)
        for i in range(len(dfs)):                                                           
            folium.Marker([dfs['Y'][i],dfs['X'][i]],                                       
                    tooltip=dfs['stores'][i],                                               
                    popup=dfs['place_url'][i],                                              
                    ).add_to(m)
        return m
    
    # 지도 기본설정
    def standard_map(self):
        m = folium.Map(location=[37.5518911,126.9917931],zoom_start=12)
        m.save('assets/map.html')

    # 키워드로 지도검색하는 함수
    async def map_search(self):
        if self.map_search_input == "":                                                          
            return rx.window_alert('Please enter your search term!')
        self.map_count+=1                        
        self.locations = self.map_search_input.split(',')                                         
        self.df = self.keywords()
        m = self.make_map(self.df)
        if self.map_html == '/map2.html':
            m.save('assets/map3.html')
            self.map_html = '/map3.html'
        else :
            m.save('assets/map2.html')
            self.map_html = '/map2.html'
        await asyncio.sleep(1)
        self.map_iframe = self.time_map_iframe
        self.df = self.df.drop_duplicates(['ID']) 
        self.df['place url'] = self.df['place_url']
        self.df = self.df.drop('place_url', axis=1)                                         
        self.df = self.df.reset_index()
        with rx.session() as session:
            hotplace = Hotplace(
                search_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                search_place = self.map_search_input,
            )
            session.add(hotplace)
            session.commit()

    # 지도 초기화 함수
    def map_clear(self):
        self.map_html = '/map.html'

    # kakaoapi 길찾기함수
    async def get_directions(self):
        self.kakao_api()
        api_url = "https://apis-navi.kakaomobility.com/v1/directions"
        origin = self.start_location_x+','+self.start_location_y
        destination = self.end_location_x+','+self.end_location_y

        headers = {
            "Authorization": f"KakaoAK {self.KAKAO_REST_API_KEY}"
        }

        params = {
            "origin": origin,
            "destination": destination,
        }

        response = requests.get(api_url, headers=headers, params=params)
        result = response.json()
        m = folium.Map(location=[37.5518911,126.9917931],zoom_start=7)
        location_list =[]
        for i in range(0,len(result['routes'][0]['sections'][0]['guides'])):
            location_list.append([result['routes'][0]['sections'][0]['guides'][i]['y'],result['routes'][0]['sections'][0]['guides'][i]['x']])
            folium.Marker([result['routes'][0]['sections'][0]['guides'][i]['y'],result['routes'][0]['sections'][0]['guides'][i]['x']],
                          tooltip=f"{result['routes'][0]['sections'][0]['guides'][i]['name']}",
                          popup=f"{result['routes'][0]['sections'][0]['guides'][i]['name']}",
                          icon = folium.Icon(color='orange',icon='info-sign'),
                          ).add_to(m)
        folium.PolyLine(locations=location_list,                                       
                color = 'black',                             
                ).add_to(m)
        if self.map_html == '/map2.html':
            m.save('assets/map3.html')
            self.map_html = '/map3.html'
        else :
            m.save('assets/map2.html')
            self.map_html = '/map2.html'
        await asyncio.sleep(1)
        self.map_iframe = self.time_map_iframe
        self.taxi_fee = f"택시비용 : {result['routes'][0]['summary']['fare']['taxi']}원"
        self.toll_fee = f"톨게이트비용 : {result['routes'][0]['summary']['fare']['toll']}원"
        distance = result['routes'][0]['summary']['distance']
        self.distance = f'총 이동거리 : {float(distance)/float(1000)}km'
        path_time = result['routes'][0]['summary']['duration']
        path_time_h = path_time//3600
        path_time_m = (path_time%3600)//60
        path_time_s = path_time%60
        self.path_time = f'소요시간 : {path_time_h}시간 {path_time_m}분 {path_time_s}초'

    # 최근 하루 동안 핫플레이스 검색하는 함수
    def hotplaces(self):
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        twenty_four_hours_ago_without_microseconds = twenty_four_hours_ago.replace(microsecond=0)
        with rx.session() as session:
            self.map_hotplaces = (
                session.query(Hotplace)
                .filter(
                    func.datetime(Hotplace.search_at) >= twenty_four_hours_ago_without_microseconds.strftime("%Y-%m-%d %H:%M:%S")
                )
                .order_by(
                    desc(func.count(Hotplace.search_place)),
                    desc(func.datetime(Hotplace.search_at))
                )
                .group_by(Hotplace.search_place)
                .all()
            )

    # youtube링크를 가져오는 함수
    def get_youtube_links(self):
        search_word = self.search_video
        url = f'https://www.youtube.com/results?search_query={search_word}' 
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(service=service,options=options)
        driver.get(url)
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        titles = driver.find_elements(By.CSS_SELECTOR,"#dismissible.style-scope.ytd-video-renderer")
        self.youtube_results = []
        for title in titles:
            result = ''
            main_title = title.find_element(By.CSS_SELECTOR,"#video-title").get_property("title")
            tube_url = title.find_element(By.CSS_SELECTOR,"#video-title").get_property("href")
            result += main_title
            result += ','
            result += tube_url
            self.youtube_results.append(result)

    # 나중에 볼 동영상에 추가
    def add_video_playlist(self, video_url,video_title):
        if not self.logged_in:
            return rx.window_alert("Please log in to save video.")          
        with rx.session() as session:
            existing_playlist = session.query(Video_Playlist).filter_by(
                user_id=self.user.username,
                video_url=video_url,
                video_title=video_title
            ).first()

            if existing_playlist:
                # Playlist with the same URL and title already exists
                return rx.window_alert("This video is already in your playlist.")

            new_playlist = Video_Playlist(
                user_id = self.user.username,
                video_url = video_url,
                video_title = video_title,
            )
            session.add(new_playlist)
            session.commit()
        return self.get_saved_video()

    # 나중에 볼 영상에서 제거
    def remove_video_playlist(self, video_url):
        if not self.logged_in:
            return rx.window_alert("Please log in to remove video.")
        
        with rx.session() as session:
            video_playlist_entry = session.query(Video_Playlist).filter_by(user_id=self.user.username, video_url=video_url).first()
            
            if video_playlist_entry:
                # 찾은 동영상을 재생목록에서 제거하고 커밋
                session.delete(video_playlist_entry)
                session.commit()
        return self.get_saved_video()

    # 동영상 저장 리스트를 불러오는 함수
    def get_saved_video(self):
        if not self.logged_in:
            return rx.window_alert("Please log in to see saved video.")
        with rx.session() as session:
            self.saved_video_results = session.query(Video_Playlist).filter(Video_Playlist.user_id == self.user.username).all()[::-1]

    # 동영상 팝업을 띄우는 함수
    def popup_video(self,video_url,video_title):
        self.show = not (self.show)
        self.popup_video_url = video_url
        self.popup_video_title = video_title

    # 실시간 멜론차트 Top100을 불러오는 함수
    def music_chart(self):
        self.music_chart_info = []
        chart_data = ChartData(imageSize=500)
        chart_entries = chart_data.entries
        for entry in chart_entries:
            entry_dict = {
                'artist' : entry.artist,
                'title': entry.title,
                'lastPos':entry.lastPos, 
                'rank': entry.rank,
                'isNew' : entry.isNew,
            }
            self.music_chart_info.append(entry_dict)

    # 멜론 가수 크롤링 
    def melon_singer_crawling(self):
        url = "https://www.melon.com/search/keyword/index.json"
        params = {
                'jscallback' : "jQuery19105357803934720518_1603168193882",
                'query' : self.search_singer
        }
        headers = {
                'Referer' : "http://www.melon.com/index.htm",
                "User-Agent" : ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                                (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36")
        }
        response = requests.get(url, headers = headers, params = params)
        response = response.text

        json_string = response.replace(params['jscallback'] + '(', '').replace(');', '')
        result_dict = json.loads(json_string)
        self.search_singer_result = []
        for song in result_dict['SONGCONTENTS']:
            data = {'ARTIST NAME' : song['ARTISTNAME'], 'ALBUM NAME' : song['ALBUMNAME'],'SONG NAME' : song['SONGNAME']}
            self.search_singer_result.append(data)

    # 음악 플레이리스트 추가
    def add_music_playlist(self, music_title,music_album,music_artist):
        if not self.logged_in:
            return rx.window_alert("Please log in to save video.")          
        with rx.session() as session:
            existing_playlist = session.query(Music_Playlist).filter_by(
                user_id=self.user.username,
                music_title = music_title,
                music_album = music_album,
                music_artist = music_artist,
            ).first()

            if existing_playlist:
                # Playlist with the same URL and title already exists
                return rx.window_alert("This Music is already in your playlist.")

            new_playlist = Music_Playlist(
                user_id = self.user.username,
                music_title = music_title,
                music_album = music_album,
                music_artist = music_artist,
            )
            session.add(new_playlist)
            session.commit()
        return self.get_saved_music()
    
    # 음악 플레이리스트를 불러오는 함수
    def get_saved_music(self):
        if not self.logged_in:
            return rx.window_alert("Please log in to see saved video.")
        with rx.session() as session:
            self.saved_music_results = session.query(Music_Playlist).filter(Music_Playlist.user_id == self.user.username).all()[::-1]

    # 음악 플레이리스트에서 제거
    def remove_music_playlist(self, music_title, music_album, music_artist):
        if not self.logged_in:
            return rx.window_alert("Please log in to remove video.")
        
        with rx.session() as session:
            music_playlist_entry = session.query(Music_Playlist).filter_by(user_id=self.user.username, music_title = music_title, music_album = music_album, music_artist = music_artist).first()
            
            if music_playlist_entry:
                # 찾은 동영상을 재생목록에서 제거하고 커밋
                session.delete(music_playlist_entry)
                session.commit()
        return self.get_saved_music()

    # 재난문자 웹 크롤링
    def climate_message(self):
        url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9E%AC%EB%82%9C%EB%AC%B8%EC%9E%90"
        response = requests.get(url)
        html = response.text
        soup = bs(html, 'html.parser')
        areas = soup.select(".area")
        disaster_texts = soup.select(".disaster_text")
        dates = soup.select(".date")
        self.weather_message_result = []
        # 결과 출력
        for area, disaster_text, date in zip(areas, disaster_texts, dates):
            data = {'area' : area.get_text(strip=True), 'date' : date.get_text(strip=True), 'text':disaster_text.get_text(strip = True) }
            self.weather_message_result.append(data)

    # 날씨 웹 크롤링
    def climate_websearch(self):
        key=''
        with open('weatherapikey.json','r')as f:                                               
            key = json.load(f)
        weather_api_key = key['key']
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.weather_search}&appid={weather_api_key}&lang=kr&units=metric"
        result = requests.get(url)
        data = json.loads(result.text)
        self.status_climate = data['weather'][0]['description']
        self.status_temperature = data['main']['temp']
        self.status_feel_temperature = data['main']['feels_like']
        self.today_min_temperature = data['main']['temp_min']
        self.today_max_temperature = data['main']['temp_max']
        self.status_humidity = data['main']['humidity']
        self.status_atmospheric_pressure = data['main']['pressure']
        self.status_wind_direction = data['wind']['deg']
        self.status_wind_speed = data['wind']['speed']
        self.status_climate_icon_url=  f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        self.image = Image.open((requests.get(self.status_climate_icon_url, stream=True).raw))
        self.weather_search_show=True