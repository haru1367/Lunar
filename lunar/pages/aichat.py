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
                    'conversation notes',
                    font_Size='25px',
                    font_Weight='bold',
                    color = '#42d647',
                ),
                align_items='start',
            ),
            rx.button(
                rx.text('Delete all conversations',font_weight='bold',font_Size = '20px'),
                on_click = HomeState.clear_gpt,
                bg = 'red.300',
            ),
            width = '90%',
        ),
        py=4,
        overflow = 'auto',
    )

def gpt(gpt):
    box_color = rx.cond(gpt.author == "Gemini", "#b2d5eb", "#f5ec76")
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.container(width='2px'),
                    rx.avatar(name=gpt.author, size="sm"), 
                ),
                rx.box(
                    rx.hstack(
                        rx.text("@" + gpt.author, font_weight="bold"),
                        rx.text("["+ gpt.created_at +"]"),  
                    ),
                    rx.text(gpt.content, width="auto"),  
                    width = 'auto',
                ),
                py=4,
                gap=1,
                width='auto',
            ),
            align_items='start',
            width = '97%',
            margin_left='5px',
            border_radius='20px',
            border = '2px solid #000000',
            background=box_color,
        ),
        rx.container(height='5px'),
        margin_left='10px',
        align_items='start',
        width='auto',
    )
                
def feed_header(HomeState):
    return rx.box(
        rx.vstack(
            rx.container(height='10px'),
            rx.hstack(
                rx.image(src = '/chattingai.png',height='100%',width='80px'),
                rx.text_area(
                    value=HomeState.user_input_chat,
                    w='100%',
                    border=2,
                    placeholder="Talk to Gemini!",  # 트윗을 작성하는 입력 상자
                    resize="none",
                    py=4,
                    px=0,
                    _focus={"border": 0, "outline": 0, "boxShadow": "none"},
                    on_change=HomeState.set_user_input_chat,
                ),
                rx.button(
                    rx.image(src = '/aichatload.png',height='100%',width='100%'),
                    on_click = HomeState.get_gpt,
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={"opacity": 1},
                ),
                rx.button(
                    rx.image(src = '/aimessagesend.png',height='100%',width='100%'),
                    on_click = HomeState.chatai,
                    border_radius="1em",
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    box_sizing="border-box",
                    color="white",
                    opacity="0.6",
                    _hover={"opacity": 1},
                ),
                justify="space-between",
                p=4,
                width = '97%',
                border_radius = '20px',
                border = '2px solid #000000',
                box_shadow = '10px 10px 5px #706666',
                align_items='start',
            ),
            rx.container(height='10px'),
        ),
    )

# 피드 영역
def feed(HomeState):
    return rx.box(
        rx.container(height='10px'),
        feed_header(HomeState),
        rx.cond(
            HomeState.aichatting,
            rx.foreach(
                HomeState.aichatting,
                gpt
            ),
        ),
        h="100%",
        overflow='auto'
    )

# 홈 페이지
def aichat():
    State.check_login
    return rx.vstack(
        rx.grid(
            tabs(),
            feed(HomeState),
            grid_template_columns="2fr 7fr",

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
