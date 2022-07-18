from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.constants import *
from PIL import ImageTk, Image, ImageFile
import threading
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Note set up
IP = '127.0.0.1'
PORT = 5005
FORMAT = 'utf-8'
BUFFER_SIZE = 4100000

# Colors
WHITE = '#ffffff'
DARK = '#000000'
LIGHT = '#b5e2ff'
BLUE = '#3047ff'
LIGHT_GRAY = '#bdb9b1'
DARK_GRAY = '#4f4e4d'
RED = '#d22b2b'
PINK = '#ff647f'

class NoteApp():
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
        self.root.title('E-Note')

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
        self.bg_panel.grid(row=0)

        # Note Frame
        self.note_frame = Frame(self.root, bg=WHITE, width=950, height=600)
        self.note_frame.place(x=110, y=60)

        # List Notes 
        columns = ('id', 'type', 'content')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        style = ttk.Style()
        style.configure("Treeview.Heading", fg=DARK_GRAY, font=('yu gothic ui', 13))
        self.tree.column("id", anchor=CENTER, width=80)
        self.tree.column("type", anchor=CENTER, width=200)
        self.tree.column("content", anchor=W, width=400)

        # Headings
        self.tree.heading('id', text='ID')
        self.tree.heading('type', text='TYPE')
        self.tree.heading('content', text='CONTENT')

        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.tree.place(x=250, y=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Load Data
        self.client_notes = self.client.recv(BUFFER_SIZE).decode(FORMAT)
        self.client_notes = eval(self.client_notes)
        notes = self.client_notes['note']
        files = self.client_notes['file']
        imgs = self.client_notes['image']
        self.id_count = 1
        for note in notes:
            self.tree.insert('', 'end', values=(note['_id'], "Text", f"[Topic: {note['title']}] : {note['content'] if len(note['content']) < 20 else note['content'][0:20:1] + '...'}"))
            self.id_count = max(self.id_count, int(note['_id'])) + 1
        for img in imgs:
            self.tree.insert('', 'end', values=(img['_id'], "Image", f"[Name]: {img['name']}"))
            self.id_count = max(self.id_count, int(img['_id'])) + 1
        for file in files:
            self.tree.insert('', 'end', values=(file['_id'], "File", f"[Name]: {file['name']}"))
            self.id_count = max(self.id_count, int(file['_id'])) + 1

        self.frame1 = Frame(self.root, width=850, height=100, bg=WHITE)
        self.frame1.place(x=105, y=100)

        # Title
        self.heading = Label(self.frame1, text='E-NOTE', fg=BLUE,
                             bg=WHITE, font=('yu gothic ui', 25, 'bold'))
        self.heading.place(x=0, y=0, width=400, height=30)

        # User
        self.user = Label(self.frame1, text=f'User: {self.user_info[1]}', fg=DARK_GRAY,bg=WHITE, font=('yu gothic ui', 16, 'bold'))
        self.user.place(x=640, y=50)

        # Left side image
        self.side_image = Image.open('./images/cat_note.jpg')
        leftPhoto = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.note_frame, image=leftPhoto, bg=WHITE)
        self.side_image_label.image = leftPhoto
        self.side_image_label.place(x=120, y=340)

        # Functions
        self.frame2 = Frame(self.root, width=420, height=250, bg=WHITE)
        self.frame2.place(x=550, y=450)

        self.heading = Label(self.frame2, text='Add', fg=BLUE,
                             bg=WHITE, font=('yu gothic ui', 20, 'bold'))
        self.heading.place(x=1, y=35.5, width=50, height=30)

        self.add_txt_btn = Button(self.frame2, width=9, pady=8, text='Text', font=('yu gothic ui', 13, 'bold'),
                                cursor="hand2", bg=BLUE, fg=WHITE, border=0, relief=FLAT, highlightthickness=0, command=self.add_text)
        self.add_txt_btn.place(x=73, y=30)

        self.add_files_btn = Button(self.frame2, width=9, pady=8, text='File', font=('yu gothic ui', 13, 'bold'),
                                    cursor="hand2", bg=BLUE, fg=WHITE, border=0, relief=FLAT, highlightthickness=0, command=self.add_file)
        self.add_files_btn.place(x=181, y=30)

        self.upload_img_btn = Button(self.frame2, width=9, pady=8, text='Image', font=('yu gothic ui', 13, 'bold'),
                                     cursor="hand2", bg=BLUE, fg=WHITE, border=0, relief=FLAT, highlightthickness=0, command=self.upload_image)
        self.upload_img_btn.place(x=288, y=30)

        self.download_btn = Button(self.frame2, width=11, pady=8, text='Download', font=('yu gothic ui', 13, 'bold'),
                                   cursor="hand2", bg=DARK_GRAY, fg=WHITE, border=0, command=self.download)
        self.download_btn.place(x=1, y=110)

        self.view_btn = Button(self.frame2, width=11, pady=8, text='View', font=('yu gothic ui', 13, 'bold'),
                               cursor="hand2", bg=PINK, fg=WHITE, border=0, relief=FLAT, highlightthickness=0, command=self.view)
        self.view_btn.place(x=135, y=110)

        self.delete_btn = Button(self.frame2, width=11, pady=8, text='Delete', font=('yu gothic ui', 13, 'bold'),
                                 cursor="hand2", bg=RED, fg=WHITE, border=0, relief=FLAT, highlightthickness=0, command=self.delete)
        self.delete_btn.place(x=268, y=110)

        #==================#
        self.gui_done = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def add_text(self):
        self.win = Toplevel()
        window_width = 500
        window_height = 350
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        position_top = int(screen_height / 4 - window_height / 4)
        position_right = int(screen_width / 2 - window_width / 2)
        self.win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.win.title('Text')
        self.win.configure(background=WHITE)
        self.win.resizable(0, 0)

        self.topic_label = Label(self.win, text='Topic:', font=('yu gothic ui', 12, 'bold'), fg=DARK_GRAY, bg=WHITE)
        self.topic_label.place(x=10, y=10)
        self.topic_area = Text(self.win, height=1)
        self.topic_area.config(font=("yu gothic ui", 14))
        self.topic_area.pack(padx=(80, 20), pady=10)

        self.input_label = Label(self.win, text='Notes:', font=('yu gothic ui', 12, 'bold'), fg=DARK_GRAY, bg=WHITE)
        self.input_label.place(x=10, y=150)
        self.input_area = Text(self.win, height=10)
        self.input_area.config(font=("yu gothic ui", 14))
        self.input_area.pack(padx=(80, 20), pady=3)

        self.send_btn = Button(self.win, text="Add note", command=self.add_note)
        self.send_btn.config(font=("yu gothic ui", 14))
        self.send_btn.pack(padx=50, pady=10)

    def add_note(self):
        while self.running:
            self.note_topic = f"{self.topic_area.get('1.0', 'end').strip()}"
            self.note = f"{self.input_area.get('1.0', 'end').strip()}"
            self.user_note = str(["ADD-NOTE", self.user_info[1], self.note_topic, self.note, self.id_count])
            self.client.send(self.user_note.encode(FORMAT))
            response = self.client.recv(BUFFER_SIZE).decode(FORMAT)
            if response == "Note successfully created!":
                if self.gui_done:
                    self.tree.insert('', 'end', values=(self.id_count, "Text", f"[Topic: {self.note_topic}] : {self.note if len(self.note) < 20 else self.note[0:20:1] + '...'}"))
                    self.id_count += 1
                    self.input_area.delete('1.0', 'end')
                    messagebox.showinfo(None, response)
                    self.win.destroy()
                    break
            elif response == "This title is already exist!":
                messagebox.showwarning(title="Warning!", message="This title is already exist!")
                break
            else:
                messagebox.showwarning(title="Warning!", message="You must enter a note!")
                break

    def delete(self):
        try:
            self.task_index = self.tree.selection()[0]
            self.id = self.tree.item(self.task_index)['values'][0]
            self.type = self.tree.item(self.task_index)['values'][1]
            self.client.send(str(["DELETE-NOTE", self.user_info[1], self.id, self.type]).encode(FORMAT))
            self.tree.delete(self.task_index)
        except:
            messagebox.showwarning(title="Warning!", message="You must select a note!")

    def upload_image(self):
        img_path = askopenfilename(title='Select Image',filetypes=[("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")])
        if img_path == "":
            return
        img = img_path.split('/')
        self.image = img[len(img) - 1]
        while self.running:
            self.user_image = str(["ADD-IMAGE", self.user_info[1], self.image, self.id_count])
            self.client.send(self.user_image.encode(FORMAT))
            response = self.client.recv(BUFFER_SIZE).decode(FORMAT)
            if response == "Image successfully created!":
                with open(img_path, 'rb') as f:
                    self.client.send(f.read())
                    f.close()
                if self.gui_done:
                    self.tree.insert('', 'end', values=(self.id_count, "Image", f"[Name]: {self.image}"))
                    self.id_count += 1
                    messagebox.showinfo(None, response)
                    break
            elif response == "This title is already exist!":
                messagebox.showwarning(title="Warning!", message="This title is already exist!")
                break
            else:
                messagebox.showwarning(title="Warning!", message="You must enter a image!")
                break

    def view(self):
        try:
            self.task_index = self.tree.selection()[0]
            self.id = self.tree.item(self.task_index)['values'][0]
            self.type = self.tree.item(self.task_index)['values'][1]
            self.file_name = self.tree.item(self.task_index)['values'][2]
            self.file_name = self.file_name[8:]
            self.client.send(str(["VIEW-NOTE", self.user_info[1], self.id, self.type]).encode(FORMAT))
            if self.type == "Image":
                data = self.client.recv(BUFFER_SIZE)
                img = io.BytesIO(data)
                image = Image.open(img)
                image.show()
            elif self.type == "Text":
                data = self.client.recv(BUFFER_SIZE)
                data = eval(data)
                Topic = data[0]
                Content = data[1]
                self.win = Toplevel()
                window_width = 500
                window_height = 300
                screen_width = self.win.winfo_screenwidth()
                screen_height = self.win.winfo_screenheight()
                position_top = int(screen_height / 4 - window_height / 4)
                position_right = int(screen_width / 2 - window_width / 2)
                self.win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
                self.win.title('Text')
                self.win.configure(background=WHITE)
                self.win.resizable(0, 0)

                self.topic_label = Label(self.win, text='Topic:', font=('yu gothic ui', 12, 'bold'), fg=DARK_GRAY, bg=WHITE)
                self.topic_label.place(x=15, y=12)
                self.topic_area = Label(self.win, text=Topic, font=('yu gothic ui', 12), bg=WHITE)
                self.topic_area.place(x=95, y=12)

                self.input_label = Label(self.win, text='Notes:', font=('yu gothic ui', 12, 'bold'), fg=DARK_GRAY, bg=WHITE)
                self.input_label.place(x=15, y=52)

                self.text_area = scrolledtext.ScrolledText(self.win, width=35, height=12, font=('yu gothic ui', 12))
                self.text_area.grid(column=0, pady=10, padx=10)
                self.text_area.place(x=95, y=52)
                self.text_area.insert(INSERT, Content)
                self.text_area.config(state=DISABLED)
        except:
            messagebox.showwarning(
                title="Warning!", message="You must select a note!")

    def download(self):
        file_path = askdirectory(title="Select Folder")
        if file_path == "":
            messagebox.showwarning(title="Warning!", message="You must enter a file!")
            return
        try:
            self.task_index = self.tree.selection()[0]
            self.id = self.tree.item(self.task_index)['values'][0]
            self.type = self.tree.item(self.task_index)['values'][1]
            self.client.send(str(["DOWNLOAD-NOTE", self.user_info[1], self.id, self.type]).encode(FORMAT))
            if self.type == "Text":
                data = self.client.recv(BUFFER_SIZE).decode(FORMAT)
                data = eval(data)
                print(data)
                Topic = data[0]
                Content = data[1]
                with open(f'{file_path}/{Topic}.txt', 'w') as f:
                    f.add_note(Content)
                f.close()
            else:
                self.file_name = self.tree.item(self.task_index)['values'][2]
                self.file_name = self.file_name.split('[Name]: ')
                self.file_name = self.file_name[len(self.file_name) - 1]
                with open(f"{file_path}/{self.file_name}", 'wb') as f:
                    data = self.client.recv(BUFFER_SIZE)
                    f.add_note(data)
                    f.close()
        except:
            messagebox.showwarning(title="Warning!", message="You must enter a file!")

    def add_file(self):
        file_path = askopenfilename(title='Select File',filetypes=[('text files', '*.txt'), ('All files', '*.*')])
        if file_path == "":
            return
        self.file = file_path.split('/')
        self.file = self.file[len(self.file) - 1]
        while self.running:
            self.user_file = str(["ADD-FILE", self.user_info[1], self.file, self.id_count])
            self.client.send(self.user_file.encode(FORMAT))
            response = self.client.recv(BUFFER_SIZE).decode(FORMAT)
            if response == "File successfully created!":
                with open(file_path, 'rb') as f:
                    self.client.send(f.read())
                    f.close()
                if self.gui_done:
                    self.tree.insert('', 'end', values=(self.id_count, "File", f"[Name]: {self.file}"))
                    self.id_count += 1
                    messagebox.showinfo(None, response)
                    break
            elif response == "This title is already exist!":
                messagebox.showwarning(title="Warning!", message="This title is already exist!")
                break
            else:
                messagebox.showwarning(title="Warning!", message="You must enter a file!")
                break

    def stop(self):
        self.running = False
        self.root.destroy()
        self.client.close()
        exit(0)
