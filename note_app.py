import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.constants import *
from PIL import ImageTk, Image
import threading

# Colors
WHITE = '#ffffff'
DARK = '#000000'
LIGHT = '#b5e2ff'
BLUE = '#3047ff'
LIGHT_GRAY = '#bdb9b1'
DARK_GRAY = '#4f4e4d'

class Note:
    def __init__(self, root, client, user_info):
        self.client = client
        self.running = True
        self.gui_done = False

        gui_thread = threading.Thread(target=self.gui_loop(root, user_info))

        gui_thread.start()
    
    def gui_loop(self, root, user_info):
        self.user_info = eval(user_info)
        self.root = root
        # Rename window title
        self.root.title('E-Note Page')
        # Changing window icon
        icon = ImageTk.PhotoImage(file='./images/cat.ico')
        self.root.iconphoto(False, icon)

        # Set window size
        self.root.geometry('1166x718')
        
        # Set button close, minimize button beside x button
        isResize = False
        self.root.resizable(isResize, isResize)

        # Background image
        self.bg_frame = Image.open('./images/backgroundNote.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.root, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # Note frame
        self.frame = Frame(self.root, bg=WHITE, width=950, height=600)
        self.frame.place(x=110, y=60)

        self.tree = ttk.Treeview(self.root, show='headings')
        columns = ('id', 'type', 'content')
        self.tree['columns'] = ('id', 'type', 'content')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.column("id", anchor=CENTER, width=80)
        self.tree.column("type", anchor=CENTER, width=200)
        self.tree.column("content", anchor=W, width=400)
        # define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('type', text='TYPE')
        self.tree.heading('content', text='CONTENT')

        self.gui_done = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def stop(self):
        self.running = False
        self.root.destroy()
        self.client.close()
        exit(0)