from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import serial
import serial.tools.list_ports
import sys
import glob

style.use('ggplot')
root = Tk()
root.title("Image")
root.iconbitmap('img/he.ico')

USART_MODE = "Asynchronous"
USART_BAUD_RATE = IntVar()
USART_BAUD_RATE.set(115200)
USART_WORD_LENGTH = IntVar()
USART_WORD_LENGTH.set(8)
USART_PARITY = StringVar()
USART_PARITY.set('None')
USART_STOP_BITS = IntVar()
USART_STOP_BITS.set(1)
USART_PORT = StringVar()

entry_value = Entry(root, width=50, textvariable="0")
entry_value.insert(0, "0")
entry_value.grid(row=0, column=0)

# a = np.arange(1, 5, 1)
data_array = np.array([], dtype=float)

fig = Figure(figsize=(5, 4), dpi=100)
to_animate = fig.add_subplot(111)  # .plot(data_array, data_array)
to_animate.plot(data_array, data_array)
t = np.array([])


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


available_ports = serial_ports()
USART_PORT.set(available_ports[0])


def refresh_ports():
    global available_ports
    available_ports = serial_ports()


def config_menu():
    menu = Toplevel()
    menu.title("UART config")
    menu.iconbitmap('img/he.ico')
    global USART_BAUD_RATE
    global USART_WORD_LENGTH
    global USART_PARITY
    global USART_STOP_BITS
    global USART_PORT
    BAUD_RATE = [
        ("600", 600),
        ("1200", 1200),
        ("2400", 2400),
        ("4800", 4800),
        ("9600", 9600),
        ("14400", 14400),
        ("19200", 19200),
        ("28800", 28800),
        ("38400", 38400),
        ("56000", 56000),
        ("57600", 57600),
        ("115200", 115200),
        ("128000", 128000),
        ("256000", 256000)
    ]
    WORD_LENGTHS = [
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8)
    ]
    PARITY = [
        ("none", "none"),
        ("odd", "odd"),
        ("even", "even"),
        ("mark", "mark"),
        ("space", "space")
    ]
    STOP_BITS = [
        ("1", 1),
        ("1.5", 1.5),
        ("2", 2)
    ]

    Baud_Rate_frame = LabelFrame(menu, text="Baud Rate :", padx=10, pady=10)
    Word_length_frame = LabelFrame(menu, text="Word Length :", padx=10, pady=23)
    Parity_frame = LabelFrame(menu, text="Parity :", padx=10, pady=10)
    Stop_bits_frame = LabelFrame(menu, text="Stop bits :", padx=10, pady=30)
    iter_x = 0
    iter_y = 0
    for text, mode in BAUD_RATE:
        Radiobutton(Baud_Rate_frame, text=text, variable=USART_BAUD_RATE, value=mode).grid(row=iter_x, column=iter_y,
                                                                                           sticky=W)
        if iter_x < 4:
            iter_x = iter_x + 1
        else:
            iter_x = 0
            iter_y = iter_y + 1
    iter_x = 0
    iter_y = 0
    for text, mode in WORD_LENGTHS:
        Radiobutton(Word_length_frame, text=text, variable=USART_WORD_LENGTH, value=mode).grid(row=iter_x,
                                                                                               column=iter_y, sticky=W)
        iter_x = iter_x + 1
    iter_x = 0
    for text, mode in PARITY:
        Radiobutton(Parity_frame, text=text, variable=USART_PARITY, value=mode).grid(row=iter_x, column=iter_y,
                                                                                     sticky=W)
        iter_x = iter_x + 1
    iter_x = 0
    for text, mode in STOP_BITS:
        Radiobutton(Stop_bits_frame, text=text, variable=USART_STOP_BITS, value=mode).grid(row=iter_x, column=iter_y,
                                                                                           sticky=W)
        iter_x = iter_x + 1

    Baud_Rate_frame.grid(row=0, column=0, sticky=W + E + S + N)
    Word_length_frame.grid(row=0, column=1, sticky=W + E + S + N)
    Parity_frame.grid(row=0, column=2, sticky=W + E + S + N)
    Stop_bits_frame.grid(row=0, column=3, sticky=W + E + S + N)

    port = OptionMenu(menu, USART_PORT, *available_ports)
    port.grid(row=1, column=0, sticky=W)
    Save_Exit_button = Button(menu, text="Save and Exit", command=menu.destroy)
    refresh = Button(menu, text="Refresh the port list", command=refresh_ports)

    Save_Exit_button.grid(row=1, column=3, sticky=W + E, pady=10)
    refresh.grid(row=1, column=2)


def animate_fig(i):
    global data_array
    global t
    data_array = np.append(data_array, float(entry_value.get()))
    t = np.append(t, int(len(t - 1) + 1))
    to_animate.clear()
    to_animate.plot(t, data_array)


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=3, rowspan=2)

ani = animation.FuncAnimation(fig, animate_fig, interval=1000)

Config_button = Button(root, text="USART Configuration", command=config_menu)  # , padx=40, pady=40)
Start_Stop_button = Button(root, text="USART Configuration", command=config_menu)

Config_button.grid(row=2, column=2)

root.mainloop()
