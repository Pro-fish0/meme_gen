import tkinter as tk
from tkinter import filedialog, colorchooser
import cv2
import numpy as np
from PIL import Image, ImageTk

def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and cv2.getTextSize(line + words[0], font[0], font[1], font[2])[0][0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def generate_meme(image, top_text, bottom_text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, font_thickness=2, font_color=(255, 255, 255)):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert image to BGR format for OpenCV

    top_lines = wrap_text(top_text, (font, font_scale, font_thickness), image.shape[1])
    bottom_lines = wrap_text(bottom_text, (font, font_scale, font_thickness), image.shape[1])

    y = 0
    for line in top_lines:
        (width, height), _ = cv2.getTextSize(line, font, font_scale, font_thickness)
        cv2.putText(image, line, ((image.shape[1] - width) // 2, y + height), font, font_scale, font_color, font_thickness)
        y += height

    y = image.shape[0]
    for line in bottom_lines:
        (width, height), _ = cv2.getTextSize(line, font, font_scale, font_thickness)
        cv2.putText(image, line, ((image.shape[1] - width) // 2, y), font, font_scale, font_color, font_thickness)
        y -= height

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert back to RGB format

image_dict = {
    'original': None,
    'tkinter': None
}

def create_gui():
    window = tk.Tk()
    window.title("Meme Generator")

    global font_color
    font_color = (255, 255, 255)

    def open_image():
        file_path = filedialog.askopenfilename()
        if file_path:
            img = cv2.imread(file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for PIL compatibility
            pil_img = Image.fromarray(img)
            pil_img.thumbnail((300, 300))
            image_dict['original'] = np.array(pil_img)
            img_tk = ImageTk.PhotoImage(pil_img)
            image_dict['tkinter'] = img_tk
            preview_label.config(image=img_tk)

    def pick_color():
        global font_color
        chosen_color = colorchooser.askcolor()[1]
        if chosen_color:
            font_color = tuple(int(chosen_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    def generate():
        top_text = top_text_entry.get()
        bottom_text = bottom_text_entry.get()
        meme = generate_meme(image_dict['original'].copy(), top_text, bottom_text, font_color=font_color)
        pil_img = Image.fromarray(meme)
        img_tk = ImageTk.PhotoImage(pil_img)
        image_dict['tkinter'] = img_tk
        image_dict['original'] = meme
        preview_label.config(image=img_tk)

    def save_meme():
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(image_dict['original'], cv2.COLOR_RGB2BGR))

    open_button = tk.Button(window, text="Open Image", command=open_image)
    open_button.pack(pady=20)

    top_text_entry = tk.Entry(window, width=40)
    top_text_entry.pack(pady=20)
    top_text_entry.insert(0, "Top Text")

    bottom_text_entry = tk.Entry(window, width=40)
    bottom_text_entry.pack(pady=20)
    bottom_text_entry.insert(0, "Bottom Text")

    color_button = tk.Button(window, text="Pick Font Color", command=pick_color)
    color_button.pack(pady=10)

    generate_button = tk.Button(window, text="Generate Meme", command=generate)
    generate_button.pack(pady=20)

    save_button = tk.Button(window, text="Save Meme", command=save_meme)
    save_button.pack(pady=20)

    preview_label = tk.Label(window)
    preview_label.pack(pady=20)

    window.mainloop()

create_gui()
