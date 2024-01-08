# lunar.state.home 모듈에서 필요한 State 및 HomeState를 가져옵니다.
import reflex as rx
from lunar.state.base import State
from lunar.state.home import HomeState
from PIL import Image
# 컴포넌트를 가져옵니다.
from ..components import container

color = "rgb(107,99,246)"
# 탭 버튼을 생성하는 함수
def tab_button(imagepath, href):
    """A tab switcher button."""
    return rx.link(
        rx.image(
            src=imagepath,
            height='40px',
            width='40px',
        ),
        display="inline-flex",
        align_items="center",
        py=3,
        px=2,
        href=href,  # 버튼 클릭 시 이동할 경로
    )

def message(message):
    return rx.box(
        rx.button(
            rx.vstack(
                rx.box(
                    rx.text(
                        message['date'],
                        style={'white-space': 'normal'},
                        font_Size = '15px',
                        font_weight= 'bolder',
                    ),
                    bg = '#dec445',
                ),
                rx.text(),
                rx.text(
                    message['area'],
                    style={'white-space': 'normal'},
                    font_Size = '13px',
                    font_weight='bold',
                ),
                rx.divider(variant="dashed", border_color="black"),
                rx.text(
                    message['text'],
                    style={'white-space': 'normal'},
                    font_size = '15px',
                ),
                width = '100%',
            ),
            height='auto',
            width='90%',
        ),
        rx.container(height='5px'),
        align='start',
        padding='5px',  # 테두리와 내용 사이의 여백 지정
    )

# 왼쪽에 표시되는 탭 스위처
def tabs():
    """The tab switcher displayed on the left."""
    return rx.box(
        rx.vstack(
            rx.container(
                rx.hstack(
                    rx.image(
                        src='/moon.png',
                        height='60px',
                        width='60px',         
                    ),
                    rx.text(
                        "Lunar", 
                        style={
                            "fontSize": "40px",
                            "fontWeight": "bolder",
                            "fontFamily": "Calibri, Calibri",
                            "background": "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)",
                            "-webkit-background-clip": "text",
                            "color": "transparent",
                        },
                        center_content=True,
                    ),  # 앱 이름
                ),
            ),
            rx.vstack(
                rx.hstack(
                    rx.container(width='5px'),
                    rx.vstack(
                        rx.container(height='10px'),
                        rx.vstack(
                            rx.button('Disaster',Font_size = '20px',on_click = HomeState.climate_message,bg = '#eb7373'),
                        ),
                        rx.container(height='5px'),
                        rx.foreach(
                            HomeState.weather_message_result,
                            message,
                        ),
                        rx.container(height='4px'),
                        align_items='start',
                        width ='100%',
                    ),
                ),
                align_items = 'start',
                margin_left = '20px',
                border = '3px solid #000000',
                border_radius = '30px',
                box_Shadow = '10px 10px 5px #d61c4e',
                width = '90%',
            ),
            align_items="start",
            gap=4,
        ),
        py=4,
        overflow='auto',
    )

# 오른쪽에 표시되는 사이드바
def sidebar(HomeState):
    """The sidebar displayed on the right."""
    return rx.vstack(
        rx.vstack(
            rx.text('Route search',font_size='35px'),
            rx.hstack(
                rx.image(src='/startpoint.png',height='35px',width='35px'),
                rx.text('origin',font_size = '20px'),
                align_items='start',
                width = '100%',
            ),
            rx.input(
                on_change=HomeState.set_start_location_x,
                placeholder="starting point longitude", 
                width="100%",
                border = "3px solid #000000",
            ),
            rx.input(
                on_change=HomeState.set_start_location_y,
                placeholder="starting point latitude", 
                width="100%",
                border = "3px solid #000000",
            ),
            rx.hstack(
                rx.image(src='/endpoint.png',height='35px',width='35px'),
                rx.text('Destination',font_size='20px'),
                align_items='start',
                width='100%',
            ),
            rx.input(
                on_change=HomeState.set_end_location_x,
                placeholder="end point longitude", 
                width="100%",
                border = "3px solid #000000",
            ),
            rx.input(
                on_change=HomeState.set_end_location_y,
                placeholder="end point latitude", 
                width="100%",
                border = "3px solid #000000",
            ),
            rx.vstack(
                rx.button(
                    'Search',
                    on_click = HomeState.get_directions,
                    bg="#e85e1e",
                    color="white",
                    _hover={"bg": "orange.900"},
                ),
                align_items='left',
                width='100%',
            ),
            rx.container(height='30px'),
            border = '3px solid #000000',
            box_Shadow = '10px 10px 5px #307849',
            border_radius = '20px',
            width = '90%',
        ),
        rx.container(height='40px'),
        rx.vstack(
            rx.vstack(
                rx.text('Route search result',font_size='30px'),
            ),
            rx.vstack(
                rx.text(HomeState.distance,font_size = '25px'),
                rx.text(HomeState.path_time,font_size ='25px'),
                rx.text(HomeState.taxi_fee, font_size = '20px'),
                rx.text(HomeState.toll_fee, font_size = '20px'),
                align_items='start',
            ),
            border = '3px solid #000000',
            border_radius = '20px',
            box_Shadow = '10px 10px 5px #973dba',
            width = '90%',
        ),
        align_items="start",
        gap=4,
        h="100%",
        width = '100%',
        py=4,
        overflow='auto',
    )

# 피드의 헤더
def feed_header(HomeState):
    """The header of the feed."""
    return rx.hstack(
        rx.image(src='/find1.png',height='35px',width='35px'),
        rx.input(on_change=HomeState.set_weather_search, placeholder="Search place..!"),
        rx.button('search', on_click = HomeState.climate_websearch),
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        rx.container(height='10px'),
        rx.vstack(
            rx.cond(
                HomeState.weather_search_show,
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            HomeState.weather_search,
                            as_='mark',
                            font_Size = '50px',
                        ),
                        margin_left = '5%',
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                f"현재 기온 : {HomeState.status_temperature}'C",
                                font_Size = '25px',
                                font_weight='bold',
                            ),
                            rx.text(
                                f'현재 날씨 : {HomeState.status_climate}',
                                font_Size = '25px',
                                font_weight='bolder',
                            ),
                            rx.text(
                                f"체감 온도 : {HomeState.status_feel_temperature}'C",
                                font_Size = '25px',
                                font_weight='bolder',
                            ),
                            rx.text(
                                f"최저 온도 : {HomeState.today_min_temperature}'C",
                                font_Size = '25px',
                                font_weight='bolder',
                                color = 'blue',
                            ),
                            rx.text(
                                f"최고 온도 : {HomeState.today_max_temperature}'C",
                                font_Size = '25px',
                                font_weight='bolder',
                                color = 'red',
                            ),
                            rx.text(
                                f'현재 습도 : {HomeState.status_humidity}%',
                                font_Size = '25px',
                                font_weight='bolder',
                            ),
                            rx.text(
                                f'현재 기압 : {HomeState.status_atmospheric_pressure}hpa',
                                font_Size = '25px',
                                font_weight='bolder',
                            ),
                            rx.text(
                                f'풍속 : {HomeState.status_wind_speed}m/s',
                                font_Size = '25px',
                                font_weight='bolder',
                            ),
                            align_items='start',
                            margin_left = '5%',
                        ),
                        rx.container(width='5%'),
                        rx.vstack(
                            rx.image(
                                src = HomeState.image,
                                height='400px',
                                width = 'auto',
                            )
                        )
                    ),
                    width = '90%',
                    margin_left = '5%',
                    align_items='start',
                    border = '2px solid #000000',
                    border_radius = '30px',
                    box_Shadow = '10px 10px 10px #575050',
                ),
                rx.vstack(
                    rx.heading(
                        'Enter the area where you want to search for weather.',
                        font_Size = '40px',
                        font_weight='border',
                    ),
                    align_items='start',
                    width = '100%',
                )
            )
        ),
        rx.container(height='20px'),
        overflow='auto',
    )

# 홈 페이지
def weather():
    State.check_login
    return rx.vstack(
        rx.grid(
            tabs(),
            feed(HomeState),
            sidebar(HomeState),
            grid_template_columns="2fr 5fr 2fr",
            width='97%',
            h="90vh",
            gap=4,
        ),
        rx.grid(
            rx.vstack(
                rx.container(height='5px'),
                rx.button(
                    rx.icon(tag="moon"),
                    on_click=rx.toggle_color_mode,
                    width = '80%',
                    _hover={"bg": "orange.400"},
                ),
                width = '100%',
            ),
            rx.vstack(
                rx.hstack(
                    tab_button('/Home.png','/'),
                    tab_button('/profile.png','/profile'),
                    tab_button('/map.png','/map'),
                    tab_button('/chat.png','/chat'),
                    tab_button('/Aichat.png','/aichat'),
                    tab_button('/diary.png','/diary'),
                    tab_button('/video.png','/video'),
                    tab_button('/game.png','/game'),
                    tab_button('/music.png','/music'),
                    tab_button('/weather.png','/weather'),
                    tab_button('/setting.png','/setting'),
                    margin_right='5px',
                    border="1px solid #000000",
                    border_radius="full",
                    box_Shadow = '10px 10px 5px #3083f0',
                ),
                width = '100%',
            ),
            rx.vstack(
                rx.container(height='5px'),
                rx.button(
                    "Sign out",
                    on_click=State.logout,
                    bg="#212963",
                    color="white",
                    _hover={"bg": "blue.600"},
                    width = '80%',
                ),
                width = '100%',
            ),
            width='97%',
            grid_template_columns="2fr 5fr 2fr",
        ),
    )
