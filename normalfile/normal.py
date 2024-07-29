import os
import requests
import io
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_images():
    user_prompt = prompt_entry.get("1.0", tk.END).strip()
    user_prompt += " in style: " + style_dropdown.get()

    response = openai.Image.create(prompt=user_prompt, n=int(number_slider.get()), size="512x512")

    image_urls = [data['url'] for data in response['data']]
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

def generate_silly_answer():
    question = silly_question_entry.get("1.0", tk.END).strip()
    silliness = int(silliness_slider.get())
    prompt = f"Answer this question in a silly manner (silliness level: {silliness}): {question}"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    result.insert("1.0", answer)

root = ctk.CTk()
root.geometry("1200x700")
root.title("AI Generator")

# Set appearance mode
ctk.set_appearance_mode("dark")

# Set root window background color
root.configure(bg="#2C2C2C")

# Title
title_label = ctk.CTkLabel(root, text="AI Generator", font=ctk.CTkFont(size=30, weight="bold"), text_color="#FFFFFF", bg_color="#2C2C2C")
title_label.pack(padx=10, pady=(20, 20))

# Tabs
tab_view = ctk.CTkTabview(root, width=1200, height=600, bg_color="#2C2C2C")
tab_view.pack(expand=True, fill="both", padx=10, pady=10)

# Image Generation Tab
image_tab = tab_view.add("Image Generation")
image_frame = ctk.CTkFrame(image_tab, bg_color="#2C2C2C")
image_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(image_frame, text="Prompt", text_color="#FFD700", bg_color="#2C2C2C")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(image_frame, height=10, fg_color="#333333", text_color="#FFFFFF", bg_color="#2C2C2C")
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

style_label = ctk.CTkLabel(image_frame, text="Style", text_color="#FFD700", bg_color="#2C2C2C")
style_label.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(image_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"], fg_color="#333333", text_color="#FFFFFF", button_color="#FFD700", bg_color="#2C2C2C")
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

number_label = ctk.CTkLabel(image_frame, text="# Images", text_color="#FFD700", bg_color="#2C2C2C")
number_label.grid(row=2, column=0)
number_slider = ctk.CTkSlider(image_frame, from_=1, to=10, number_of_steps=9, fg_color="#FFD700", progress_color="#FFD700", bg_color="#2C2C2C")
number_slider.grid(row=2, column=1)

generate_button = ctk.CTkButton(image_frame, text="Generate", command=generate_images, fg_color="#3B5998", hover_color="#8B9DC3", text_color="#FFFFFF", bg_color="#2C2C2C")
generate_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

canvas = tk.Canvas(image_tab, width=512, height=512, bg="black")
canvas.pack(side="right")

# Silly Question Answer Tab
silly_tab = tab_view.add("Silly Question Answer")
silly_frame = ctk.CTkFrame(silly_tab, bg_color="#2C2C2C")
silly_frame.pack(fill="x", padx=100)

silly_question_label = ctk.CTkLabel(silly_frame, text="Enter your silly question", font=ctk.CTkFont(weight="bold"), text_color="#FFD700", bg_color="#2C2C2C")
silly_question_label.pack()

silly_question_entry = ctk.CTkTextbox(silly_frame, height=10, fg_color="#333333", text_color="#FFFFFF", bg_color="#2C2C2C")
silly_question_entry.pack(pady=10)

silliness_label = ctk.CTkLabel(silly_frame, text="Silliness Level", font=ctk.CTkFont(weight="bold"), text_color="#FFD700", bg_color="#2C2C2C")
silliness_label.pack()

silliness_slider = ctk.CTkSlider(silly_frame, from_=1, to=10, number_of_steps=9, fg_color="#FFD700", progress_color="#FFD700", bg_color="#2C2C2C")
silliness_slider.pack(pady=10)

generate_silly_answer_button = ctk.CTkButton(silly_frame, text="Generate Answer", command=generate_silly_answer, fg_color="#3B5998", hover_color="#8B9DC3", text_color="#FFFFFF", bg_color="#2C2C2C")
generate_silly_answer_button.pack(pady=10)

result = ctk.CTkTextbox(silly_tab, font=ctk.CTkFont(size=15), fg_color="#333333", text_color="#FFFFFF", bg_color="#2C2C2C")
result.pack(pady=10, fill="x", padx=100)

root.mainloop()

