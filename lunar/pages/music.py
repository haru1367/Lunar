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

def music_chart(chart):
    return rx.box(
        rx.button(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        f"{chart['rank']}",
                        font_Size = '20px',
                        font_weight='border',
                    ),
                ),
                rx.container(width = '5px'),
                rx.vstack(
                    rx.text(
                        f"{chart['title']}",
                        # style={'white-space': 'normal'},
                        font_weight='border',
                        font_Size='20px',
                        overflow='hidden',
                    ),
                    rx.text(
                        f"{chart['artist']}",
                        font_Size='15px',
                        overflow='hidden',
                    ),
                    align_items='start',
                ),
                width='215px',
                height='auto',
                justify_content='flex-start',
                overflow='hidden',
            ),
            height='auto',
        ),
        rx.container(height='5px'),
        align='start',
        padding='2px',  # 테두리와 내용 사이의 여백 지정
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
                        rx.hstack(
                            rx.button('Music chart 100!',Font_size = '20px',on_click = HomeState.music_chart,bg = '#7ad65e'),
                        ),
                        rx.container(height='5px'),
                        rx.foreach(
                            HomeState.music_chart_info,
                            music_chart,
                        ),
                        width ='100%',
                        align_items='start',
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
        rx.input(on_change=HomeState.set_search_music, placeholder="Search music..!"),
        rx.button('search', on_click = HomeState.map_search),
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
        ),
        rx.container(height='20px'),
        overflow='auto',
    )

# 홈 페이지
def music():
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
