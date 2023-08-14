import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser
from PIL import Image, ImageTk
import requests
from io import BytesIO
import giphy_client
from giphy_client.rest import ApiException

# Initialize GIPHY client
api_instance = giphy_client.DefaultApi()
API_KEY = 'LWoWtvGY30VXXMlN5ScXo2YnKSRDkDnI'  # Replace this with your GIPHY API key

def search_giphy(tag, limit=10):
    try:
        response = api_instance.gifs_search_get(API_KEY, tag, limit=limit)
        return [x.images.original.url for x in response.data]
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return []

def fetch_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def create_gui():
    window = tk.Tk()
    window.title("M3m3 Generator")

    def search_meme_template():
        tag = simpledialog.askstring("Search", "Enter meme template tag:")
        if tag:
            urls = search_giphy(tag)
            if urls:
                # For simplicity, we'll just fetch the first meme template
                # In a more advanced version, you can provide a gallery for the user to choose from
                img = fetch_image(urls[0])
                img.thumbnail((300, 300))
                img_tk = ImageTk.PhotoImage(img)
                preview_label.config(image=img_tk)
                preview_label.image = img_tk

    search_button = tk.Button(window, text="Search Meme Template", command=search_meme_template)
    search_button.pack(pady=20)

    preview_label = tk.Label(window)
    preview_label.pack(pady=20)

    window.mainloop()

create_gui()
