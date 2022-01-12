from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Image")
root.iconbitmap('img/he.ico')

addres_list = ['img/one.png', 'img/2.jpg', 'img/3.jpg', 'img/4.jpg']

MyImage1 = ImageTk.PhotoImage(Image.open(addres_list[0]))
MyImage2 = ImageTk.PhotoImage(Image.open(addres_list[1]))
MyImage3 = ImageTk.PhotoImage(Image.open(addres_list[2]))
MyImage4 = ImageTk.PhotoImage(Image.open(addres_list[3]))

ImgList = [MyImage1, MyImage2, MyImage3, MyImage4]
curr_id = 0
currentPhoto = Label(image=ImgList[0])
currentPhoto.grid(row=0, column=0, columnspan=3)


def next_img(dir):
    global currentPhoto
    global ImgList
    global curr_id
    if dir == "next":
        if curr_id < len(ImgList)-1:
            curr_id = curr_id + 1
            currentPhoto.config(image=ImgList[curr_id])
    elif dir == "back":
        if curr_id > 0:
            curr_id = curr_id - 1
            currentPhoto.config(image=ImgList[curr_id])



# button_1 = Button(root, text=1, command=lambda: clicked_number(1), padx=40, pady=40)

next_button = Button(root, text=">>", command=lambda: next_img("next"))
next_back = Button(root, text="<<", command=lambda: next_img("back"))

next_button.grid(row=1, column=2)
next_back.grid(row=1, column=0)
root.mainloop()
