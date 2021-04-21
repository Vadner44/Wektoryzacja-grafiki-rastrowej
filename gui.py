from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk
from main import *
import cv2
from pathlib import Path


root = Tk()


def wybierz():
    filename = filedialog.askopenfilenames(parent=root, initialdir="/", title="Obrazki",
                                           filetypes=[("PNG, JPEG, BMP", "*.png; *jpg; *jpeg; *.bmp")])

    try:
        clear = 255 * np.ones((300, 300), dtype=np.uint8)
        clear = Image.fromarray(clear)
        clear = clear.resize((300, 300), Image.ANTIALIAS)
        clear = ImageTk.PhotoImage(clear)
        clear = Label(image=clear)
        clear.image = clear
        clear.place(x=320, y=250)
        image = Image.open(filename[0])
        image = image.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        img = Label(image=render)
        img.image = render
        img.place(x=10, y=250)
        global file
        file = filename[0]
    except IndexError:
        messagebox.showinfo("", "Nie wybrano obrazka")


def wektoryzacja():
    try:
        zmienna1 = int(e1.get())
        zmienna2 = float(e2.get())
        image = cv2.imread(file)
        nazwa = Path(file).resolve().stem
        folder = os.path.dirname(file)
        run(image, zmienna1, zmienna2, folder, nazwa)
        wynik = Image.open(folder + '/wektoryzacja/' + nazwa + '.png')
        image = wynik.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        img = Label(image=render)
        img.image = render
        img.place(x=320, y=250)
    except NameError:
        messagebox.showwarning("", "Nie wybrano obrazka")


root.title('')
root.geometry("635x565")
root.resizable(width=False, height=False)
root.iconbitmap('img/v.ico')
root.config(background="black")

A = 255 * np.ones((300, 300), dtype=np.uint8)
im = Image.fromarray(A)
im = im.resize((300, 300), Image.ANTIALIAS)
im2 = ImageTk.PhotoImage(im)
im3 = Label(image=im2)
im3.image = im2
im3.place(x=10, y=250)

im22 = ImageTk.PhotoImage(im)
im4 = Label(image=im2)
im4.image = im2
im4.place(x=320, y=250)

tytul = Label(root, text="Algorytm wektoryzacji", width=80, height=2, fg="blue",
              background="white", font=("Ariel", 10, "bold"))
button_wybierz = Button(root, text="Wybierz obrazek", border=3, command=wybierz)
button_wektoryzacja = Button(root, text="Wektoryzacja", border=3, command=wektoryzacja)
l1 = Label(root, text="Rozmycie gaussowskie:", fg="white", background="black")
e1 = Entry(root, width=6)
e1.insert(END, '3')
l2 = Label(root, text="Dolny próg:", fg="white", background="black")
e2 = Entry(root, width=6)
e2.insert(END, '0.12')
tytul.place(x=0, y=0)
l1.place(x=380, y=80)
e1.place(x=510, y=80)
l2.place(x=380, y=105)
e2.place(x=510, y=105)
button_wektoryzacja.place(x=430, y=150)
button_wybierz.place(x=115, y=125)
root.mainloop()
