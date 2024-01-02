"""Login page. Uses auth_layout to render UI shared with the sign up page."""
import reflex as rx

from lunar.state.auth import AuthState

def login():
    return rx.container(
        rx.container(height='150px'),
        rx.hstack( 
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.container(height='20px'),
                        rx.image(
                            src = "/moonico.ico",
                            width="70px",
                            height="70px",
                        ),
                    ),              
                    rx.vstack(           
                        rx.container(height='8px'),
                        rx.container(
                            rx.text(
                                "Lunar",
                                style={
                                    "fontSize": "50px",
                                    "fontWeight": "bolder",
                                    "letterSpacing": "3px",
                                    "background": "-webkit-linear-gradient(-45deg, #e04a3f, #24d6d6)",
                                    "-webkit-background-clip": "text",
                                    "color": "black",
                                },
                                mb=-3,
                            ),
                            rx.text(
                                "Share your daily life with people!",
                                style={
                                    'background': "-webkit-linear-gradient(-45deg, #e04a3f, #4e8be6)",
                                    'background_clip': "text",  # 텍스트에만 그라데이션 적용
                                    'color': "transparent",  # 텍스트 색상을 투명으로 설정
                                    'font_weight': "bold",
                                    'fontSize':'20px',
                                },
                            ),
                        ),

                    ),
                ),
                rx.container(height='20px'),
                rx.container(
                    rx.vstack(
                        rx.container(
                            rx.input(placeholder="Nickname", on_blur=AuthState.set_username, mb=4),
                            rx.input(
                                type_="password",
                                placeholder="Password",
                                on_blur=AuthState.set_password,
                                mb=4,
                            ),
                            rx.button(
                                "Log in",
                                on_click=AuthState.login,
                                bg="#212963",
                                color="white",
                                _hover={"bg": "blue.600"},
                            ),
                            center_content=True,
                            align_items="left",
                            bg="white",
                            border="1px solid #eaeaea",
                            p=4,
                            max_width="400px",
                            border_radius="20px",
                            background= 'rgb(255,255,255,0.7)'
                        ),
                        rx.container(height='10px'),
                        rx.hstack(
                            rx.container(width='20px'),
                            rx.vstack(
                                rx.text(
                                    'Forgot your id?     ',
                                    rx.link('Find Id!',href="/findid",color='red.500'),
                                    color='gray.600', 
                                ),
                                rx.text(
                                    'Forgot your password?     ',
                                    rx.link('Find Password!',href="/findpassword",color='green.500'),
                                    color="gray.600",
                                ), 
                                rx.text(
                                    "Don't have an account yet?     ",
                                    rx.link("Sign up!", href="/signup", color="blue.500"),
                                    color="gray.600",
                                ),
                                align_items='start',
                            ),
                        ),
                        rx.container(height='30px') ,
                        align_items='start',  
                    ),
                ),
                width='500px',
                height='auto',
                center_content=True,
                borderRadius='30px',
                # boxShadow='10px 10px 100px #79d0ed',
                background= 'rgb(255,255,255,0.7)'
            ),
        ),
        center_content=True,
        # justifyContent='center',
        maxWidth='auto',
        maxHeight='auto',
        height='100vh',
        background_image = '/deepspace1.gif',
        background_size = 'cover',
        # background_repeat = 'no-repeat',
        # style={
        #     'background-image':"url('/space2.jpg')",
        #     'background-size':'cover',
        # }
    )
