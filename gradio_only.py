import gradio as gr
from gradio.components import Textbox


def greet(name):
    return "Hello " + name + "!"


demo = gr.Interface(
    fn=greet,
    inputs=Textbox(placeholder="Type your name here..."),
    outputs=Textbox()
)

if __name__ == "__main__":
    demo.launch()
