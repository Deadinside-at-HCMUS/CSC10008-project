import socket
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Constant
FORMAT = 'utf-8'
BUFFER_SIZE = 10000

# Colors
WHITE = '#ffffff'
DARK = '#000000'
LIGHT = '#b5e2ff'
BLUE = '#3047ff'
LIGHT_GRAY = '#bdb9b1'
DARK_GRAY = '#4f4e4d'

class SignUp():
    def __init__(self, root, client):
        self.root = root
        self.client = client
        
        # Rename window title
        self.root.title('Sign Up Page')

        # Changing window icon
        icon = ImageTk.PhotoImage(file='./images/cat.ico')
        self.root.iconphoto(False, icon)

        # Set window size
        self.root.geometry('1166x718')
        
        # Set button close, minimize button beside x button
        isResize = False
        self.root.resizable(isResize, isResize)

        # Background image
        self.bg_frame = Image.open('./images/background.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.root, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.grid(row=1)
        # self.bg_panel.pack(fill='both', expand='yes')

        # Sign up frame
        self.signup_frame = Frame(self.root, bg=WHITE, width=950, height=600)
        self.signup_frame.place(x=110, y=60)

        self.txt = "Let's started!"
        self.heading = Label(self.signup_frame, text=self.txt, font=('yu gothic ui', 25, 'bold'), bg=WHITE, fg=BLUE)
        self.heading.place(x=60, y=60, width=400, height=30)

        # Left side image
        self.side_image = Image.open('./images/computer.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.signup_frame, image=photo, bg=WHITE)
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # Sign up image
        self.sign_up_image = Image.open('./images/new_user.png')
        photo = ImageTk.PhotoImage(self.sign_up_image)
        self.sign_up_image_label = Label(self.signup_frame, image=photo, bg=WHITE)
        self.sign_up_image_label.image = photo
        self.sign_up_image_label.place(x=645, y=90)

        self.sign_up_label = Label(self.signup_frame, text='Sign Up', font=('yu gothic ui', 17, 'bold'), bg=WHITE, fg=BLUE)
        self.sign_up_label.place(x=655, y=200)

        # Username
        self.username_label = Label(self.signup_frame, text='Username', bg=WHITE, fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'))
        self.username_label.place(x=550, y=260)

        self.username_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg=WHITE, fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'))
        self.username_entry.place(x=580, y=295, width=270)

        self.username_line = Canvas(self.signup_frame, width=300, height=2.0, highlightthickness=0, bg=LIGHT_GRAY)
        self.username_line.place(x=550, y=319)

        # Username Icon
        self.username_icon = Image.open('./images/username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.signup_frame, image=photo, bg=WHITE)
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=292)

        # Signup button
        self.signup_button = Image.open('./images/button.png')
        photo = ImageTk.PhotoImage(self.signup_button)
        self.signup_button_label = Label(self.signup_frame, image=photo, bg=WHITE)
        self.signup_button_label.image = photo
        self.signup_button_label.place(x=550, y=500)
        Button(self.signup_button_label, text='SIGN UP', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                bg=BLUE, cursor='hand2', activebackground=BLUE, fg=WHITE, highlightthickness=0, command=self.signup_action).place(x=45, y=11)

        # Login 
        self.login_label = Label(self.signup_frame, text='I have an account!', fg=DARK_GRAY, bg=WHITE, font=('yu gothic ui', 12, "bold"))
        self.login_label.place(x=585, y=570)

        self.login_img = ImageTk.PhotoImage(file='./images/login.png')
        self.login = Button(self.signup_frame, image=self.login_img, bg=WHITE, cursor="hand2", borderwidth=0, 
                            background=WHITE, activebackground=WHITE, highlightthickness=0,command=self.login)
        self.login.place(x=735, y=570, width=80, height=35)

        # Password
        self.password_label = Label(self.signup_frame, text='Password', bg=WHITE, fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'))
        self.password_label.place(x=550, y=340)

        self.password_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg=WHITE, 
                                    fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'), show='*')
        self.password_entry.place(x=580, y=376, width=244)

        self.password_line = Canvas(self.signup_frame, width=300, height=2.0, highlightthickness=0, bg=LIGHT_GRAY)
        self.password_line.place(x=550, y=400)

        # Confirm Password
        self.confirm_password_label = Label(self.signup_frame, text='Confirm Password', bg=WHITE, fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'))
        self.confirm_password_label.place(x=550, y=421)

        self.confirm_password_entry = Entry(self.signup_frame, highlightthickness=0, relief=FLAT, bg=WHITE, fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'), show='*')
        self.confirm_password_entry.place(x=580, y=457, width=244)

        self.confirm_password_line = Canvas(self.signup_frame, width=300, height=2.0, highlightthickness=0, bg=LIGHT_GRAY)
        self.confirm_password_line.place(x=550, y=481)

        # Password Icon
        self.password_icon = Image.open('./images/password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.signup_frame, image=photo, bg=WHITE)
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=374)

        # Confirm Password Icon
        self.confirm_password_icon = Image.open('./images/password_icon.png')
        photo = ImageTk.PhotoImage(self.confirm_password_icon)
        self.confirm_password_icon_label = Label(self.signup_frame, image=photo, bg=WHITE)
        self.confirm_password_icon_label.image = photo
        self.confirm_password_icon_label.place(x=550, y=455)

        # Show/hide password
        self.show_image = ImageTk.PhotoImage(file='./images/show.png')
        self.hide_image = ImageTk.PhotoImage(file='./images/hide.png')
        self.show_button = Button(self.signup_frame, image=self.show_image, command=self.show_password, relief=FLAT,
                                  activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.show_button.place(x=860, y=380)

        # Show/hide confirm password
        self.show_confirm_image = ImageTk.PhotoImage(file='./images/show.png')
        self.hide_confirm_image = ImageTk.PhotoImage(file='./images/hide.png')
        self.show_confirm_button = Button(self.signup_frame, image=self.show_confirm_image, command=self.show_confirm_password, relief=FLAT,
                                            activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.show_confirm_button.place(x=860, y=461)

        #==================#
        self.gui_done = True
        self.root.mainloop()

    def show_password(self):
        self.hide_button = Button(self.signup_frame, image=self.hide_image, command=self.hide_password, relief=FLAT,
                                  activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.hide_button.place(x=860, y=380)
        self.password_entry.config(show='')

    def hide_password(self):
        self.show_button = Button(self.signup_frame, image=self.show_image, command=self.show_password, relief=FLAT,
                                  activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.show_button.place(x=860, y=380)
        self.password_entry.config(show='*')

    def show_confirm_password(self):
        self.hide_confirm_button = Button(self.signup_frame, image=self.hide_confirm_image, command=self.hide_confirm_password, relief=FLAT,
                                        activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.hide_confirm_button.place(x=860, y=461)
        self.confirm_password_entry.config(show='')

    def hide_confirm_password(self):
        self.show_confirm_button = Button(self.signup_frame, image=self.show_confirm_image, command=self.show_confirm_password, relief=FLAT,
                                        activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.show_confirm_button.place(x=860, y=461)
        self.confirm_password_entry.config(show='*')

    def signup_action(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.confirm_pw = self.confirm_password_entry.get()

        self.user_info = str(["SIGN-UP", self.username, self.password, self.confirm_pw])
        self.client.send(self.user_info.encode(FORMAT))

        self.response = self.client.recv(BUFFER_SIZE).decode(FORMAT)

        messagebox.showinfo(None, self.response)
        if self.response == "Register successfully!":
            self.root.destroy()
    
    def login(self):
        self.root.destroy()
