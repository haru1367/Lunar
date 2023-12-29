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
        rx.button('search', on_click = HomeState.get_youtube_links),
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

def get_video(video):
    result = video.split(',')
    return rx.box(
        rx.vstack(
            rx.video(
                url = result[1],
                width = '100%',
                height = '500px',
                playing = False,
                loop = True,
            ),
            rx.hstack(
                rx.heading(result[0],Font_size = '25px'),
                rx.spacer(),
                rx.button(
                    'Save',
                    on_click = HomeState.add_video_playlist(result[1],result[0]),
                    border_radius = '1em',
                    bg = '#95de98',
                    _hover={"bg": "blue.400"},
                ),
                width='100%',
                align_items='start',
            ),
            rx.container(height='10px'),
            width = '100%'
        ),
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        rx.foreach(
            HomeState.youtube_results,
            get_video,
        ),
        border_x = '3px solid #000000',
        overflow='auto',
    )

# 홈 페이지
def video():
    State.check_login
    return rx.vstack(
        rx.grid(
            tabs(),
            feed(HomeState),
            sidebar(HomeState),
            grid_template_columns="2fr 5fr 2fr",
            border_bottom = '3px solid #000000',
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
