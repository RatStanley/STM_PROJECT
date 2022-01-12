from tkinter import *

root = Tk()
root.title("calculator")

num_var = 0
pr_var = 0
op_type = "none"
display = Label(root, text=num_var, font=("Arial", 25))
display.grid(row=0, column=0, columnspan=3)
# display.config(text="nowy")

def disp_var(number):
    global display
    display.config(text=number)


def clicked_number(number):
    global num_var
    num_var = num_var * 10 + number
    disp_var(num_var)


def operation(operation_type):
    global num_var
    global pr_var
    global op_type



    if operation_type == "eq":
        if op_type == "add":
            num_var = num_var + pr_var
        elif op_type == "sub":
            num_var = pr_var - num_var
    elif operation_type == "clear":
        num_var = 0
        pr_var = 0
    else:
        op_type = operation_type
        print(op_type)
        pr_var = num_var
        num_var = 0
    disp_var(num_var)


button_1 = Button(root, text=1, command=lambda: clicked_number(1), padx=40, pady=40)
button_2 = Button(root, text=2, command=lambda: clicked_number(2), padx=40, pady=40)
button_3 = Button(root, text=3, command=lambda: clicked_number(3), padx=40, pady=40)
button_4 = Button(root, text=4, command=lambda: clicked_number(4), padx=40, pady=40)
button_5 = Button(root, text=5, command=lambda: clicked_number(5), padx=40, pady=40)
button_6 = Button(root, text=6, command=lambda: clicked_number(6), padx=40, pady=40)
button_7 = Button(root, text=7, command=lambda: clicked_number(7), padx=40, pady=40)
button_8 = Button(root, text=8, command=lambda: clicked_number(8), padx=40, pady=40)
button_9 = Button(root, text=9, command=lambda: clicked_number(9), padx=40, pady=40)
button_0 = Button(root, text=0, command=lambda: clicked_number(0), padx=40, pady=40)
button_add = Button(root, text="+", command=lambda: operation("add"), padx=40, pady=40)
button_sub = Button(root, text="-", command=lambda: operation("sub"), padx=40, pady=40)
button_clear = Button(root, text="C", command=lambda: operation("clear"), padx=40, pady=40)

button_eq = Button(root, text="=", command=lambda: operation("eq"), padx=80, pady=40)


button_1.grid(row=1, column=0)
button_2.grid(row=1, column=1)
button_3.grid(row=1, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=3, column=0)
button_8.grid(row=3, column=1)
button_9.grid(row=3, column=2)
button_0.grid(row=4, column=1)
button_add.grid(row=1, column=3)
button_eq.grid(row=4, column=2, columnspan=2)
button_sub.grid(row=2, column=3)
button_clear.grid(row=4, column=0)

root.mainloop()
