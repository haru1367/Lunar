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
            rx.vstack(
                rx.container(
                    rx.hstack(
                        rx.image(src='/human.png',height='40px',width='40px'),
                        rx.text(
                            'Recommended freinds',
                            style={
                                'fontSize':'25px',
                                'fontWeight':'bolder',
                                'fontFamily':'Calibri, Calibri',
                                "background": "-webkit-linear-gradient(-45deg, #8ea6e6, #ad3ce6)",
                                '-webkit-background-clip':'text',
                                'color':'transparent',
                            },
                        ),
                    ),
                    rx.container(height='10px'),
                    rx.vstack(
                        rx.container(height='200px'),
                        border = '2px solid #000000',
                        border_radius='30px',
                    ),
                ),
                align_items='start',
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
        rx.input(on_change=HomeState.set_search, placeholder="Search contents"),  # 콘텐츠 검색을 위한 입력 상자
        justify="space-between",
        p=4,
        border_bottom="3px solid #000000",
    )

# 새로운 게시물을 작성하는 컴포저
def composer(HomeState):
    """The composer for new craters."""
    return rx.vstack(
        rx.container(height='5px'),
        rx.vstack(
            rx.hstack(
                rx.avatar(size="md"),  # 사용자의 아바타 이미지
                rx.container(width='30px'),
                rx.text_area(
                    value=HomeState.crater,
                    w='100%',
                    border=2,
                    placeholder="What's happening?",  # 트윗을 작성하는 입력 상자
                    resize="none",
                    py=4,
                    px=0,
                    _focus={"border": 0, "outline": 0, "boxShadow": "none"},
                    on_change=HomeState.set_crater,
                ),
                width='95%',
                margin_left = '30px',
            ),
            rx.hstack(
                rx.button(
                    rx.image(src='/fileselect.png',height='35px',width='35px'),
                    on_click=HomeState.handle_file_selection,
                    border_radius = '1em',
                ),
                rx.button(
                    rx.image(src='/selectcancel.png',height='35px',width='35px'),
                    on_click=HomeState.file_select_cancel,
                    border_radius = '1em',
                ),
                rx.button(
                    rx.image(src='/write.png',height='30px',width='30px'),
                    on_click= HomeState.post_crater,
                    border_radius="1em",
                ),  # 트윗을 게시하는 버튼
                justify_content="flex-end",
                px=4,
                py=2,
                width='100%',
            ),
            rx.modal(
                rx.modal_overlay(
                    rx.modal_content(
                        rx.modal_header("File upload"),
                        rx.modal_body(
                            rx.responsive_grid(
                                rx.foreach(
                                    HomeState.img,
                                    lambda img: rx.vstack(
                                        rx.image(src=img),
                                        rx.text(img),
                                    ),
                                ),
                                columns=[2],
                                spacing="5px",
                            ),
                        ),
                        rx.modal_footer(
                            rx.button(
                                "Confirm", on_click=HomeState.change
                            ),
                            rx.button(
                                "Cancel",
                                on_click=HomeState.file_select_cancel,
                                border_radius="1em",
                                box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                                background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                                box_sizing="border-box",
                                color="white",
                                opacity="0.6",
                                _hover={"opacity": 1},
                            ),
                        ),
                    )
                ),
                is_open=HomeState.imgshow,
            ),
            rx.responsive_grid(
                rx.foreach(
                    HomeState.img,
                    lambda img: rx.vstack(
                        rx.text(img),
                    ),
                ),
                columns=[2],
                spacing="5px",
            ),
            margin_left='5px',
            width='97%',
            border_radius='20px',
            border="3px solid #000000",
        ),
    )


# 개별 트윗을 표시하는 함수
def crater(crater):
    image_tags = rx.cond(
        crater.image_content,
        rx.foreach(
            crater.image_content.split(", "),
            lambda image: rx.image(src=f"/{image}", alt="crater image",max_width = '500px')
        ),
        rx.box()  # 이미지가 없는 경우 빈 리스트를 반환합니다.
    ),

    return rx.vstack(
        rx.hstack(
            rx.avatar(name=crater.author, size="md"),  # 트윗 작성자의 아바타 이미지
            rx.text("@" + crater.author, font_weight="bold",fontSize = '20px'),  # 트윗 작성자의 사용자 이름
            rx.text("["+ crater.created_at +"]"),
        ),
        rx.hstack(
            rx.container(width='50px'),
            rx.box(
                *image_tags,
                rx.container(height='5px'),
                rx.text(crater.content, width="100%",fontSize = '15px'),  # 트윗 내용
                rx.container(height='10px'),
                width = '100%',
            ),
            py=4,
            gap=1,
            width='98%',
        ),
        rx.container(height='5px'),
        margin_left = '25px',
        align_items='start',
        width='auto',
    )

# 피드 영역
def feed(HomeState):
    """The feed."""
    return rx.box(
        feed_header(HomeState),
        composer(HomeState),
        rx.container(height='10px'),
        rx.cond(
            HomeState.craters,
            rx.foreach(
                HomeState.craters,
                crater
            ),
            rx.vstack(
                rx.button(
                    rx.icon(
                        tag="repeat",
                        mr=1,
                    ),
                    rx.text("Click to load story"),
                    on_click=HomeState.get_craters,
                ),  # 트윗을 불러오는 버튼
                p=4,
            ),
        ),
        h="100%",
        border_x = '3px solid #000000',
        overflow = 'auto',
    )

# 홈 페이지
def home():
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
