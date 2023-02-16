"""
How to launch Gradio app within another FastAPI app.

Run this from the terminal as you would normally start a FastAPI app:
`poetry run uvicorn fastapi_gradio:app --reload`
and navigate to http://localhost:8000/gradio in your browser to see the Gradio app.
"""
from fastapi import FastAPI
import gradio as gr

CUSTOM_PATH = "/gradio"

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "This is your main app"}


io = gr.Interface(lambda name: "Hello, " + name + "!", "textbox", "textbox")
app = gr.mount_gradio_app(app, io, path=CUSTOM_PATH)
