from tkinter import *
# from PIL import ImageTk, Image
import numpy as np
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import serial
import serial.tools.list_ports
from serial import SerialException

import sys
import glob
from numpy import savetxt
import time


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


def refresh_ports():
    global available_ports
    available_ports = serial_ports()


def config_menu():
    menu = Toplevel()
    menu.title("UART config")
    menu.iconbitmap('img/icon.ico')
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
        ("none", "N"),
        ("odd", "O"),
        ("even", "E"),
        ("mark", "M"),
        ("space", "S")
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

    if len(available_ports) != 0:
        port = OptionMenu(menu, USART_PORT, *available_ports)
        port.grid(row=1, column=0, sticky=W)
    Save_Exit_button = Button(menu, text="Save and Exit", command=menu.destroy)
    refresh = Button(menu, text="Refresh the port list", command=refresh_ports)

    Save_Exit_button.grid(row=1, column=3, sticky=W + E, pady=10)
    refresh.grid(row=1, column=2)

# temp_1 = 0
def animate_fig(i):
    global data_array
    global time_array
    global start_stop_bool
    global USART
    global itera
    global USART_to_show
    # global  temp_1
    if start_stop_bool == 1:
        if USART.isOpen():
            USART_read_value = USART.readline()
            USART_read_value = USART_read_value.decode('windows-1250')
            USART_variable = USART_read_value.split(",")
            try:
                # UART_Data_2.config(text=USART_read_value)
                # if not USART_read_value == '':
                if not len(USART_variable) < 2:
                    data_array = np.append(data_array, float(USART_variable[0]))
                    # time_array = np.append(time_array, float(USART_read_value[1])/1000)
                    if len(time_array) != 0:
                        # time_array = np.append(time_array, float(USART_variable[1]) / 1000)
                        time_array = np.append(time_array, time_array[-1] + float(USART_variable[1]) / 1000)
                        # time_array = np.append(time_array, float(time_array[-1] + 0.1))
                        # print(float(USART_variable[1]))
                    else:
                        time_array = np.append(time_array, float(USART_variable[1])/1000)

                    USART_to_show[7] = USART_to_show[6]
                    USART_to_show[6] = USART_to_show[5]
                    USART_to_show[5] = USART_to_show[4]
                    USART_to_show[4] = USART_to_show[3]
                    USART_to_show[3] = USART_to_show[2]
                    USART_to_show[2] = USART_to_show[1]
                    USART_to_show[1] = USART_to_show[0]
                    USART_to_show[0] = USART_variable[0] + "        " + str(time_array[-1])
                    UART_Data_8.config(text=USART_to_show[7])
                    UART_Data_7.config(text=USART_to_show[6])
                    UART_Data_6.config(text=USART_to_show[5])
                    UART_Data_5.config(text=USART_to_show[4])
                    UART_Data_4.config(text=USART_to_show[3])
                    UART_Data_3.config(text=USART_to_show[2])
                    UART_Data_2.config(text=USART_to_show[1])
                    UART_Data_1.config(text=USART_to_show[0])
                    # temp_1 = temp_1 + 0.025
                    fig_plot_animation.clear()
                    fig_plot_animation.plot(time_array, data_array)
                    Temp_var.config(text=data_array[len(data_array) - 1])
            except ValueError:
                USART_to_show[0] = 'Data could not be read, possible wrong configuration'
                UART_Data_1.config(text='Data could not be read, possible wrong configuration')
                USART_to_show[1] = USART_variable


def start_stop_conection():
    global start_stop_bool
    global animated_plot
    global USART
    global USART_MODE
    global USART_BAUD_RATE
    global USART_WORD_LENGTH
    global USART_PARITY
    global USART_STOP_BITS
    global USART_PORT
    global USART_to_show
    if start_stop_bool == 0:
        Start_Stop_button.config(text="Stop")
        animated_plot.event_source.start()
        start_stop_bool = 1
        Config_button.config(state=DISABLED)
        try:
            USART = serial.Serial(port=USART_PORT.get(), baudrate=USART_BAUD_RATE.get(),
                                  bytesize=USART_WORD_LENGTH.get(),
                                  parity=USART_PARITY.get(), stopbits=USART_STOP_BITS.get(), timeout=1)
        except serial.SerialException:
            # print("No connection to the device could be established")
            USART_to_show[0] = "No connection to the device could be established"
            start_stop_bool = 0
    elif start_stop_bool == 1:
        Start_Stop_button.config(text="Start")
        start_stop_bool = 0
        animated_plot.event_source.stop()
        Config_button.config(state=NORMAL)
        USART.close()


def save_data_from_plot(file_name):
    global data_array
    global time_array
    data = np.array([data_array, time_array]).transpose()
    savetxt(file_name + '.csv', data, delimiter=',')


def save_window_():
    save_window = Toplevel()
    save_window.title("Save")
    save_window.iconbitmap('img/icon.ico')
    save_window.geometry("230x50")
    enter_file_name = Entry(save_window, width=20, textvariable="File Name", font=("Arial", 10))
    Save_button_top = Button(save_window, text="Save",
                             command=lambda: [save_data_from_plot(enter_file_name.get()), save_window.destroy()])
    label = Label(save_window, text="File Name :", font=("Arial", 10))
    label.grid(row=0, column=0)
    enter_file_name.grid(row=0, column=1)
    Save_button_top.grid(row=1, column=0, columnspan=2)


def clear_plot_and_data():
    global data_array
    global time_array
    global USART_to_show
    data_array = np.array([])
    time_array = np.array([])
    fig_plot_animation.clear()
    canvas.draw()

    # canvas.get_tk_widget().grid(row=0, column=4, columnspan=4, rowspan=3)
    Temp_var.config(text=0)
    UART_Data_8.config(text='')
    UART_Data_7.config(text='')
    UART_Data_6.config(text='')
    UART_Data_5.config(text='')
    UART_Data_4.config(text='')
    UART_Data_3.config(text='')
    UART_Data_2.config(text='')
    UART_Data_1.config(text='')

    USART_to_show = ["", "", "", "", "", "", "", ""]



def send_var():
    global USART
    global Var_to_submit
    global USART_to_show
    string_to_submit = ""
    try:

        string_to_submit = str(float(Var_to_submit.get())) + "e"
        for i in range(5):
            if len(string_to_submit) < 7:
                string_to_submit = string_to_submit + "e"
            else:
                break
        # print(string_to_submit)

        USART.write(string_to_submit.encode())
    except ValueError:
        USART_to_show[0] = "input not a number"

    # USART.write(str(Var_to_submit.get()).encode())


# PODSTAWOWE PARAMETRY DO GUI
root = Tk()
root.title("Serial Plot Temperature")
root.iconbitmap('img/icon.ico')

# INICJOWANIE I SETOWANIE DOMYŚLNYCH WARTOŚCI KOMUNIKACJI UART I INNYCH ZMIENNYCH
USART_MODE = "Asynchronous"
USART_BAUD_RATE = IntVar()
USART_WORD_LENGTH = IntVar()
USART_PARITY = StringVar()
USART_STOP_BITS = IntVar()
USART_PORT = StringVar()

USART_BAUD_RATE.set(115200)
USART_WORD_LENGTH.set(8)
USART_PARITY.set('N')
USART_STOP_BITS.set(1)
temperature = 0
start_stop_bool = 0
fontsize = 15
USART_to_show = ["", "", "", "", "", "", "", ""]
itera = 0
available_ports = serial_ports()

# USART = serial
# print(serial.STOPBITS_ONE)
# print(serial.STOPBITS_ONE_POINT_FIVE)
# print(serial.PARITY_EVEN)
# print(serial.PARITY_MARK)
# print(serial.PARITY_SPACE)


if len(available_ports) == 0:
    USART_PORT.set("no COM")
else:
    USART_PORT.set(available_ports[0])
USART = serial.Serial

# WYŚWIETLENIE WYKRESÓW I INICJALIZACJA WEKTORÓW DANYCH
style.use('ggplot')
data_array = np.array([], dtype=float)
time_array = np.array([], dtype=float)
fig = Figure(figsize=(5, 4), dpi=100)
fig_plot_animation = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
animated_plot = animation.FuncAnimation(fig, animate_fig, interval=25)
fig.suptitle("Odpowiedź układu")
fig.supxlabel("t [s]")
fig.supylabel("Temperatura")

# WYŚWIETLENIE AKTUALNEJ TEMPERATURY
Temp_label = Label(root, text="Temperatura : ", font=("Arial", fontsize))
if not len(data_array) == 0:
    Temp_var = Label(root, text=data_array[0], font=("Arial", fontsize))  # ,relief=SUNKEN)
else:
    Temp_var = Label(root, text=0, font=("Arial", fontsize))  # ,relief=SUNKEN)
# ZADAWANIE WYBRANEJ TEMPERATURY
Var_to_submit_label = Label(root, text="Zadana temperatury : ", font=("Arial", fontsize))
Var_to_submit = Entry(root, textvariable="0", font=("Arial", fontsize), width=10)
Var_to_submit.insert(0, "0")
Submit_var_button = Button(root, text="Wyślij", command=send_var)

# KOMUNIAKCJA UART
frame = LabelFrame(root, text="USART", relief=SUNKEN, bg='white')
UART_Data_1 = Label(frame, text="", bg='white')
UART_Data_2 = Label(frame, text="", bg='white')
UART_Data_3 = Label(frame, text="", bg='white')
UART_Data_4 = Label(frame, text="", bg='white')
UART_Data_5 = Label(frame, text="", bg='white')
UART_Data_6 = Label(frame, text="", bg='white')
UART_Data_7 = Label(frame, text="", bg='white')
UART_Data_8 = Label(frame, text="", bg='white')

# PRZYCISKI
Config_button = Button(root, text="USART Configuration", command=config_menu, font=("Arial", 10))  # , padx=40, pady=40)
Start_Stop_button = Button(root, text="Start", command=start_stop_conection, font=("Arial", 10))
Save_button = Button(root, text="Save data", command=save_window_, font=("Arial", 10))
Clear_button = Button(root, text="Clear Data", command=clear_plot_and_data, font=("Arial", 10))

# POZYCJONOWANIE W GUI

canvas.get_tk_widget().grid(row=0, column=4, columnspan=4, rowspan=12)

frame.grid(row=0, column=0, columnspan=4, rowspan=8, sticky=W + E + S + N, padx=2, pady=2)
UART_Data_1.grid(row=7, column=0, sticky=S + W)
UART_Data_2.grid(row=6, column=0, sticky=S + W)
UART_Data_3.grid(row=5, column=0, sticky=S + W)
UART_Data_4.grid(row=4, column=0, sticky=S + W)
UART_Data_5.grid(row=3, column=0, sticky=S + W)
UART_Data_6.grid(row=2, column=0, sticky=S + W)
UART_Data_7.grid(row=1, column=0, sticky=S + W)
UART_Data_8.grid(row=0, column=0, sticky=S + W)

Var_to_submit_label.grid(row=8, column=0, columnspan=3, sticky=E + S)
Var_to_submit.grid(row=8, column=3, sticky=W + S + E)
Submit_var_button.grid(row=9, column=3, sticky=W + E + N)
Temp_label.grid(row=10, column=0, columnspan=3, sticky=S + E)
Temp_var.grid(row=10, column=3, sticky=S + W)

Start_Stop_button.grid(row=11, column=0, sticky=W + E + S)
Save_button.grid(row=11, column=1, sticky=W + E + S)
Clear_button.grid(row=11, column=2, sticky=W + E + S)
Config_button.grid(row=11, column=3, sticky=W + E + S)
canvas.draw()

root.mainloop()
