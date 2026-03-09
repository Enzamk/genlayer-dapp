# { "Depends": "py-genlayer:test" }
from genlayer import *

class MyApp(IContract):
    message: str

    def __init__(self, initial_message: str) -> None:
        self.message = initial_message

    @gl.public.view
    def get_message(self) -> str:
        return self.message

    @gl.public.write
    def set_message(self, new_message: str) -> None:
        self.message = new_message
