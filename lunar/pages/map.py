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
    )

# 오른쪽에 표시되는 사이드바
def sidebar(HomeState):
    """The sidebar displayed on the right."""
    return rx.vstack(
        rx.hstack(
            rx.image(src='/find2.png',height='35px',width='35px'),
            rx.input(
                on_change=HomeState.set_friend,
                placeholder="Search users",  # 사용자 검색을 위한 입력 상자
                width="100%",
                border = "3px solid #000000",
            ),
        ),
        rx.container(height='10px'),
        rx.foreach(
            HomeState.search_users,
            lambda user: rx.vstack(
                rx.hstack(
                    rx.avatar(name=user.username, size="sm"),  # 검색된 사용자의 아바타 이미지
                    rx.text(user.username),  # 검색된 사용자의 사용자 이름
                    rx.spacer(),
                    rx.button(
                        rx.icon(tag="add"),
                        on_click=lambda: HomeState.follow_user(user.username),  # 사용자를 팔로우하는 버튼
                    ),
                    width="100%",
                ),
                py=2,
                width="100%",
            ),
        ),
        align_items="start",
        gap=4,
        h="100%",
        py=4,
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
        rx.data_table(
            data=HomeState.df,
            font_size = '8px',
        ),
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
