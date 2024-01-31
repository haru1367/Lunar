"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
from .pages import home, login, signup, findpassword, findid, map, video,music,weather,diary,aichat,chat
from .state.base import State

app = rx.App(state=State)
app.add_page(login)
app.add_page(signup)
app.add_page(findpassword)
app.add_page(findid)
app.add_page(map,on_load=State.check_login())
app.add_page(video,on_load=State.check_login())
app.add_page(music,on_load=State.check_login())
app.add_page(weather,on_load=State.check_login())
app.add_page(diary,on_load = State.check_login())
app.add_page(aichat,on_load = State.check_login())
app.add_page(chat,on_load = State.check_login())
app.add_page(home, route="/", on_load=State.check_login())
app.compile()
