from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.font import Font
from datetime import date

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('EricCrypto')
        self.width = 640
        self.height = 480
        self.year = date.today().year-1911
        self.master.resizable(True, True)
        self.x = (self.master.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (self.height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.appfont = Font(family='Consolas', size=12)
        self.create_widgets()
        self.bind_functions()

    def create_widgets(self):
        myfont = self.appfont
        mainw = self.master
        # Tab 字型設定
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('微軟正黑體','12','bold') )

        self.tabs = ttk.Notebook(mainw)
        self.tab1 = Frame(self.tabs)
        self.tab2 = Frame(self.tabs)
        self.tab3 = Frame(self.tabs)
        self.tabs.add(self.tab1, text='AES')
        self.tabs.add(self.tab2, text='RSA')
        self.tabs.add(self.tab3, text='ECC')
        self.tabs.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)

        # widgets for tab1
        self.lblKeyLen = Label(self.tab1, fg='black', font=myfont, text='Key Length:')
        self.lblKeyLen.place(x=10, y=10)
        self.optKeyLen = ['128', '192', '256']
        self.klSelected = StringVar()
        self.klSelected.set('128')
        self.opmKeyLen = OptionMenu(self.tab1 , self.klSelected, *self.optKeyLen)
        self.opmKeyLen.configure(font=myfont) 
        self.opmKeyLen.place(x=120, y=10)

        self.lblModeofOp = Label(self.tab1, fg='black', font=myfont, text='Mode of Operation:')
        self.lblModeofOp.place(x=220, y=10)
        self.optModeofOp = ['CBC', 'CFB', 'EAX']
        self.mopSelected = StringVar()
        self.mopSelected.set('CBC')
        self.opmModeofOp = OptionMenu(self.tab1 , self.mopSelected, *self.optModeofOp)
        self.opmModeofOp.configure(font=myfont) 
        self.opmModeofOp.place(x=390, y=10)

        self.btnOpenFolder = Button(self.tab1, text='Open Folder', fg='black', font=myfont) 
        self.btnOpenFolder.place(x=10, y=60)
        self.btnAesEncrypt = Button(self.tab1, text='AES Encrypt', fg='red', font=myfont)
        self.btnAesEncrypt.place(x=160, y=60)
        self.btnAesDecrypt = Button(self.tab1, text='AES Decrypt', fg='blue', font=myfont)
        self.btnAesDecrypt.place(x=280, y=60)

        self.lblAesLog = Label(self.tab1, fg='black', font=myfont, text='Log:')
        self.lblAesLog.place(x=10, y=100)
        self.txtAesLog = Text(self.tab1, font=myfont)
        self.txtAesLog.place(x=10, y=130, width=610, height=290)

        # widgets for tab2

        # widgets for tab3

    def bind_functions(self):
        self.master.bind('<Escape>', self.quit_app)
        self.btnOpenFolder.bind('<ButtonRelease-1>', self.open_folder)

    def open_folder(self, event=None):
        self.folder_name = filedialog.askdirectory(initialdir='.')
        print(self.folder_name)

    def quit_app(self, event=None):
        if messagebox.askokcancel('關閉', '確定離開？'):
            self.master.destroy()


twin = Tk()
app = Application(master=twin)
app.mainloop()
