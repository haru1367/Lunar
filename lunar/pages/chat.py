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
        rx.container(height='30px'),
        rx.vstack(
            rx.vstack(
                rx.text(
                    'Friend list',
                    font_Size='25px',
                    font_Weight='bold',
                    color = '#e0a353',
                ),
                rx.vstack(
                    rx.container(height='10px'),
                    rx.vstack(
                        rx.foreach(
                            HomeState.following,
                            lambda follow: rx.vstack(
                                rx.button(
                                    rx.vstack(
                                        rx.text(follow.followed_username),  # 팔로잉 중인 사용자의 사용자 이름
                                        width = '100%',
                                        align_items='start',
                                    ),
                                    on_click = HomeState.get_messages(follow.followed_username),
                                    width = '100%',
                                ),
                                width = '100%',
                                padding="1em",
                            ),
                        ),
                        border = '2px solid #000000',
                        border_radius = '20px',
                        box_shadow = '10px 10px 10px #76adde',
                        width = '100%',
                    ),
                    rx.container(height='10px'),
                    width='90%',
                    align_items='start',
                ),
                width = '100%',
                align_items='start',
            ),
            rx.container(height='10px'),
            align_items='start',
            width = '100%',
        ),
        py=4,
        overflow = 'auto',
    )

def sidebar():
    return rx.box(
        rx.container(height = '20px'),
        rx.text(
            'Open chat list',
            font_Size = '25px',
            font_weight='bolder',
            color = '#d19330',
        ),
        rx.vstack(
            rx.container(height='400px'),
            overflow='auto',
            border = '2px solid #000000',
            border_radius = '20px',
        ),
        rx.container(height='50px'),
        rx.text(
            'Participating rooms',
            font_Size = '25px',
            font_weight='bolder',
            color = '#2ee67a',
        ),
        rx.vstack(
            rx.container(height='30px'),
            border = '2px solid #000000',
            border_radius = '20px',
        ),
        py=4,
        overflow='auto',
    )

def message(message):
    box_color = rx.cond(message.send_user == HomeState.user.username, "#f3f7b7","#9dc6eb")
    align_direction = rx.cond(message.send_user== HomeState.user.username,"end","start")
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.container(width='2px'),
                    rx.avatar(name=message.send_user, size="sm"), 
                ),
                rx.box(
                    rx.hstack(
                        rx.text("@" + message.send_user, font_weight="bold"),  
                        rx.text("["+ message.created_at +"]"),
                    ),
                    rx.text(message.message, width="auto"), 
                    width = 'auto',
                ),
                rx.container(width = '2px'),
                py=4,
                gap=1,
                width='auto',
            ),
            border = '2px solid #000000', 
            border_radius='20px',
            background=box_color,
        ),
        rx.container(height='5px'),
        align_items=align_direction,
        width='100%',
    )

# 피드 영역
def feed(HomeState):
    return rx.box(
        rx.container(height='10px'),
        rx.text(
            HomeState.receive_user,
            font_Size = '25px',
            font_weight='bolder',
        ),
        rx.vstack(
            rx.vstack(
                rx.cond(
                    HomeState.messages,
                    rx.foreach(
                        HomeState.messages,
                        message
                    ),
                ),
                height='90%',
                width = '100%',
                overflow='auto',
            ),
            rx.hstack(
                rx.input(
                    on_blur=HomeState.set_kakaotalk,
                    placeholder="Write Message!",
                    border = '2px solid #000000',
                    border_radius = '10px',
                    width ='95%',
                ),
                rx.button(
                    rx.image(
                        src = '/dm.png',
                        height='auto',
                        width='auto',
                    ),
                    on_click = HomeState.sending_message,
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={"opacity": 1},
                    width ='5%',
                ),
                width = '100%',
            ),
            height='90%',
            align_items='start',
        ),
        h="100%",
        overflow='auto'
    )

# 홈 페이지
def chat():
    State.check_login
    return rx.vstack(
        rx.grid(
            tabs(),
            feed(HomeState),
            sidebar(),
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
