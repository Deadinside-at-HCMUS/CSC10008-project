from tkinter import *
from PIL import ImageTk, Image

WHITE = '#ffffff'
DARK = '#000000'
LIGHT = '#b5e2ff'
BLUE = '#3047ff'
LIGHT_GRAY = '#bdb9b1'
DARK_GRAY = '#4f4e4d'

class Login:
    def __init__(self, window):
        self.window = window
        # Rename window title
        self.window.title('Login Page')
        # Changing window icon
        icon = ImageTk.PhotoImage(file='C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/cat.ico')
        self.window.iconphoto(False, icon)

        # Set window size
        self.window.geometry('1166x718')

        # Set fullscreen default or not
        self.window.state('zoomed')  # Win
        isFull = False
        
        isResize = False
        # Set button close, minizmze button beside x button
        self.window.resizable(isResize, isResize)

        # Background image
        self.bg_frame = Image.open('C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/backgroundB.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # Login frame
        if isFull:
            xFrame = 300
            yFrame = 100
        else:
            xFrame = 110
            yFrame = 60
        self.lgn_frame = Frame(self.window, bg=WHITE, width=950, height=600)
        self.lgn_frame.place(x=xFrame, y=yFrame)

        self.txt = 'Welcome to E-Note!'
        self.heading = Label(self.lgn_frame, text=self.txt, 
                             font=('yu gothic ui', 25, 'bold'), bg=WHITE, fg=BLUE)
        self.heading.place(x=80, y=60, width=400, height=30)

        # Left side image
        self.side_image = Image.open('C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/catpng.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg=WHITE)
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # Sign in image
        self.sign_in_image = Image.open('C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/catvec.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg=WHITE)
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=635, y=130)

        self.sign_in_label = Label(self.lgn_frame, text='Sign In', 
                                   font=('yu gothic ui', 17, 'bold'), bg=WHITE, fg=BLUE)
        self.sign_in_label.place(x=650, y=240)

        # Username
        self.username_label = Label(self.lgn_frame, text='Username', bg=WHITE, fg=DARK_GRAY, 
                                    font=('yu gothic ui', 13, 'bold'))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg=WHITE, 
                                    fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'))
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, highlightthickness=0, bg=LIGHT_GRAY)
        self.username_line.place(x=550, y=359)

        # Username Icon
        self.username_icon = Image.open('C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg=WHITE)
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # Login button
        self.lgn_button = Image.open('C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg=WHITE)
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=555, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg=BLUE, cursor='hand2', activebackground=BLUE, fg=WHITE, highlightthickness=0)
        self.login.place(x=40, y=10)

        # Forgot password
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password?",
                                    font=("yu gothic ui", 13, "bold underline"), fg=BLUE, relief=FLAT, highlightthickness=0,
                                    activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.forgot_button.place(x=620, y=510)        

        # Sign up
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background=WHITE, fg=DARK_GRAY, highlightthickness=0,)
        self.sign_label.place(x=600, y=560)

        self.signup_img = ImageTk.PhotoImage(file='C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/signup.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg=WHITE, cursor="hand2",
                                          borderwidth=0, background=WHITE, activebackground=WHITE, highlightthickness=0,)
        self.signup_button_label.place(x=720, y=554, width=120, height=35)

        # Password
        self.password_label = Label(self.lgn_frame, text='Password', bg=WHITE, fg=DARK_GRAY, 
                                    font=('yu gothic ui', 13, 'bold'))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg=WHITE, 
                                    fg=DARK_GRAY, font=('yu gothic ui', 13, 'bold'), show='*')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, highlightthickness=0, bg=LIGHT_GRAY)
        self.password_line.place(x=550, y=440)

        # Password Icon
        self.password_icon = Image.open('C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg=WHITE)
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)

        # Show/hide password
        self.show_image = ImageTk.PhotoImage(file='C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/show.png')
        self.hide_image = ImageTk.PhotoImage(file='C:/Users/Nguyen Hi Huu/source/repos/Python_Socket/CSC10008-project/images/hide.png')   
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground=WHITE, borderwidth=0, background=WHITE, cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

def page():
    window = Tk()
    Login(window)
    window.mainloop()

page()