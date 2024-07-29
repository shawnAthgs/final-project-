import os
import requests
import io
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_images():
    user_prompt = prompt_entry.get("0.0", tkinter.END).strip()
    user_prompt += " in style: " + style_dropdown.get()

    response = client.images.generate(prompt=user_prompt, n=int(number_slider.get()), size="512x512")
    
    image_urls = [data.url for data in response.data]
    images = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)

    def update_image(index=0):
        canvas.image = images[index]
        canvas.create_image(0, 0, anchor="nw", image=images[index])
        index = (index + 1) % len(images)
        canvas.after(3000, update_image, index)

    update_image()

def generate_silly_joke():
    prompt = "Please generate 1 silly joke phrase."
    language = language_dropdown.get()
    prompt += " the generated message should be answered sarcasticly. " + language + ". "
    difficulty = difficulty_value.get()
    prompt += " The difficulty is " + difficulty + ". "
    if checkbox1.get():
        prompt += " The project should include a database."
    if checkbox2.get():
        prompt += " The project should include an API."

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content
    result.insert("0.0", answer)

root = ctk.CTk()
root.geometry("1200x700")
root.title("AI Generator")

ctk.set_appearance_mode("dark")

# Title
title_label = ctk.CTkLabel(root, text="AI Generator", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(padx=10, pady=(20, 20))

# Tabs
tab_view = ctk.CTkTabview(root, width=1200, height=600)
tab_view.pack(expand=True, fill="both", padx=10, pady=10)

# Image Generation Tab
image_tab = tab_view.add("Image Generation")
image_frame = ctk.CTkFrame(image_tab)
image_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(image_frame, text="Prompt")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(image_frame, height=10)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

style_label = ctk.CTkLabel(image_frame, text="Style")
style_label.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(image_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

number_label = ctk.CTkLabel(image_frame, text="# Images")
number_label.grid(row=2, column=0)
number_slider = ctk.CTkSlider(image_frame, from_=1, to=10, number_of_steps=9)
number_slider.grid(row=2, column=1)

generate_button = ctk.CTkButton(image_frame, text="Generate", command=generate_images)
generate_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

canvas = tkinter.Canvas(image_tab, width=512, height=512)
canvas.pack(side="right")

# Project Idea Generation Tab
project_tab = tab_view.add("Project Ideas")
project_frame = ctk.CTkFrame(project_tab)
project_frame.pack(fill="x", padx=100)

language_frame = ctk.CTkFrame(project_frame)
language_frame.pack(padx=100, pady=(20, 5), fill="both")

language_label = ctk.CTkLabel(language_frame, text="Programming Language", font=ctk.CTkFont(weight="bold"))
language_label.pack()

language_dropdown = ctk.CTkComboBox(language_frame, values=["Python", "Java", "C++", "JavaScript", "Golang"])
language_dropdown.pack(pady=10)

difficulty_frame = ctk.CTkFrame(project_frame)
difficulty_frame.pack(padx=100, pady=5, fill="both")

difficulty_label = ctk.CTkLabel(difficulty_frame, text="Project Difficulty", font=ctk.CTkFont(weight="bold"))
difficulty_label.pack()

difficulty_value = ctk.StringVar(value="Easy")
radiobutton1 = ctk.CTkRadioButton(difficulty_frame, text="Easy", variable=difficulty_value, value="Easy")
radiobutton1.pack(side="left", padx=(20, 10), pady=10)

radiobutton2 = ctk.CTkRadioButton(difficulty_frame, text="Medium", variable=difficulty_value, value="Medium")
radiobutton2.pack(side="left", padx=(20, 10), pady=10)

radiobutton3 = ctk.CTkRadioButton(difficulty_frame, text="Hard", variable=difficulty_value, value="Hard")
radiobutton3.pack(side="left", padx=(20, 10), pady=10)

features_frame = ctk.CTkFrame(project_frame)
features_frame.pack(padx=100, pady=5, fill="both")

features_label = ctk.CTkLabel(features_frame, text="Features", font=ctk.CTkFont(weight="bold"))
features_label.pack()

checkbox1 = ctk.CTkCheckBox(features_frame, text="Database")
checkbox1.pack(side="left", padx=50, pady=10)

checkbox2 = ctk.CTkCheckBox(features_frame, text="API")
checkbox2.pack(side="left", padx=50, pady=10)

generate_ideas_button = ctk.CTkButton(project_frame, text="Generate Ideas", command=generate_silly_joke)
generate_ideas_button.pack(padx=100, fill="x", pady=(5, 20))

result = ctk.CTkTextbox(project_tab, font=ctk.CTkFont(size=15))
result.pack(pady=10, fill="x", padx=100)

root.mainloop()
