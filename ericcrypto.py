from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.font import Font
from datetime import date
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
import os
import json
import base64
import pickle

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('EricCrypto')
        self.width = 650
        self.height = 480
        self.year = date.today().year-1911
        self.master.resizable(True, True)
        self.x = (self.master.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.master.winfo_screenheight() // 2) - (self.height // 2)
        # 定義視窗尺寸及位置
        self.master.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.appfont = Font(family='Consolas', size=12)
        self.name = []
        self.folder_path = ''
        self.file_path = ''
        self.en_folder = ''
        self.move_folder = ''
        self.mode = ''
        self.ecc_folder = ''
        self.enc_file = ''
        self.dec_file = ''
        self.sign_file = ''
        self.ciphertext = bytes()
        self.key = bytes()
        self.file_sha = ''
        # 建立視窗
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
        self.lblAesKeyLen = Label(self.tab1, fg='black', font=myfont, text='Key Length:')
        self.lblAesKeyLen.place(x=10, y=10)
        self.optAesKeyLen = ['128', '192', '256']
        self.klAesSelected = StringVar()
        self.klAesSelected.set('128')
        self.opmAesKeyLen = OptionMenu(self.tab1 , self.klAesSelected, *self.optAesKeyLen)
        self.opmAesKeyLen.configure(font=myfont) 
        self.opmAesKeyLen.place(x=120, y=10)

        self.lblAesModeofOp = Label(self.tab1, fg='black', font=myfont, text='Mode of Operation:')
        self.lblAesModeofOp.place(x=220, y=10)
        self.optAesModeofOp = ['CBC', 'CFB', 'EAX']
        self.mopAesSelected = StringVar()
        self.mopAesSelected.set('CBC')
        self.opmAesModeofOp = OptionMenu(self.tab1 , self.mopAesSelected, *self.optAesModeofOp)
        self.opmAesModeofOp.configure(font=myfont) 
        self.opmAesModeofOp.place(x=390, y=10)

        self.btnOpenAesFolder = Button(self.tab1, text='Open Folder', fg='black', font=myfont) 
        self.btnOpenAesFolder.place(x=10, y=60)
        self.btnOpenAesFile = Button(self.tab1, text='Open File', fg='black', font=myfont) 
        self.btnOpenAesFile.place(x=130, y=60)
        self.btnAesEncrypt = Button(self.tab1, text='AES Encrypt', fg='red', font=myfont)
        self.btnAesEncrypt.place(x=240, y=60)
        self.btnAesDecrypt = Button(self.tab1, text='AES Decrypt', fg='blue', font=myfont)
        self.btnAesDecrypt.place(x=360, y=60)

        self.lblAesLog = Label(self.tab1, fg='black', font=myfont, text='Log:')
        self.lblAesLog.place(x=10, y=100)
        self.txtAesLog = Text(self.tab1, font=myfont)
        self.txtAesLog.place(x=10, y=130, width=610, height=290)

        # widgets for tab2
        self.lblRSAKeyLen = Label(self.tab2, fg='black', font=myfont, text='Key Length:')
        self.lblRSAKeyLen.place(x=10, y=10)
        self.optRSAKeyLen = ['1024', '2048', '4096']
        self.klRSASelected = StringVar()
        self.klRSASelected.set('1024')
        self.opmRSAKeyLen = OptionMenu(self.tab2 , self.klRSASelected, *self.optRSAKeyLen)
        self.opmRSAKeyLen.configure(font=myfont) 
        self.opmRSAKeyLen.place(x=120, y=10)

        self.lblRSAModeofOp = Label(self.tab2, fg='black', font=myfont, text='Mode of Operation: OAEP')
        self.lblRSAModeofOp.place(x=220, y=10)

        self.btnOpenRSAFolder = Button(self.tab2, text='Open Folder', fg='black', font=myfont) 
        self.btnOpenRSAFolder.place(x=10, y=60)
        self.btnOpenRSAFile = Button(self.tab2, text='Open File', fg='black', font=myfont) 
        self.btnOpenRSAFile.place(x=130, y=60)
        self.btnRSAEncrypt = Button(self.tab2, text='RSA Encrypt', fg='red', font=myfont)
        self.btnRSAEncrypt.place(x=240, y=60)
        self.btnRSADecrypt = Button(self.tab2, text='RSA Decrypt', fg='blue', font=myfont)
        self.btnRSADecrypt.place(x=360, y=60)

        self.lblRSALog = Label(self.tab2, fg='black', font=myfont, text='Log:')
        self.lblRSALog.place(x=10, y=100)
        self.txtRSALog = Text(self.tab2, font=myfont)
        self.txtRSALog.place(x=10, y=130, width=610, height=290)

        # widgets for tab3
        self.lblECCKeyLen = Label(self.tab3, fg='black', font=myfont, text='Mode of Operation: ECDSA')
        self.lblECCKeyLen.place(x=10, y=10)

        self.lblECCModeofOp = Label(self.tab3, fg='black', font=myfont, text='Mode of Elliptic:')
        self.lblECCModeofOp.place(x=280, y=10)
        self.optECCModeofOp = ['SECP256R1', 'SECP384R1', 'SECP521R1']
        self.mopECCSelected = StringVar()
        self.mopECCSelected.set('SECP256R1')
        self.opmECCModeofOp = OptionMenu(self.tab3 , self.mopECCSelected, *self.optECCModeofOp)
        self.opmECCModeofOp.configure(font=myfont) 
        self.opmECCModeofOp.place(x=450, y=10)

        self.btnOpenECCFolder = Button(self.tab3, text='Open Folder', fg='black', font=myfont) 
        self.btnOpenECCFolder.place(x=10, y=60)
        self.btnOpenECCFile = Button(self.tab3, text='Open File', fg='black', font=myfont) 
        self.btnOpenECCFile.place(x=130, y=60)
        self.btnECCSignature = Button(self.tab3, text='ECC Signature', fg='red', font=myfont)
        self.btnECCSignature.place(x=240, y=60)
        self.btnECCVerify = Button(self.tab3, text='ECC Verify', fg='blue', font=myfont)
        self.btnECCVerify.place(x=380, y=60)

        self.lblECCLog = Label(self.tab3, fg='black', font=myfont, text='Log:')
        self.lblECCLog.place(x=10, y=100)
        self.txtECCLog = Text(self.tab3, font=myfont)
        self.txtECCLog.place(x=10, y=130, width=610, height=290)

    def bind_functions(self):
        self.master.bind('<Escape>', self.quit_app)
        self.mode = self.tabs.tab(self.tabs.select(), "text")

        # AES encrypt and decrypt
        self.btnOpenAesFolder.bind('<ButtonRelease-1>', lambda event: self.open_folder(mode='AES', event=event))
        self.btnOpenAesFile.bind('<ButtonRelease-1>', lambda event: self.open_file(mode='AES', event=event))
        self.btnAesEncrypt.bind('<ButtonRelease-1>', self.aes_encrypt_files)
        self.btnAesDecrypt.bind('<ButtonRelease-1>', self.aes_decrypt_files)

        # RSA encrypt and decrypt
        self.btnOpenRSAFolder.bind('<ButtonRelease-1>', lambda event: self.open_folder(mode='RSA', event=event))
        self.btnOpenRSAFile.bind('<ButtonRelease-1>', lambda event: self.open_file(mode='RSA', event=event))
        self.btnRSAEncrypt.bind('<ButtonRelease-1>', self.rsa_encrypt_files)
        self.btnRSADecrypt.bind('<ButtonRelease-1>', self.rsa_decrypt_files)

        # ECC encrypt and decrypt
        self.btnOpenECCFolder.bind('<ButtonRelease-1>', lambda event: self.open_folder(mode='ECC', event=event))
        self.btnOpenECCFile.bind('<ButtonRelease-1>', lambda event: self.open_file(mode='ECC', event=event))
        self.btnECCSignature.bind('<ButtonRelease-1>', self.ecc_signature_files)
        self.btnECCVerify.bind('<ButtonRelease-1>', self.ecc_verify_files)

    # 開啟資料夾
    def open_folder(self, mode='', event=None):
        self.folder_path = filedialog.askdirectory(initialdir='.')
        self.folder_name = os.path.basename(self.folder_path)
        if mode == 'AES':
            self.txtAesLog.delete('1.0', 'end')
            self.txtAesLog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
        if mode == 'RSA':
            self.txtRSALog.delete('1.0', 'end')
            self.txtRSALog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
        if mode == 'ECC':
            self.txtECCLog.delete('1.0', 'end')
            self.txtECCLog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
    
    # 開啟檔案
    def open_file(self, mode='', event=None):
        self.file_path= filedialog.askopenfilename(initialdir='.')
        self.file_name = os.path.basename(self.file_path)
        if mode == 'AES':
            self.txtAesLog.delete('1.0', 'end')
            self.txtAesLog.insert('end', '選擇的檔案： '+ self.file_name +'\n')
        if mode == 'RSA':
            self.txtRSALog.delete('1.0', 'end')
            self.txtRSALog.insert('end', '選擇的檔案： '+ self.file_name +'\n')
        if mode == 'ECC':
            self.txtECCLog.delete('1.0', 'end')
            self.txtECCLog.insert('end', '選擇的檔案： '+ self.file_name +'\n')
    
    # 取得資料夾(不會遞迴子資料夾)
    def get_dirlist(self, path):
        self.dirlist = os.listdir(path)
        self.dirlist.sort()
        return self.dirlist

    # 印資料夾及下面的檔案
    # 對資料夾進行的操作
    def print_files(self, path, mode, prefix='', isprint=1, namelist=[], op_mode=''):
        # path : file_path or folder_path
        # mode: ECC op_mode : sign
        if prefix == '':
            # 17A-da-114-en和17A-da-114-de
            if op_mode == 'de':
                if os.path.isdir(path):
                    self.move_folder = self.folder_name.replace('en','de')
                    self.now_folder = self.move_folder
                else:
                    # path : encrypted_data
                    self.create_files(path, mode, op_mode)
                    return
                    
            if op_mode == 'en':
                if os.path.isdir(path):
                    # 建立要移動到的資料夾
                    self.move_folder = f'{self.folder_name}-{self.year}-' + mode + '-' + op_mode
                    # 目前資料夾
                    self.now_folder = self.move_folder
                else:
                    # path : file_path
                    # 裡面的sub_folder會變檔案
                    self.create_files(path, mode, op_mode)
                    return

            if op_mode == 'sign':
                if os.path.isdir(path):
                    self.move_folder = f'{self.folder_name}-{self.year}-' + mode
                    # 建立要移動到的資料夾
                    # 目前資料夾
                    self.ecc_folder = self.move_folder
                else:
                    # path : file_path
                    self.create_folder_files(path, '', mode, '', '', op_mode)
                    return

            if not os.path.exists(self.move_folder):
                os.makedirs(self.move_folder)

            if isprint:
                print('Folder listing for <{}>'.format(path))
                print('-'*40)
            prefix='| '
    
        print('prefix', prefix)
        # path: C:/Users/Eric/Desktop/mycode/ppy3/17A-da
        # path中的資料夾及檔案
        self.dirlist = self.get_dirlist(path)
        print(self.dirlist)
        # f: da01 ~ da15
        for f in self.dirlist:
            # fullname: 資料夾路徑+裡面資料夾或檔案路徑
            self.fullname = os.path.join(path, f)
            # new_path:資料夾中的資料夾路徑
            if op_mode == 'sign':
                new_path = os.path.join(self.move_folder, f)
                self.create_folder_files(new_path, self.fullname, mode, self.move_folder, f, op_mode)
            else:
                print('full:',self.fullname)
                if os.path.isdir(self.fullname):
                    # 建立子資料夾
                    self.now_folder = self.create_folder(self.fullname, self.move_folder, f)
                    # print('new:',self.now_folder)
                    if isprint:
                        print('{}<{}>'.format(prefix, f))
                    namelist.append(f'{prefix}<資料夾> {f}')
                    self.print_files(self.fullname, mode, prefix*2, isprint, namelist, op_mode)

                else:
                    # 建立檔案
                    print(self.fullname, self.move_folder)
                    print('now', self.now_folder)
                    self.create_folder_files(path, self.fullname, mode, self.move_folder, f, op_mode)
                    if isprint:
                        print(prefix + f)
                    namelist.append(f'{prefix}檔案： {f}')

        return namelist
    
    # 建立加密資料夾
    def create_folder(self, fullname, folder, file, event=None):
        self.sub_folder = os.path.join(folder, file)
        print(self.sub_folder)
        # 檢查舊路徑是否為資料夾，是的話建立子資料夾
        if os.path.isdir(fullname):
            os.mkdir(self.sub_folder)
        
        return self.sub_folder

    def create_files(self, path, mode, operation_mode, event=None):
        if os.path.isfile(path):
            if operation_mode == 'en':
                print('path',path)
                # 檔名、副檔名
                file,ext = os.path.splitext(path)
                if not os.path.exists(file):
                    os.mkdir(file)
                
                self.enc_file = file
                # 要新增加密檔案的檔名
                file_path = os.path.join(file, self.file_name +f'.{mode.lower()}{self.mopAesSelected.get().lower()}enc')
                with open(path, 'r', encoding='utf-8') as src_file:
                    plain_data = src_file.read()

                    if mode == 'AES':
                        plain_data = plain_data.encode('utf-8')
                        encrypted_data = self.aes_encrypt(plain_data)
                        with open(file_path, 'wb') as dest_file:
                            dest_file.write(encrypted_data)
                    
                    if mode == 'RSA':
                        # 讀取
                        with open("rsa_private_key.pem", "rb") as f:
                            private_key_bytes = f.read()
                        with open("rsa_public_key.pem", "rb") as f:
                            public_key_bytes = f.read()
                        # 轉成 RSA key 
                        self.private_key = RSA.import_key(private_key_bytes)
                        self.public_key = RSA.import_key(public_key_bytes)

                        plain_data = plain_data.encode('utf-8')
                        encrypted_data = self.rsa_encrypt(plain_data, self.private_key, self.public_key)
                    
                        with open(file_path, 'wb') as dest_file:
                            pickle.dump(encrypted_data, dest_file)

            if operation_mode == 'de':
                # 使用 AES 解密
                if mode == 'AES':
                    with open(path, 'rb') as src_file:
                        encrypted_data = src_file.read()
                    decrypted_data = self.aes_decrypt(encrypted_data)
                    decrypted_data = decrypted_data.decode('utf-8')
                    base, ext = os.path.splitext(path)
                    # 寫入的檔案路徑
                    file_path = base
                    # 印在text上會用到此變數
                    self.dec_file = file_path
    
                # 使用 RSA 解密
                if mode == 'RSA':
                    # 讀取
                    with open("rsa_private_key.pem", "rb") as f:
                        private_key_bytes = f.read()

                    # 轉成 RSA key 
                    self.private_key = RSA.import_key(private_key_bytes)
                    with open(path, 'rb') as f:
                        self.encrypted_data = pickle.load(f)
                        decrypted_data = self.rsa_decrypt(self.encrypted_data, self.private_key)

                    file_path = path.replace(f'.{mode.lower()}{self.mopAesSelected.get().lower()}enc', '')
                    self.dec_file =  file_path

                with open(file_path, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(decrypted_data)
  
    # 新增加密或解密檔案至子資料夾
    def create_folder_files(self, path, fullname, mode, move_folder, file, operation_mode, event=None):
        # 是否為檔案
        if os.path.isfile(fullname) and operation_mode != 'sign':
            if operation_mode == 'en':      
                with open(fullname, 'r', encoding='utf-8') as src_file:
                    plain_data = src_file.read()
                    # 使用 AES 加密
                    if mode == 'AES':
                        file_path = os.path.join(move_folder, file + f'.{mode.lower()}{self.mopAesSelected.get().lower()}enc')
                        plain_data = plain_data.encode('utf-8')
                        self.encrypted_data = self.aes_encrypt(plain_data)
                        with open(file_path, 'wb') as dest_file:
                            dest_file.write(self.encrypted_data)

                    # 使用 RSA 加密
                    if mode == 'RSA':
                        file_path = os.path.join(move_folder, file + f'.{mode.lower()}oaepenc')
                        # 讀取
                        with open("rsa_private_key.pem", "rb") as f:
                            private_key_bytes = f.read()
                        with open("rsa_public_key.pem", "rb") as f:
                            public_key_bytes = f.read()
                        # 轉成 RSA key 
                        self.private_key = RSA.import_key(private_key_bytes)
                        self.public_key = RSA.import_key(public_key_bytes)

                        plain_data = plain_data.encode('utf-8')
                        self.encrypted_data = self.rsa_encrypt(plain_data, self.private_key, self.public_key)

                        with open(file_path, 'wb') as dest_file:
                            pickle.dump(self.encrypted_data, dest_file)

            if operation_mode == 'de':
                file_path = os.path.join(move_folder, file)
                # with open(fullname, 'rb') as src_file:
                #     cipher_data = src_file.read()

                # 使用 AES 解密
                if mode == 'AES':
                    with open(fullname, 'rb') as src_file:
                        encrypted_data = src_file.read()
                    # print('out encrypted_data', len(encrypted_data))
                    decrypted_data = self.aes_decrypt(encrypted_data)
                    decrypted_data = decrypted_data.decode('utf-8')
                    base, ext = os.path.splitext(file_path)
                    file_path = base
                    with open(file_path, 'w', encoding='utf-8') as dest_file:
                        dest_file.write(decrypted_data)
    
                # 使用 RSA 解密
                if mode == 'RSA':
                    # 讀取
                    with open("rsa_private_key.pem", "rb") as f:
                        private_key_bytes = f.read()

                    # 轉成 RSA key 
                    self.private_key = RSA.import_key(private_key_bytes)
                    file_path = file_path.replace('de', 'en')
                    with open(file_path, 'rb') as f:
                        self.encrypted_data = pickle.load(f)
                        decrypted_data = self.rsa_decrypt(self.encrypted_data, self.private_key)

                    # print(type(decrypted_data))

                    file_path = file_path.replace(f'.{mode.lower()}oaepenc', '').replace('en','de')
                    with open(file_path, 'w', encoding='utf-8') as dest_file:
                        dest_file.write(decrypted_data)

                    # # print(cipher_data)
                    # # print(len(cipher_data))
                    # with open('encrypted_data.pkl','rb') as f:
                    #     self.encrypted_data = pickle.load(f)

        # 執行sign的操作並新增.sig .sha檔案
        else:
            # 讀取
            with open("ecc_private_key.pem", "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                        f.read(),
                        password=None,
                 )
            # 如果是檔案，就執行對檔案簽章的操作
            if os.path.isfile(path):
                ext = os.path.splitext(self.file_name)[1]

                print('path', path)
                self.signature ,self.file_sha = self.ecc_signature(path, self.private_key, f='file')
                sha_path = path.replace(ext, '.sha')
                file_path = path.replace(ext, '.sig')
                self.sign_file = file_path
                print('file_sha: ', self.file_sha)
                with open(file_path, 'wb') as dest_file:
                        dest_file.write(self.signature)

                with open(sha_path, 'wb') as dest_file:
                        dest_file.write(self.file_sha)

            # 如果是資料夾，就執行對資料夾簽章的操作
            else:
                self.signature = self.ecc_signature(path, self.private_key, f='folder')
                self.folder_path = os.path.join(move_folder, self.ecc_folder+'.sig')
                self.folder_sha = os.path.join(move_folder, self.ecc_folder+'.sha')
                self.sign_file = self.folder_path
                with open(self.folder_path, 'wb') as dest_file:
                        dest_file.write(self.signature)
   
    # 新增aes加密資料夾
    def aes_encrypt_files(self, event=None):
        # 若還未選擇資料夾或檔案
        if not self.folder_path and not self.file_path:
            messagebox.showwarning("提示", "請先選擇資料夾或檔案")
            return
        else:
            self.mode = self.tabs.tab(self.tabs.select(), "text")
            if self.file_path:
                self.name = self.print_files(self.file_path, self.mode, isprint=0, op_mode='en')
                self.add_aes_message(mode='en')
                # 加密完後路徑清空
                self.file_path = ''
            if self.folder_path:
                self.files_name = []
                self.name = self.print_files(self.folder_path, self.mode, isprint=0, namelist=self.files_name, op_mode='en')
                self.add_aes_message(mode='en')
                # 加密完後路徑清空
                self.folder_path = ''
    
    # 新增aes解密資料夾
    def aes_decrypt_files(self, event=None):
        # 若還未選擇資料夾或檔案
        if not self.folder_path and not self.file_path:
            messagebox.showwarning("提示", "請先選擇資料夾或檔案")
            return
        else:
            self.mode = self.tabs.tab(self.tabs.select(), "text")
            if self.file_path:
                # file_path: encrypted file
                self.name = self.print_files(self.file_path, self.mode, isprint=0, op_mode='de')
                self.add_aes_message(mode='de')
                # 加密完後路徑清空
                self.file_path = ''
            if self.folder_path:
                self.files_name = []
                # folder_path: encrypted folder
                self.name = self.print_files(self.folder_path, self.mode, isprint=0, namelist=self.files_name, op_mode='de')
                self.add_aes_message(mode='de')
                # 加密完後路徑清空
                self.folder_path = ''

    # 新增rsa加密資料夾
    def rsa_encrypt_files(self, event=None):
        # 若還未選擇資料夾或檔案
        if not self.folder_path and not self.file_path:
            messagebox.showwarning("提示", "請先選擇資料夾或檔案")
            self.txtRSALog.delete('1.0', 'end')
            return
        else:
            # 產生 RSA 金鑰對
            self.key = RSA.generate(int(self.klRSASelected.get()))
            self.rsa_private_key = self.key
            self.rsa_public_key = self.key.publickey()

            # 轉為 bytes (使用pycryptdome)
            private_key_bytes = self.rsa_private_key.export_key()
            public_key_bytes = self.rsa_public_key.export_key()

            # 儲存到檔案
            with open("rsa_private_key.pem", "wb") as f:
                f.write(private_key_bytes)
            with open("rsa_public_key.pem", "wb") as f:
                f.write(public_key_bytes)

            self.mode = self.tabs.tab(self.tabs.select(), "text")
            if self.file_path:
                self.name = self.print_files(self.file_path, self.mode, isprint=0, op_mode='en')
                self.add_rsa_message(mode='en')
                # 加密完後路徑清空
                self.file_path = ''
            if self.folder_path:
                self.files_name = []
                self.name = self.print_files(self.folder_path, self.mode, isprint=0, namelist=self.files_name, op_mode='en')
                self.add_rsa_message(mode='en')
                # 加密完後路徑清空
                self.folder_path = ''
    
    # 新增rsa解密資料夾
    def rsa_decrypt_files(self, event=None):
        # 若還未選擇資料夾或檔案
        if not self.folder_path and not self.file_path:
            messagebox.showwarning("提示", "請先選擇資料夾或檔案")
            self.txtRSALog.delete('1.0', 'end')
            return
        else:
            self.mode = self.tabs.tab(self.tabs.select(), "text")
            if self.file_path:
                # file_path : 加密的檔案
                self.name = self.print_files(self.file_path, self.mode, isprint=0, op_mode='de')
                self.add_rsa_message(mode='de')
                # 加密完後路徑清空
                self.file_path = ''
            if self.folder_path:
                self.files_name = []
                self.name = self.print_files(self.folder_path, self.mode, isprint=0, namelist=self.files_name, op_mode='de')
                self.add_rsa_message(mode='de')
                # 加密完後路徑清空
                self.folder_path = ''

    # 新增ecc加密資料夾
    def ecc_signature_files(self, event=None):
        # 若還未選擇資料夾
        if not self.folder_path and not self.file_path:
            messagebox.showwarning("提示", "請先選擇資料夾或檔案")
            self.txtECCLog.delete('1.0', 'end')
            return
        else:
            # 生成 ECC 密鑰對
            self.ecc_private_key = ec.generate_private_key(ec.SECP256R1())  # 使用 SECP256R1 曲線
            self.ecc_public_key = self.ecc_private_key.public_key()

             # 將私鑰與公鑰序列化以便儲存
            ecc_private_pem = self.ecc_private_key.private_bytes(
                # 哪種格式 PEM: Base64編碼
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                # 私鑰序列化時使用，私鑰是否要密碼
                encryption_algorithm=serialization.NoEncryption()
            )

            ecc_public_pem = self.ecc_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # 將金鑰儲存到檔案
            with open("ecc_private_key.pem", "wb") as f:
                f.write(ecc_private_pem)
            with open("ecc_public_key.pem", "wb") as f:
                f.write(ecc_public_pem)

            # mode : ECC
            self.mode = self.tabs.tab(self.tabs.select(), "text")
            self.files_name = []
            if self.folder_path:
                self.name = self.print_files(self.folder_path, self.mode, isprint=0, namelist=self.files_name, op_mode='sign')
            
            if self.file_path:
                self.name = self.print_files(self.file_path, self.mode, isprint=0, namelist=self.files_name, op_mode='sign')
            self.add_ecc_message(mode='sign')
            # 簽章完後路徑清空
            self.folder_path = ''
            self.file_path = ''
    
    # 新增ecc驗證
    def ecc_verify_files(self, event=None):
        # 若還未選擇資料夾
        if not self.folder_path and not self.file_path:
            messagebox.showwarning("提示", "請先選擇資料夾或檔案")
            self.txtECCLog.delete('1.0', 'end')
            return
        else:
            with open("ecc_public_key.pem", "rb") as f:
                self.ecc_public_key_bytes = f.read()

            self.ecc_public_key = serialization.load_pem_public_key(
                                    self.ecc_public_key_bytes,
                                    backend=default_backend()
                                    )
            
            mode = self.tabs.tab(self.tabs.select(), "text")
            sign_file = os.path.basename(self.folder_path)
            print(sign_file)
            # sign_path = os.path.join(f'{sign_file}-{self.year}-{mode}', f'{sign_file}-{self.year}-{mode}.sig')
            sign_path = os.path.join(f'{sign_file}', f'{sign_file}.sig')
            print(sign_path)
            with open(sign_path, 'rb') as f:
                signature = f.read()

            # 對檔案進行簽章
            if self.file_path:
                new_file_hash = hashlib.sha256()
                with open(self.file_path, 'rb') as f:
                    while chunk := f.read(4096):
                        new_file_hash.update(chunk)
                        
                # 進行驗證
                self.verify = self.verify_signature(self.ecc_public_key, new_file_hash, signature)
                self.add_ecc_message(mode='verify')
                self.file_path = ''

            if self.folder_path:
                new_combined_hash = hashlib.sha256()
                for root, dirs, files in sorted(os.walk(self.folder_path)):
                    for file in sorted(files):  # 按檔案名稱排序
                        file_path = os.path.join(root, file)
                        new_combined_hash.update(file_path.encode('utf-8'))
                        with open(file_path, "rb") as f:
                            while chunk := f.read(4096):
                                new_combined_hash.update(chunk)
                    
                # 進行驗證
                self.verify = self.verify_signature(self.ecc_public_key, new_combined_hash.digest(), signature)
                self.add_ecc_message(mode='verify')
                self.folder_path = ''

    # 用aes將檔案進行加密
    def aes_encrypt(self, file_data,event=None): 
        # 選擇密鑰長(變bytes)
        self.keyAesselect = int(self.klAesSelected.get()) // 8
        if not self.key:
            # 產生金鑰
            self.key = get_random_bytes(self.keyAesselect)
        # 使每次加密的密文都不相同
        iv = get_random_bytes(16)
        # 將資料填充到16的倍數
        data_padded = pad(file_data, AES.block_size)
        # CBC、CFB、EAX
        self.mode = self.mopAesSelected.get()
    
        # CBC加密
        if self.mode == self.optAesModeofOp[0]:
            # cipher: 加密器
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            self.cipher_data = cipher.encrypt(data_padded)
            return iv + self.cipher_data 
        # CFB加密
        if self.mode == self.optAesModeofOp[1]:
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            self.cipher_data = cipher.encrypt(data_padded)
            return iv + self.cipher_data 
        # EAX加密(和CBC、CFB不同)
        if self.mode == self.optAesModeofOp[2]:
            cipher = AES.new(self.key, AES.MODE_EAX, iv)
            # tag：驗證碼，解密時會用tag驗證資料是否完整
            self.cipher_data, tag = cipher.encrypt_and_digest(file_data)
            # cipher.nonce: EAX的IV
            return cipher.nonce + tag + self.cipher_data

    # 用AES將檔案進行解密
    def aes_decrypt(self, encrypted_data, event=None):
        mode = self.mopAesSelected.get()
        if mode == 'CBC':
            # 因為加密時return iv + ct
            # 前16位為IV
            iv = encrypted_data[:AES.block_size]
            data = encrypted_data[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data =  unpad(cipher.decrypt(data), AES.block_size)

        elif mode == 'CFB':
            iv = encrypted_data[:AES.block_size]
            data = encrypted_data[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            decrypted_data =  unpad(cipher.decrypt(data), AES.block_size)
        elif mode == 'EAX':
            nonce = encrypted_data[:AES.block_size]
            tag = encrypted_data[AES.block_size:AES.block_size+16]
            data = encrypted_data[AES.block_size+16:] 
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            decrypted_data =  cipher.decrypt_and_verify(data, tag)

        return decrypted_data

    # 用rsa將檔案進行加密
    def rsa_encrypt(self, file_data, key, public_key, event=None):
        # 定義 RSA 加密的最大塊大小(42)
        # 填充42的空間
        block_size = key.size_in_bytes() -42

        # 分割訊息
        chunks = []
        for i in range(0, len(file_data), block_size):
            chunks.append(file_data[i:i + block_size])

        # 建立加密器
        encryptor = PKCS1_OAEP.new(public_key)

        # 加密每個塊
        encrypted_chunks = []
        for chunk in chunks:
            encrypted_chunk = encryptor.encrypt(chunk)
            encrypted_chunks.append(encrypted_chunk)

        return encrypted_chunks

    # 用RSA將檔案進行解密
    def rsa_decrypt(self, encrypt_data, private_key, event=None):
        # 建立解密器
        decryptor = PKCS1_OAEP.new(private_key)
        decrypted_chunks = []

        for chunk in encrypt_data:   
            decrypted_chunk = decryptor.decrypt(chunk)
            decrypted_chunks.append(decrypted_chunk)

        # 合併解密後的區塊
        decrypted_data = b''.join(decrypted_chunks)
        decrypted_data = decrypted_data.decode('utf-8')

        return decrypted_data

    # 生成 ECDSA 金鑰對
    # 使用 ECDSA 進行簽名
    def ecc_signature(self, folder_path, private_key, f='', evevt=None):
        # 對檔案進行簽章
        if f == 'file':
            file_hash = hashlib.sha256()
            with open(folder_path, 'rb') as f:
                while chunk := f.read(4096):
                    file_hash.update(chunk)

            signature = private_key.sign(
                file_hash.digest(),
                ec.ECDSA(hashes.SHA256())
            )

            return signature

        if f == 'folder':
            combined_hash = hashlib.sha256()
            for root, dirs, files in sorted(os.walk(folder_path)):
                for file in sorted(files):  # 按檔案名稱排序
                    file_path = os.path.join(root, file)
                    combined_hash.update(file_path.encode('utf-8'))
                    with open(file_path, "rb") as f:
                        while chunk := f.read(4096):
                            combined_hash.update(chunk)

            signature = private_key.sign(
                combined_hash.digest(),
                ec.ECDSA(hashes.SHA256())
            )

            return signature

    # 驗證
    def verify_signature(self, public_key, message, signature, event=None):
        try:
            public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    def add_aes_message(self, mode='', event=None):
        if self.folder_path:
            self.txtAesLog.delete('1.0', 'end')
            self.txtAesLog.insert('end', '選擇的路徑： '+ self.folder_path +'\n')
            self.txtAesLog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
            self.txtAesLog.insert('end', '使用的加密演算法： '+ self.tabs.tab(self.tabs.select(), "text") +'\n')
            self.txtAesLog.insert('end', '密鑰長度： '+self.klAesSelected.get() +'\n')
            
            if mode == 'en':
                self.txtAesLog.insert('end', '加密模式：'+ self.mopAesSelected.get() + '\n')
                self.txtAesLog.insert('end', '加密到哪裡：' + self.move_folder+'\n')
                self.txtAesLog.insert('end', '加密的檔案如下：'+'\n')
                for n in self.name:
                    self.txtAesLog.insert('end', n +'\n')
 
            if mode == 'de':
                self.txtAesLog.insert('end', '解密模式： '+ self.mopAesSelected.get() + '\n')
                self.txtAesLog.insert('end', '解密到哪裡：' + self.move_folder +'\n')
                self.txtAesLog.insert('end', '解密的檔案如下：'+'\n')
                for n in self.name:
                    self.txtAesLog.insert('end', n +'\n')
                
        if self.file_path:
            self.txtAesLog.delete('1.0', 'end')
            self.txtAesLog.insert('end', '選擇的路徑： '+ self.file_path +'\n')
            self.txtAesLog.insert('end', '選擇的檔案： '+ self.file_name +'\n')
            self.txtAesLog.insert('end', '使用的加密演算法： '+ self.tabs.tab(self.tabs.select(), "text") +'\n')
            self.txtAesLog.insert('end', '密鑰長度： '+self.klAesSelected.get() +'\n')
            if mode == 'en':
                self.txtAesLog.insert('end', '加密模式： '+ self.mopAesSelected.get() + '\n')
                self.txtAesLog.insert('end', '加密到哪裡：' + self.enc_file+'\n')
    
            if mode == 'de':
                self.txtAesLog.insert('end', '解密模式： '+ self.mopAesSelected.get() + '\n')
                self.txtAesLog.insert('end', '解密到哪裡：' + self.dec_file +'\n')

    def add_rsa_message(self, mode='', event=None):
        if self.folder_path:
            self.txtRSALog.delete('1.0', 'end')
            self.txtRSALog.insert('end', '選擇的路徑： '+ self.folder_path +'\n')
            self.txtRSALog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
            self.txtRSALog.insert('end', '使用的加密演算法： '+ self.tabs.tab(self.tabs.select(), "text") +'\n')
            self.txtRSALog.insert('end', '密鑰長度： '+self.klAesSelected.get() +'\n')
            if mode == 'en':
                self.txtRSALog.insert('end', '加密模式： OAEP'+'\n')
                self.txtRSALog.insert('end', '加密到哪裡：' + self.move_folder+'\n')
                self.txtRSALog.insert('end', '加密的檔案如下：'+'\n')
                for n in self.name:
                    self.txtRSALog.insert('end', n +'\n')
            if mode == 'de':
                self.txtRSALog.insert('end', '解密模式： OAEP'+'\n')
                self.txtRSALog.insert('end', '解密到哪裡：' + self.move_folder +'\n')

        if self.file_path:
            self.txtRSALog.delete('1.0', 'end')
            self.txtRSALog.insert('end', '選擇的路徑： '+ self.file_path +'\n')
            self.txtRSALog.insert('end', '選擇的檔案： '+ self.file_name +'\n')
            self.txtRSALog.insert('end', '使用的加密演算法： '+ self.tabs.tab(self.tabs.select(), "text") +'\n')
            self.txtRSALog.insert('end', '密鑰長度： '+self.klAesSelected.get() +'\n')
            if mode == 'en':
                self.txtRSALog.insert('end', '加密模式： OAEP'+'\n')
                self.txtRSALog.insert('end', '加密到哪裡：' + self.enc_file+'\n')
            if mode == 'de':
                self.txtRSALog.insert('end', '解密模式： OAEP'+'\n')
                self.txtRSALog.insert('end', '解密到哪裡：' + self.dec_file +'\n')

    def add_ecc_message(self, mode='', event=None):
        self.txtECCLog.delete('1.0', 'end')
        if mode == 'sign':
            if self.folder_path:
                self.txtECCLog.insert('end', '選擇的路徑： '+ self.folder_path +'\n')
                self.txtECCLog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
            if self.file_path:
                self.txtECCLog.insert('end', '選擇的路徑： '+ self.file_path +'\n')
                self.txtECCLog.insert('end', '選擇的檔案： '+ self.file_name +'\n')    
            self.txtECCLog.insert('end', '使用的加密演算法： '+ self.tabs.tab(self.tabs.select(), "text") +'\n')
            self.txtECCLog.insert('end', '選擇的橢圓曲線： '+self.mopECCSelected.get() +'\n')
            self.txtECCLog.insert('end', '簽章儲存位置：' + self.sign_file +'\n')

        if mode == 'verify':
            if self.folder_path:
                self.txtECCLog.insert('end', '選擇的路徑： '+ self.folder_path +'\n')
                self.txtECCLog.insert('end', '選擇的資料夾： '+ self.folder_name +'\n')
            if self.file_path:
                self.txtECCLog.insert('end', '選擇的路徑： '+ self.file_path +'\n')
                self.txtECCLog.insert('end', '選擇的檔案： '+ self.file_name +'\n')   
            if self.verify:
                self.txtECCLog.insert('end', '驗證結果： 驗證成功' +'\n')
            else:
                self.txtECCLog.insert('end', '驗證結果： 驗證成功，資料無變動' +'\n')

    def send_messages(self, event=None):
        print(self.folder_name)

    def quit_app(self, event=None):
        if messagebox.askokcancel('關閉', '確定離開？'):
            self.master.destroy()

twin = Tk()
app = Application(master=twin)
app.mainloop()