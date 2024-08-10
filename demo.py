import numpy as np
import pandas as pd
import gradio as gr
import os
from PIL import Image
import json


def image_generator(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory_path, filename)
            image = Image.open(image_path)
            image_array = np.array(image)
            yield filename, image_array


directory_path = "/home/maulik/Documents/data/PETA/images/"
directory_path = "data/"
label_dict_path = "label_dict.json"
label_dict = {}  # mapping filename to label
# Create the generator

image_gen = image_generator(directory_path)

def save_label_dict():
    with open(label_dict_path, "w") as f:
        json.dump(label_dict, f)

def record_input(fname: str, gen_label: str, age_label: str, view_label: str):
    if gen_label and age_label and view_label:
        label_dict[fname] = {
            "gender": gen_label,
            "age": age_label,
            "view": view_label,
        }
        save_label_dict()
    # try:    
    fname, image = next(image_gen)
    print(fname)
    # except StopIteration:
    #     fname = "No more images"
    #     image = None
    return fname, image


def start():       
    fname, image = next(image_gen)
    while label_dict.get(fname) is not None:
        fname, image = next(image_gen)    
    return fname, image


with gr.Blocks() as demo:
    start_btn = gr.Button("Start")
    with gr.Column():        
        img_block = gr.Image(visible=True, width=300, height=300)
        
    file_name = gr.Textbox(info="File name", visible=True)
    checkbox_labels = ["Male", "Female", "Pass"]
    
    with gr.Row():        
        gen = gr.CheckboxGroup(["Male", "Female"], label="Gender")
        age = gr.Slider(0, 100, value=25, label="Age")
        view = gr.CheckboxGroup(["Front", "Side", "Back"], label="View")
    
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=record_input, 
                     inputs=[file_name, gen, age, view], 
                     outputs=[file_name, img_block])
    start_btn.click(fn=start, outputs=[file_name, img_block])
demo.queue()
demo.launch(share=False, debug=True)
