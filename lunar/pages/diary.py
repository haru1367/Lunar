# lunar.state.home 모듈에서 필요한 State 및 HomeState를 가져옵니다.
import reflex as rx
from lunar.state.base import State
from lunar.state.home import HomeState
from datetime import datetime

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

def ddaylist(ddaylist):
    return rx.box(
        rx.vstack(
            rx.heading(ddaylist.dday, font_Size = '20px', font_weight='bold',margin_left = '10px',bg='blue.300'),
            rx.flex(
                rx.center(
                    rx.text(ddaylist.dday_content, font_Size='15px',font_weight='bold',margin_left='10px'),
                ),
                rx.spacer(),
                rx.center(
                    rx.button(
                        rx.icon(tag='close',size='sm'),
                        on_click = HomeState.remove_ddaylist(ddaylist.dday, ddaylist.dday_content),
                        border_radius='20px',
                    ),
                ),
                width='100%',
            ),
            width='90%',
            border = '2px solid #000000',
            border_radius ='20px',
            align_items='start',
        ),
        rx.container(height='10px'),
        width='100%',
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
                rx.button(
                    rx.heading(
                        "D-day",
                        font_Size = '30px',
                        font_weight = 'bolder',
                    ),
                    color = '#db5942',
                    on_click = HomeState.get_ddaylist,
                ),
                rx.vstack(
                    rx.foreach(
                        HomeState.ddaylist,
                        ddaylist,  
                    ),
                    rx.vstack(
                        rx.container(height='10px'),
                        rx.hstack(
                            rx.input(placeholder='year',on_change=HomeState.set_dday_year),
                            rx.input(placeholder='month',on_change=HomeState.set_dday_month),
                            rx.input(placeholder='day',on_change=HomeState.set_dday_day),
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder = 'add content..',
                                on_change = HomeState.set_dday_content,
                            ),
                            rx.button(
                                rx.icon(tag='add',size = 'sm'),
                                on_click = HomeState.add_ddaylist
                            ),
                        ),
                        rx.container(height='10px'),
                        width='90%',
                        align_items='start',
                    ),
                    align_items='start',
                    width='100%',
                ),
                width='100%',
                align_items='start',
            ),
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
        align_items="start",
        gap=4,
        h="100%",
        max_width = '100%',
        py=4,
        overflow='auto',
    )

# 피드의 헤더
def feed_header(HomeState):
    """The header of the feed."""
    return rx.hstack(
        rx.image(src='/find1.png',height='35px',width='35px'),
        rx.input(on_change=HomeState.set_search_video, placeholder="video search..!"),
        rx.button('search', on_click = HomeState.print_calendar),
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

def recorded(recorded):
    return rx.box(
        rx.vstack(
            rx.text_area(
                value=recorded.memo,
                w='100%',
                border=2,
                placeholder="Add memo!", 
                resize="none",
                py=4,
                px=0,
                _focus={"border": 0, "outline": 0, "boxShadow": "none"},
            ),
            width='100%',
            align_items='start',
            border='3px solid #000000',
        ),
        rx.container(height='10px'),
    )

def daylist(daylist):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(daylist.split(':')[0],color = '#5fa9de',font_Size='20px',font_weight='bold'),
                    rx.text(daylist.split(':')[1],font_Size='20px',font_weight='bold'),
                    width='20%',
                ),
                rx.box(           
                    rx.button(
                        rx.text('hello'),
                        width='95%',
                        on_click=HomeState.memo_change(daylist),
                    ),
                    rx.modal(
                        rx.modal_content(
                            rx.modal_header(
                                rx.heading(
                                    HomeState.popup_day,
                                    color = '#5fa9de',
                                    font_Size='20px',
                                    font_weight='bold',
                                ),
                            ),
                            rx.modal_body(
                                rx.foreach(
                                    HomeState.recorded_memo,
                                    recorded,
                                ),
                                rx.text_area(
                                    value=HomeState.memo_content,
                                    w='100%',
                                    border=2,
                                    placeholder="Add memo!",  # 트윗을 작성하는 입력 상자
                                    resize="none",
                                    py=4,
                                    px=0,
                                    _focus={"border": 0, "outline": 0, "boxShadow": "none"},
                                    on_change=HomeState.set_memo_content,
                                ),
                            ),
                            rx.modal_footer(
                                rx.button(
                                    'Save', on_click = HomeState.add_memo(daylist)
                                ),
                                rx.button(
                                    "Close", on_click=HomeState.memo_change(daylist)
                                ),
                            ),
                        ),
                        size = '3xl',
                        is_open=HomeState.memo_show,
                    ),
                    width='100%',
                ),
                width='100%',
                height='auto',
            ),
            align_items='start',
            width='100%',
            border='2px solid #000000',
            border_radius='20px',
        ),
        rx.container(height='5px'),
        width='100%',
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        rx.flex(
            rx.center(
                rx.heading(
                    f'{HomeState.year}.{HomeState.month}',
                    font_Size = '65px',
                    font_weight='bolder',
                    color = '#bd5757',
                ),
            ),
            rx.spacer(),
            rx.center(
                rx.heading(
                    HomeState.search_month,
                    font_Size = '50px',
                    font_weight='bolder',
                    color = '#665d5d',
                ),
            ),
        ),
        rx.vstack(
            rx.foreach(
                HomeState.daylist,
                daylist,
            )
        ),
        width = '100%',
        overflow = 'auto',
    )

# 홈 페이지
def diary():
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
