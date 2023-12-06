"""Login page. Uses auth_layout to render UI shared with the sign up page."""
import reflex as rx

from lunar.state.auth import AuthState

def signup():
    return rx.container(
        rx.container(height='100px'),
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
                                    "fontFamily": "Comic Sans MS, Cursive",
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
                rx.container(height='40px'),
                rx.image(
                    src = '/space2.jpg',
                ),
                width = '500px',
                height= '100%',
            ),
            rx.container(width='30px'),
            rx.vstack(
                rx.container(height='20px'),
                rx.container(
                    rx.hstack(
                        rx.input(placeholder="Nickname", on_blur=AuthState.set_username),
                        rx.button(
                            "Check",
                            on_click=AuthState.id_check,
                            bg="#212963",
                            color="white",
                            _hover={"bg": "blue.600"},
                        ),
                    ),
                    rx.container(height='16px'),
                    rx.form_control(
                        rx.input(
                            placeholder="password",
                            on_blur=AuthState.set_password,
                            type_='password',
                        ),
                        rx.cond(
                            AuthState.time_valid_password,
                            rx.form_error_message(
                                "The password must be 8 to 16 characters containing a combination of numbers and alphabets."
                            ),
                            rx.form_helper_text("password is valid"),
                        ),
                        is_invalid=AuthState.time_valid_password,
                        is_required=True,
                    ),
                    rx.container(height='16px'),
                    rx.form_control(
                        rx.input(
                            placeholder="password",
                            on_blur=AuthState.set_confirm_password,
                            type_='password',
                        ),
                        rx.cond(
                            AuthState.time_valid_confirm_password,
                            rx.form_error_message(
                                "Please check your password again."
                            ),
                            rx.form_helper_text("The passwords match."),
                        ),
                        is_invalid=AuthState.time_valid_confirm_password,
                        is_required=True,
                    ),
                    rx.container(height='16px'),
                    rx.form_control(
                        rx.input(
                            placeholder="your name",
                            on_blur=AuthState.set_user_realname,
                        ),
                        rx.cond(
                            AuthState.time_valid_username,
                            rx.form_error_message(
                                "The name must be between 2 and 20 characters."
                            ),
                            rx.form_helper_text("name is valid"),
                        ),
                        is_invalid=AuthState.time_valid_username,
                        is_required=True,
                    ),
                    rx.container(height='16px'),
                    rx.form_control(
                        rx.input(
                            placeholder="your email address",
                            on_blur=AuthState.set_user_email_address,
                        ),
                        rx.cond(
                            AuthState.time_valid_email_address,
                            rx.form_error_message(
                                "Please enter correct email."
                            ),
                            rx.form_helper_text("check"),
                        ),
                        is_invalid=AuthState.time_valid_email_address,
                        is_required=True,
                    ),
                    rx.container(height='16px'),
                    rx.hstack(
                        rx.select(
                            AuthState.year,
                            placeholder="birth year",
                            on_change=AuthState.set_user_birthday_year,
                            color_schemes="twitter",
                        ),
                        rx.select(
                            AuthState.month,
                            placeholder="birth month",
                            on_change=AuthState.set_user_birthday_month,
                            color_schemes="twitter",
                        ),
                        rx.select(
                            AuthState.day,
                            placeholder="birth day",
                            on_change=AuthState.set_user_birthday_day,
                            color_schemes="twitter",
                        ),
                    ),
                    rx.vstack(
                        rx.container(height='20px'),
                        rx.button(
                            "Sign up",
                            on_click=AuthState.signup,
                            bg="#212963",
                            color="white",
                            _hover={"bg": "blue.600"},
                        ),
                        center_content=True,
                        align_items="left",
                        bg="white",
                        max_width="400px",
                        border_radius="20px",
                        background= 'rgb(255,255,255,0.7)'
                    ),
                    align_items="left",
                    bg="white",
                    border="1px solid #eaeaea",
                    p=4,
                    max_width="400px",
                    border_radius="lg",
                ),
                rx.text(
                    "Already have an account? ",
                    rx.link("Sign in here.", href="/", color="blue.500"),
                    color="gray.600",
                ),
                rx.container(height='10px'),
                width='500px',
                height='auto',
                center_content=True,
                borderRadius='40px',
                boxShadow='10px 10px 100px #79d0ed',
                background= 'rgb(255,255,255,0.7)'
            ),
        ),
        center_content=True,
        justify_content=True,
        maxWidth='auto',
        maxHeight='auto',
        height='100vh',
    )
