import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog, LEFT
from tkinter import messagebox
from tkinter import *

HOST = '127.0.0.1'
PORT = 50002


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        msg = tkinter.Tk()
        msg.withdraw()

        self.gui = False
        self.running = True
        self.connectedTCP = False

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.geometry('550x600')
        canvas = Canvas(
            self.win,
            bg="#ffffff",
            height=600,
            width=550,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(file=f"../Messanger_Project/GUI/background.png", master=self.win)
        background = canvas.create_image(
            278.0, 299.0,
            image=background_img)

        entry0_img = PhotoImage(file=f"../Messanger_Project/GUI/img_textBox0.png", master=self.win)
        entry0_bg = canvas.create_image(
            352.5, 504.0,
            image=entry0_img)

        self.input_area = Entry(
            bd=0,
            bg="#d4cbcb",
            highlightthickness=0
            , master=self.win)

        self.input_area.place(
            x=193.0, y=478,
            width=319.0,
            height=50
        )

        entry1_img = PhotoImage(file=f"../Messanger_Project/GUI/img_textBox1.png", master=self.win)
        entry1_bg = canvas.create_image(
            81.0, 504.0,
            image=entry1_img)

        self.private_dest = Entry(
            bd=0,
            bg="#d4cbcb",
            highlightthickness=0, master=self.win)

        self.private_dest.place(
            x=34.0, y=478,
            width=94.0,
            height=50)

        entry2_img = PhotoImage(file=f"../Messanger_Project/GUI/img_textBox2.png", master=self.win)
        entry2_bg = canvas.create_image(
            279.0, 40.0,
            image=entry2_img)

        self.nickname_entrace = Entry(
            bd=0,
            bg="#d4cbcb",
            highlightthickness=0, master=self.win)

        self.nickname_entrace.place(
            x=240.0, y=25,
            width=78.0,
            height=28)

        entry3_img = PhotoImage(file=f"../Messanger_Project/GUI/img_textBox3.png", master=self.win)
        entry3_bg = canvas.create_image(
            466.5, 40.0,
            image=entry3_img)

        entry3 = Entry(
            bd=0,
            bg="#d4cbcb",
            highlightthickness=0, master=self.win)

        entry3.place(
            x=428.0, y=25,
            width=77.0,
            height=28)

        img1 = PhotoImage(file=f"../Messanger_Project/GUI/img1.png", master=self.win)
        self.login_btn = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat", master=self.win)

        self.login_btn.place(
            x=8, y=13,
            width=120,
            height=50)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.config(state='disabled', bg='lightgray')
        self.text_area.place(x=21, y=68,
                             width=502,
                             height=373)

        img0 = tkinter.PhotoImage(file=f"../Messanger_Project/GUI/img0.png", master=self.win)
        self.send_btn = tkinter.Button(
            self.win,
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.write,
            relief="flat")

        self.send_btn.place(
            x=-9, y=542,
            width=120,
            height=50)

        img2 = PhotoImage(file=f"../Messanger_Project/GUI/img2.png", master=self.win)
        self.showOnline_btn = Button(
            image=img2,
            borderwidth=0,
            highlightthickness=0,
            command=self.showOnline,
            relief="flat", master=self.win)

        self.showOnline_btn.place(
            x=112, y=545,
            width=108,
            height=49)

        img3 = PhotoImage(file=f"../Messanger_Project/GUI/img3.png", master=self.win)
        self.ShowFiles_btn = Button(
            image=img3,
            borderwidth=0,
            highlightthickness=0,
            command=self.showFiles,
            relief="flat", master=self.win)

        self.ShowFiles_btn.place(
            x=221, y=547,
            width=104,
            height=50)

        img4 = PhotoImage(file=f"../Messanger_Project/GUI/img4.png", master=self.win)
        self.download_btn = Button(
            image=img4,
            borderwidth=0,
            highlightthickness=0,
            command=self.askFile,
            relief="flat", master=self.win)

        self.download_btn.place(
            x=326, y=548,
            width=110,
            height=50)
        img5 = PhotoImage(file=f"../Messanger_Project/GUI/img5.png", master=self.win)
        self.disconnect_btn = Button(
            image=img5,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop,
            relief="flat", master=self.win)

        self.disconnect_btn.place(
            x=436, y=547,
            width=107,
            height=43)

        self.gui = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def showOnline(self):
        self.sock.send("get_users".encode('utf-8'))

    def write(self):
        print(self.private_dest.get())
        if self.private_dest.get() == "":
            message = f"{self.nickname} : {self.input_area.get()}\n"
        else:
            message = f"{self.nickname} : /{self.private_dest.get()} {self.input_area.get()}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('0', 'end')

    def showFiles(self):
        self.sock.send("show_files".encode('utf-8'))

    def stop(self):
        self.win.destroy()
        self.sock.send(f"{self.nickname} has disconnected!".encode('utf-8'))
        self.running = False
        self.sock.close()
        exit(0)


    def askFile(self):
        filename = simpledialog.askstring("File", "Enter file name:", parent=self.win)
        savingFileName = simpledialog.askstring("File", "Save as ?:", parent=self.win)
        self.sock.send(f"{self.nickname} : /download {filename} {savingFileName}\n".encode('utf-8'))

    def recieve(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                messageCheck = message.split(" ")
                print(messageCheck)

                if messageCheck[0] == '/download':
                    print("LOL")
                    port = int(messageCheck[2])
                    self.sockUDP.connect((messageCheck[1], port))
                    filename = messageCheck[3]
                    fileSize = int(messageCheck[4])

                    self.sockUDP.sendto("Connected received !".encode(), (messageCheck[1], port))
                    getFile_thread = threading.Thread(target=self.recieveFile , args=[filename , fileSize])
                    getFile_thread.start()
                    # self.recieveFile(filename, fileSize)
                    if self.gui:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', f"{filename} downloaded !\n")
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')


                elif message == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                pass

    def recieveFile(self, filename, fileSize):
        dataList = []

        while fileSize != 0:
            bytes_read, _ = self.sockUDP.recvfrom(2053)
            if bytes_read not in dataList:
                dataList.append(bytes_read)
                self.sockUDP.sendto(f'ack'.encode(), _)
                fileSize -= len(bytes_read)
            else:
                self.sockUDP.sendto(f'ack'.encode(), _)

            if not bytes_read:
                break



        with open(filename, 'wb') as f:
            for elem in dataList:
                f.write(elem)




    def login(self):
        if self.connectedTCP == False:
            self.nickname = self.nickname_entrace.get()
            self.sock.connect((HOST, PORT))
            self.connectedTCP = True
            recieve_thread = threading.Thread(target=self.recieve)
            recieve_thread.start()


client = Client(HOST, PORT)

