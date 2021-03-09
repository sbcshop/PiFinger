#! /usr/bin/python3

"""
This file contains GUI code for Configuring of SBS Servo
Developed by - SB Components
http://sb-components.co.uk
"""

from fingerprint import FingerprintSensor
import logging
import io
from PIL import Image, ImageTk
import os
from tkinter import font
import tkinter as tk
from tkinter import messagebox
from time import sleep
import webbrowser

if os.name == "posix":
    COMPORT_BASE = "/dev/"
else:
    COMPORT_BASE = ""


class MainApp(tk.Tk):
    """
    This is a class for Creating Frames and Buttons for left and top frame
    """
    current_baud = 9600

    def __init__(self, *args, **kwargs):
        global logo, img, xy_pos

        tk.Tk.__init__(self, *args, **kwargs)

        self.screen_width = tk.Tk.winfo_screenwidth(self)
        self.screen_height = tk.Tk.winfo_screenheight(self)
        self.app_width = 800
        self.app_height = 480
        self.xpos = (self.screen_width / 2) - (self.app_width / 2)
        self.ypos = (self.screen_height / 2) - (self.app_height / 2)
        xy_pos = self.xpos, self.ypos

        self.label_font = font.Font(family="Helvetica", size=10)
        self.heading_font = font.Font(family="Helvetica", size=12)

        self.geometry(
            "%dx%d+%d+%d" % (self.app_width, self.app_height, self.xpos,
                             self.ypos))
        self.title("Fingerprint Sensor")

        self.config(bg="gray85")

        img = tk.PhotoImage(file=path + '/Images/settings.png')
        logo = tk.PhotoImage(file=path + '/Images/sblogo.png')

        self.left_frame = tk.Frame(self, width=int(self.app_width / 3),
                                   bg="gray10")
        self.left_frame.pack(side="left", fill="both")
        self.left_frame.pack_propagate(0)

        self.right_frame = tk.Frame(self, bg="gray85")
        self.right_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.propagate(0)

        self.label_font = font.Font(family="Helvetica", size=10)
        self.heading_font = font.Font(family="Helvetica", size=12)

        self.frames = {}
        for F in (CompareFrame, RegisterFrame):
            frame_name = F.__name__
            frame = F(parent=self.right_frame, controller=self)
            self.frames[frame_name] = frame
            frame.config(bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame_contents()
        # self.show_frame("CompareFrame")
        self.compare_screen()
        robot.set_active_mode()

    def left_frame_contents(self):
        """
        This function creates the left frame widgets
        """
        global logo
        self._com_port = tk.StringVar()
        self._com_port.set(COMPORT_BASE)

        label = tk.Label(self.left_frame, image=logo, height=40, width=250,
                         bg='white')
        label.place(x=7, y=10)

        self.compare_button = tk.Button(self.left_frame,
                                        text="Compare Fingerprint",
                                        bg="gray60",
                                        font=self.label_font, width=31,
                                        command=self.compare_screen)
        self.compare_button.place(x=5, y=60)

        self.add_fingerprint_button = tk.Button(self.left_frame,
                                                text="Add Fingerprint",
                                                bg="gray60",
                                                font=self.label_font,
                                                width=31,
                                                command=self.register_screen)
        self.add_fingerprint_button.place(x=5, y=100)

        self.remove_fingerprint_button = tk.Button(self.left_frame,
                                                   text="Remove Fingerprint "
                                                        "by ID",
                                                   bg="gray60",
                                                   font=self.label_font,
                                                   width=31,
                                                   command=self.remove_single_dialog)
        self.remove_fingerprint_button.place(x=5, y=140)

        self.remove_all_button = tk.Button(self.left_frame,
                                           text="Remove "
                                                "All Fingerprints",
                                           bg="gray60",
                                           font=self.label_font,
                                           width=31,
                                           command=self.remove_all_dialog)
        self.remove_all_button.place(x=5, y=180)

        #  Connect Port
        helvetica_bold = "Helvetica 10 bold"
        helvetica_italics = "Helvetica 10"

        serial_box = tk.Canvas(self.left_frame, width=250,
                               height=110, bg="white", bd=2)
        serial_box.place(x=4, y=220)

        tk.Label(serial_box, fg="gray10", bg="white",
                 font=helvetica_bold, text="Comm Port").place(x=2, y=3)
        self.com_entry = tk.Entry(serial_box, fg="black", bg="white",
                                  bd=2,
                                  font=helvetica_italics, width=14,
                                  textvariable=self._com_port)
        self.com_entry.place(x=140, y=4)

        tk.Label(serial_box, fg="gray10", bg="white",
                 font=helvetica_bold, text="Baud Rate").place(x=2, y=40)
        tk.Label(serial_box, text="9600", borderwidth=2, width=14,
                 justify="left", anchor="w", bg="white",
                 relief="groove").place(x=140, y=40)

        self.connect_button = tk.Button(serial_box, text="Connect",
                                        fg="gray10", bg="white",
                                        font=self.label_font, width=9,
                                        command=self.connect_hat)
        self.connect_button.place(x=150, y=80)

        self.circle = tk.Canvas(serial_box, height=40, width=40,
                                bg="white", bd=0,
                                highlightthickness=0)
        self.indication = self.circle.create_oval(10, 10, 25, 25, fill="red")
        self.circle.place(x=1, y=80)

        url = "https://shop.sb-components.co.uk/"
        LabelButton(self.left_frame, url)

    def connect_hat(self):
        #  Connect Sensor
        """
        This function connects the serial port
        """
        if self.connect_button.cget(
                'text') == 'Connect' and self._com_port.get():
            robot.connect_sensor(port=self._com_port.get(),
                                 baud_rate=self.current_baud)
            if robot.alive:
                self.connect_button.config(relief="sunken", text="Disconnect")
                self.circle.itemconfigure(self.indication, fill="green3")
                self.com_entry.config(state="readonly")
            else:
                messagebox.showerror("Port Error",
                                     "Couldn't Connect with {} ".format(
                                         self._com_port.get()))

        elif self.connect_button.cget('text') == 'Disconnect':
            self.connect_button.config(relief="raised", text="Connect")
            self.circle.itemconfigure(self.indication, fill="red")
            self.com_entry.config(state="normal")
            robot.disconnect_sensor()

    def compare_screen(self):
        self.compare_button.config(relief="sunken", fg="SteelBlue2")
        self.add_fingerprint_button.config(relief="raised", fg="black")
        self.remove_fingerprint_button.config(relief="raised", fg="black")
        self.remove_all_button.config(relief="raised", fg="black")
        self.show_frame("CompareFrame")

    def register_screen(self):
        self.compare_button.config(relief="raised", fg="black")
        self.add_fingerprint_button.config(relief="sunken", fg="SteelBlue2")
        self.remove_fingerprint_button.config(relief="raised", fg="black")
        self.remove_all_button.config(relief="raised", fg="black")
        self.show_frame("RegisterFrame")
        self.get_frame("CompareFrame").stop_anim = True

    def show_frame(self, frame_name):
        """
        This function raise the frame on Top
        Args:
            frame_name: Name of the Frame
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def get_frame(self, frame):
        return self.frames[frame]

    def remove_all_dialog(self):
        self.get_frame("CompareFrame").stop_anim = True
        result = messagebox.askquestion("Remove All Fingerprints", "Are You "
                                                                   "Sure?",
                                        icon='warning')
        if result == 'yes':
            robot.remove_all_fingerprints()
            sleep(.1)
            if b"<R>OK</R>\n" in robot.rxData:
                robot.rxData = []
                messagebox.showinfo("Fingerprint Remove", "All Fingerprints "
                                                          "Removed!")

    def remove_single_dialog(self):
        self.get_frame("CompareFrame").stop_anim = True
        PopupWindow(self)


class CompareFrame(tk.Frame):
    """
    This is a class for Creating widgets for Matplotlib Graph
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.LARGE_FONT = ("Verdana", 12)
        self.reg_frame_obj = None
        self.stop_anim = False
        self.after_idle(self.timer)

        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        compare_canvas = tk.Canvas(self,
                                   width=int(
                                       self.controller.app_width * 2 / 3) - 15,
                                   height=self.controller.app_height - 15,
                                   bd=2,
                                   bg="gray50")
        compare_canvas.grid(row=0, column=0, padx=5, pady=5)
        compare_canvas.grid_propagate(0)

        self.compare_button = tk.Button(compare_canvas, text='Compare',
                                        fg="black", bg="gray90",
                                        font=self.LARGE_FONT, bd=2,
                                        highlightthickness=0, width=20,
                                        command=self.compare_fp)
        self.compare_button.grid(row=0, column=0, padx=10, pady=10)

        # fp_img = tk.PhotoImage()
        self.fp_img = tk.PhotoImage(file="Images/fingerprint_anim-0.gif",
                                    format="gif -index 0")

        self.img_label = tk.Label(compare_canvas, padx=10, pady=10,
                                  justify="center", bg="black", relief="flat",
                                  fg="black", image=self.fp_img,
                                  height=186,
                                  width=160)
        self.img_label.grid(row=0, column=1, padx=80, pady=50)
        self.img_label.image = self.fp_img
        self.gif_index = 0

        self.registration_status = False

        text_str = "This is finger compare window"
        text_box = tk.Label(compare_canvas, bg="gray50", fg="white", bd=3,
                            font=self.LARGE_FONT, height=8, width=40,
                            text=text_str)
        text_box.grid(row=1, column=0, columnspan=3)
        # text_box.insert(tk.END, text_str)

    def next_frame(self):
        try:
            # XXX: Move to the next frame
            self.fp_img.configure(format="gif -index {}".format(
                self.gif_index))
            self.gif_index += 1
        except tk.TclError:
            self.gif_index = 0
            return self.next_frame()
        else:
            if not self.stop_anim:
                self.after(50, self.next_frame)  # XXX: Fixed animation speed
            else:
                self.fp_img.configure(format="gif -index 0")

    def timer(self):
        if len(robot.rxData) > 1:
            if robot.rxData[-2] == b"<I>":
                img_byte = robot.rxData[-1]
                img_byte = img_byte.replace(b"</I>", b"")
                robot.rxData = []

                img_bytes_array = bytearray(img_byte)
                head = bytearray(
                    [80, 53, 32, 10, 49, 55, 54, 32, 49, 55, 54, 32, 50, 53,
                     53, 10])

                img_arr = bytearray(head + img_bytes_array)

                image = Image.open(io.BytesIO(img_arr))
                # image.save(img_path)
                #  Show Image
                image = ImageTk.PhotoImage(image)
                self.img_label.configure(image=image)
                self.img_label.image = image
                robot.compare_fingerprint()
            elif robot.rxData[-2] in (b"Matched!\n", b'Mismatch!\n'):
                match_status = robot.rxData[-2].decode("utf-8")
                self.stop_anim = True
                if "Matched!" in match_status:
                    match_num = robot.rxData[-1].decode("utf-8")
                    match_num = match_num.replace("<R>PASS_", "").replace(
                        "</R>", "")
                    robot.rxData = []
                    messagebox.showinfo("Match Status",
                                        "Fingerprint Matched with {}".format(
                                            match_num))
                else:
                    robot.rxData = []
                    messagebox.showinfo("Match Status",
                                        "Fingerprint Mismatched!")
                self.stop_anim = True

            elif b'List registration status:\n' in robot.rxData and \
                    robot.rxData[-1] == b"\n":
                fingers_str = robot.rxData[-3].replace(b"<R>", b"").replace(
                    b"</R>", b"")
                fingers = int(fingers_str)
                robot.register_fingerprint_at(fingers + 1)
                robot.rxData = []
                self.registration_status = True

        if self.registration_status:
            data_string = ""
            rx_buffer = robot.rxData[0:]
            if b'<R>FINISHED</R>\n' in rx_buffer:
                length = len(rx_buffer)
                del rx_buffer[length - 1:length]
                rx_buffer[-1] = b"Fingerprint Registration Complete\n"
                robot.rxData = []
            for data in rx_buffer:
                decoded_data = data.decode("utf-8")
                data_string = decoded_data + data_string
            self.controller.get_frame(
                "RegisterFrame").register_text_label.config(
                text=data_string)

        self.after(1000, self.timer)

    def compare_fp(self):
        self.gif_index = 0
        self.after_idle(self.next_frame)
        self.stop_anim = False
        robot.compare_fingerprint()
        # robot.read_fp_image()


class RegisterFrame(tk.Frame):
    """
    This is a class for Creating widgets for Matplotlib Graph
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.LARGE_FONT = ("Verdana", 12)

        self.message_str = tk.StringVar()
        # self.message_str.set("Hello")

        self.font = self.controller.label_font

        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        register_canvas = tk.Canvas(self,
                                    width=int(
                                        self.controller.app_width * 2 / 3) -
                                          15,
                                    height=self.controller.app_height - 15,
                                    bd=2,
                                    bg="gray50")
        register_canvas.grid(row=0, column=0, padx=5, pady=5)
        register_canvas.grid_propagate(0)

        compare_button = tk.Button(register_canvas, text='Register',
                                   fg="black", bg="gray90",
                                   font=self.LARGE_FONT, bd=2,
                                   highlightthickness=0,
                                   command=self.register_fp)
        compare_button.place(x=50, y=50)

        self.register_text_label = tk.Label(register_canvas, justify="left",
                                            fg="black", bd=5, anchor="nw",
                                            height=15, font=self.font,
                                            width=60)
        self.register_text_label.place(x=20, y=150)
        # self.register_text_label.grid(row=0, column=1, padx=30, pady=10)

    @staticmethod
    def register_fp():
        robot.get_fp_numbers()
        # robot.register_fingerprint_at(num)


class PopupWindow(object):
    """
    This Window is for Remove Finger ID Pop Up
    """

    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Remove Fingerprint by ID")
        self.top.resizable(False, False)
        self.width = master.screen_width / 5
        self.height = master.screen_height / 6
        self.top.geometry("%dx%d+%d+%d" % (self.width, self.height, xy_pos[0]
                                           * 2, xy_pos[1] * 15 / 7))

        self.fp_id = tk.IntVar()
        self.fp_id.set(0)
        self.bell = master.bell

        tk.Label(self.top, text="Enter Fingerprint ID").grid(row=0,
                                                             column=0,
                                                             padx=25, pady=20)
        int_vcmd = (master.register(self.id_validate), '%P')
        self.entry_box = tk.Entry(self.top, validate='key',
                                  validatecommand=int_vcmd,
                                  width=6, font=master.label_font,
                                  textvariable=self.fp_id)
        self.entry_box.grid(row=0, column=1, padx=25, pady=20)
        tk.Button(self.top, text='Delete',
                  command=self.cleanup).grid(row=1, column=0, columnspan=2,
                                             padx=15)

    def id_validate(self, new_value):
        try:
            if not new_value or 0 <= int(new_value) <= 24:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def cleanup(self):
        value = self.entry_box.get()
        robot.remove_one_fingerprint(value)
        self.top.destroy()
        if b"<R>OK</R>\n" in robot.rxData:
            robot.rxData = []
            messagebox.showinfo("Fingerprint Remove", "Fingerprints {} "
                                                      "Removed!".format(value))


class LabelButton(object):
    def __init__(self, master, url=None):
        self.url = url
        self.label = tk.Label(master, image=logo, height=40, width=250,
                              bg='white')
        self.label.place(x=7, y=400)
        self.label.bind("<Button-1>", self.open_url)

    def open_url(self, tmp):
        webbrowser.open(self.url, new=1)


robot = None
logo = None
img = None
path = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    robot = FingerprintSensor()
    app = MainApp()
    app.tk.call('wm', 'iconphoto', app._w, img)
    app.resizable(0, 0)
    app.mainloop()
