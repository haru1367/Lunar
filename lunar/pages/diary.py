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
            rx.container(
                rx.text(HomeState.search_calendar),
            ),
            align_items="left",
            gap=4,
        ),
        py=4,
        overflow='auto',
    )

def saved_video(video):
    return rx.vstack(
        rx.hstack(
            rx.video(
                url = video.video_url,
                width = '150px',
                height= '100px',
            ),
            rx.button(
                f'{video.video_title[:20] + "..."}',
                style={'white-space': 'normal'},
                align='start',
                max_width='200px',
                height='100px',
                on_click = HomeState.popup_video(video.video_url,video.video_title),
            ),
            rx.alert_dialog(
                rx.alert_dialog_overlay(
                    rx.alert_dialog_content(
                        rx.alert_dialog_header("Video"),
                        rx.alert_dialog_body(
                            rx.video(
                                url = HomeState.popup_video_url,
                                width = '700px',
                                height= '500px',
                            ),
                            rx.heading(
                                HomeState.popup_video_title,
                                Font_size='20px',
                            )
                        ),
                        rx.alert_dialog_footer(
                            rx.button(
                                "Close",
                                on_click=HomeState.popup_video(video.video_url,video.video_title),
                            )
                        ),
                    ),
                ),
                size = '3xl',
                is_open=HomeState.show,
            ),
        ),
        rx.button(
            'Save cancel',
            width='100%',
            border_radius = '20px',
            bg = '#ecf065',
            _hover={'bg':'orange.400'},
            on_click = HomeState.remove_video_playlist(video.video_url)
        ),
        rx.container(height='5px'),
        max_width='100%',
    )

# 오른쪽에 표시되는 사이드바
def sidebar(HomeState):
    """The sidebar displayed on the right."""
    return rx.vstack(
        rx.heading('Saved video',Font_size='25px',Font_weight='border',bg = 'green.400'),
        rx.vstack(
            rx.cond(
                HomeState.saved_video_results,
                rx.foreach(
                    HomeState.saved_video_results,
                    saved_video
                ),
                rx.vstack(
                    rx.button(
                        rx.icon(
                            tag="repeat",
                            mr=1,
                        ),
                        rx.text("load",Font_size = '20px',),
                        on_click=HomeState.get_saved_video,
                    ),
                    p=4,
                ),
            ),
        ),
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

def daylist(daylist):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(daylist.split(':')[0]),
                    rx.text(daylist.split(':')[1]),
                    width='20%',
                ),           
                rx.button(
                    rx.text('hello'),
                    width='75%',
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
