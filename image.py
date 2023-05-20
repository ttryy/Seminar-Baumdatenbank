import tkinter as tk

from PIL import ImageTk, Image


class ImageShow:

    def __init__(self, tkroot, image):
        root = tk.Toplevel(tkroot)
        self.root = root
        root.title("Bild")
        width = 500
        height = 500
        root.geometry(f'{width}x{height}')
        root.resizable(False, False)

        self.image_label = tk.Label(root)
        self.image_label.place(x=0, y=0, width=width, height=height)

        self.load_image(image, width, height)

    def load_image(self, image, width, height):
        thumbnail_image = image.copy()
        thumbnail_image = self.scale_image(thumbnail_image, width, height)
        photo = ImageTk.PhotoImage(thumbnail_image)
        self.image_label["image"] = photo
        self.image_label.image = photo

    def scale_image(self, image, width, height):
        width_ratio = width / image.width
        height_ratio = height / image.height

        scale_factor = min(width_ratio, height_ratio)

        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        scaled_img = image.resize((new_width, new_height), Image.ANTIALIAS)

        return scaled_img