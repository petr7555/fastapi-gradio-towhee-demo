"""
How to launch Gradio app within another FastAPI app.

Run this from the terminal as you would normally start a FastAPI app:
`poetry run uvicorn fastapi_gradio:app --reload`
and navigate to http://localhost:8000/gradio in your browser to see the Gradio app.
"""
import gradio as gr
from fastapi import FastAPI

CUSTOM_PATH = "/gradio"

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "This is your main app"}


io = gr.Interface(lambda name: "Hello, " + name + "!", "textbox", "textbox")
gradio_app = gr.routes.App.create_app(io)

app.mount(CUSTOM_PATH, gradio_app)
