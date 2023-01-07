import os
import cv2
import tkinter as Tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Find import Find


algorithm = {
    1: Find.with_sliding,
    2: Find.with_dichotomic,
}


selected = False
img1 = []
img2 = []


def error_modal():
    messagebox.showerror("Erreur", "Vous devez remplir tout les champs")


def compress():
    if len(img1) > 0 and len(img2) > 0 and img1.shape == img2.shape:
        if search_value.get() == 2:
            Find.with_dichotomic(img1, img2, thresh_value.get(
            ), bs=bloc_value.get(), DELTA=padding_value.get())
        else:
            Find.with_sliding(img1, img2, thresh_value.get(), dx=dxdy_value.get(
            ), dy=dxdy_value.get(), bs=bloc_value.get(), DELTA=padding_value.get())
    else:
        error_modal()


def show_image():
    global selected
    global img1
    global img2

    fln = filedialog.askopenfilename(
        initialdir=os.getcwd(), title="Selectionnez une image", filetypes=[('Images', '*.jpg *.jpeg *.png')])
    img = Image.open(fln)
    img.thumbnail((300, 400))
    img = ImageTk.PhotoImage(img)
    if selected:
        img2 = cv2.imread(fln)
        label_image_two.configure(image=img)
        label_image_two.image = img
    else:
        img1 = cv2.imread(fln)
        label_image.configure(image=img)
        label_image.image = img

    selected = True


# ---------------------------- FENETRE
window = Tk.Tk()
window.title("MPEG Encoder")
window.geometry("900x800")
window.minsize(800, 600)


thresh_value = Tk.IntVar()
thresh_value.set(1)
search_value = Tk.IntVar()
search_value.set(1)
padding_value = Tk.IntVar()
padding_value.set(0)
dxdy_value = Tk.IntVar()
dxdy_value.set(5)
bloc_value = Tk.IntVar()
bloc_value.set(8)

# ---------------------------- CADRE
image_frame = Tk.LabelFrame(
    window, text="Importations d'images", width=750, height=200, borderwidth=1)

search_frame = Tk.LabelFrame(
    window, text="Méthodes de recherche", width=750, height=200, borderwidth=1)

option_frame = Tk.LabelFrame(
    window, text="Paramètres de recherche", width=750, height=200, borderwidth=1)

button_frame = Tk.Frame(window, width=750, height=200, borderwidth=1)

# ---------------------------- IMAGES

image_one = Tk.PhotoImage(file="images\Image072.png")
image_two = Tk.PhotoImage(file="images\Image092.png")

# ---------------------------- LABEL
label_welcome = Tk.Label(window, text="Bienvenue sur MPEG Encoder")
label_image = Tk.Label(image_frame)
label_image_two = Tk.Label(image_frame)
label_seuil = Tk.Label(option_frame, text="Seuil : ")
label_padding = Tk.Label(option_frame, text="Padding : ")
label_block = Tk.Label(option_frame, text="Taille blocs : ")
label_deltaXY = Tk.Label(
    option_frame, text="Vecteur dx/dy : ")

# ---------------------------- SCALE
range_thresh = Tk.Scale(option_frame, from_=1, to=100,
                        tickinterval=10, orient="horizontal", length=300, variable=thresh_value)
range_padding = Tk.Scale(option_frame, from_=0, to=128,
                         tickinterval=16, orient="horizontal", length=300, variable=padding_value)
range_block = Tk.Scale(option_frame, from_=8, to=512,
                       tickinterval=64, orient="horizontal", length=300, variable=bloc_value)
range_deltaXY = Tk.Scale(option_frame, from_=5, to=15,
                         tickinterval=1, orient="horizontal", length=300, variable=dxdy_value)


# ---------------------------- RADIO BUTTONS
radio_slide = Tk.Radiobutton(
    search_frame, text="Linéaire", value=1, variable=search_value)
radio_dicho = Tk.Radiobutton(
    search_frame, text="Logarithmique", value=2, variable=search_value)

# ---------------------------- BASIC BUTTONS
button_quit = Tk.Button(button_frame, text="Quitter", width=20, command=exit)
button_launch = Tk.Button(
    button_frame, text="Compresser", width=20, command=compress)
button_browse = Tk.Button(image_frame, text="Parcourir",
                          width=20, command=show_image)

# ---------------------------- COMPILING

label_welcome.pack()
image_frame.pack(padx=20, pady=20, fill="x")
button_browse.pack(side="top")
label_image.pack(side="left", padx=70, pady=20)
label_image_two.pack(side="right", padx=70, pady=20)

search_frame.pack(padx=20, pady=20, fill="x")
radio_slide.pack()
radio_dicho.pack()

option_frame.pack(padx=20, pady=20, fill="x")

label_seuil.grid(column=0, row=0, padx=10)
range_thresh.grid(column=1, row=0, columnspan=10)

label_padding.grid(column=0, row=1, padx=10)
range_padding.grid(column=1, row=1)

label_block.grid(column=0, row=2, padx=10)
range_block.grid(column=1, row=2)

label_deltaXY.grid(column=0, row=3, padx=10)
range_deltaXY.grid(column=1, row=3)

button_frame.pack(padx=20, pady=20, side="bottom")
button_launch.pack(side="left", padx=20)
button_quit.pack(side="right", padx=20)

window.mainloop()
