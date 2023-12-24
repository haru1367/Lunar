# lunar.state.home 모듈에서 필요한 State 및 HomeState를 가져옵니다.
import reflex as rx
from lunar.state.base import State
from lunar.state.home import HomeState

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

def hotplace(hotplace):
    return rx.box(
        rx.button(
            f'{hotplace.search_place}',
            width='250px',
            bg = '#9debf5',
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
            rx.hstack(
                rx.container(width='5px'),
                rx.vstack(
                    rx.container(height='10px'),
                    rx.hstack(
                        rx.button('Hot place!(24H)',Font_size = '20px',on_click = HomeState.hotplaces,bg = '#ebf564'),
                    ),
                    rx.container(height='5px'),
                    rx.foreach(
                        HomeState.map_hotplaces,
                        hotplace,
                    ),
                    rx.container(height='4px'),
                    width ='100%',
                    align_items='start',
                ),
                border = '3px solid #000000',
                border_radius = '30px',
            ),
            rx.button(
                "Sign out",
                on_click=State.logout,
                bg="#212963",
                color="white",
                _hover={"bg": "blue.600"},
            ),
            rx.container(height='200px'),
            align_items="left",
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
                    bg="#d1895c",
                    color="white",
                    _hover={"bg": "orange.600"},
                ),
                align_items='left',
                width='100%',
            ),
            rx.container(height='30px'),
            border_bottom = '3px solid #000000',
        ),
        rx.vstack(
            rx.text('Route search result',font_size='30px'),
            rx.text(HomeState.distance,font_size = '25px'),
            rx.text(HomeState.path_time,font_size ='25px'),
            rx.text(HomeState.taxi_fee, font_size = '20px'),
            rx.text(HomeState.toll_fee, font_size = '20px'),
            align_items='start',
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
        rx.input(on_change=HomeState.set_map_search_input, placeholder="Search place..!"),
        rx.button('search', on_click = HomeState.map_search),
        rx.button('clear',on_click = HomeState.map_clear),
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        rx.html(HomeState.time_map_iframe),
        rx.box(
            rx.data_table(
                data=HomeState.df,
                font_size = '8px',
                width='100%',
            ),
        ),
        border_x = '3px solid #000000',
        overflow='auto',
    )

# 홈 페이지
def map():
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
            border_bottome='3px solid #000000',
        ),
        rx.hstack(
            tab_button('/Home.png','/'),
            tab_button('/profile.png','/profile'),
            tab_button('/map.png','/map'),
            tab_button('/chat.png','/chat'),
            tab_button('/Aichat.png','/aichat'),
            tab_button('/diary.png','/diary'),
            tab_button('/video.png','/video'),
            tab_button('/game.png','/game'),
            tab_button('/setting.png','/setting'),
            margin_right='5px',
            border="1px solid #000000",
            border_radius="full",
        ),
        width='100%',
    )
