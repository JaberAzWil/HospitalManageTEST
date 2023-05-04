try:
    from TKinter import *   
except ImportError:
    from tkinter import *   
    import tkinter as tk
import sqlite3
import tkinter.messagebox
import os, sys, webbrowser, time
from PIL import Image, ImageTk
from tkinter import ttk
import smtplib, random, string, socket
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

conn = sqlite3.connect('database.db')
c = conn.cursor()

class App:
    def __init__(self, master):
        self.master = master

        # menu bar
        Chooser = Menu()
        itemone = Menu()
        
        Chooser.add_command(label='Quitter', command=lambda: exitRoot(root))

        root.config(menu=Chooser)
        
        self.loginLabel = Label(text="\nConnecter vous\n", font=('arial 14 bold'), fg='black')
        self.loginLabel.pack()

        # login ID
        self.login_id = Label(text="LOGIN*", font=('arial 12'), fg='black')
        self.login_id.place(x=60, y=70)

        # password
        self.password = Label(text="Mot de passe*", font=('arial 12'), fg='black')
        self.password.place(x=60, y=120)

        # entries for labels
        self.login_id_ent = Entry(width=20)
        self.login_id_ent.place(x=280, y=72)

        self.password_ent = Entry(width=20, show='*')
        self.password_ent.place(x=280, y=122)

        # button for reset password
        self.reset_password = Button(text="Mot de passe oublié ?", bg='#aed4eb', command=self.reset_pass)
        self.reset_password.place(x=310, y=160)

        # button to login
        self.loginShield = PhotoImage(file = "resources/user-shield-100.png")
        self.buttonImage = self.loginShield.subsample(3, 3)
        self.submit = Button(text = 'Connexion', image=self.buttonImage, compound=LEFT, width=120, height=40, bg='steelblue', command=self.login)
        self.submit.place(x=170, y=200)

        # button for guest login
        self.guestAvatar = PhotoImage(file = "resources/guest.png")
        self.guestImage = self.guestAvatar.subsample(15, 15)
        self.guestButton = Button(text='Connexion en tant que invité',image=self.guestImage, compound=LEFT, width=190, height=40, command=self.guestLogin)
        self.guestButton.place(x=140, y=290)

    # function to login
    def login(self, event):
        self.id = self.login_id_ent.get()
        self.password = self.password_ent.get()
        
        if self.id=="" or self.password=="":
            tkinter.messagebox.showwarning("SVP remplissez tout les champs manquants.")
        else:
            self.login_id_ent.delete(0, END)
            self.password_ent.delete(0, END)
            sql = "SELECT * FROM credentials WHERE id LIKE ?"
            self.input = str(self.id)
            self.res = c.execute(sql, (self.input,))
            for self.row in self.res:
                self.db_name = self.row[1]
                self.db_pass = self.row[2]
                self.db_designation = self.row[3]

            if self.db_pass == self.password:
                tkinter.messagebox.showinfo("Connecter avec succes", "Bonjour "+self.db_name+"! Vous etes connecter en tant que " + self.db_designation)
                self.drawWin()
            else:
                tkinter.messagebox.showerror("Connexion echouer", "Login ou mot de passe invalide! SVP réessayer encore")
                raise ValueError('Connexion echouer')
    
    # function for guest login
    def guestLogin(self):
        self.id = "guest"
        self.db_name = "Guest User"
        self.db_designation = "Guest"

        tkinter.messagebox.showinfo("Connexion réussie", "Bonjour "+self.db_name+"! vous etes connecter en tant que " + self.db_designation)
        self.drawWin()

    #function to draw toplevel window
    def drawWin(self):
        # hiding root window
        hide_root()

        # drawing toplevel window
        top = Toplevel() 
        top.geometry("480x320+360+180") 
        top.title("Welcome") 
        
        # menu bar
        Chooser = Menu()
        itemone = Menu()

        if self.db_designation == 'System Administrator' or self.db_designation == 'Doctor':
            itemone.add_command(label='Ajouter rendez-vous', command=self.appointment)
            itemone.add_command(label='Modifier rendez-vous', command=self.update)
            itemone.add_command(label='Supprimer rendez-vous', command=self.delete)
        
        itemone.add_command(label='Voir rendez-vous', command=self.display)
        itemone.add_separator()
        itemone.add_command(label='Se Deconnecter', command=lambda: self.logout(top))

        Chooser.add_cascade(label='Fichier', menu=itemone)
        Chooser.add_command(label='Voir rendez-vous', command=self.display)
        Chooser.add_command(label='Deconnexion', command=lambda: self.logout(top))

        top.config(menu=Chooser)
        top.iconphoto(False, tk.PhotoImage(file="resources/icon.png"))

        self.left = Frame(top, width=130, height=130, bd=1, relief=RAISED)
        self.left.place(x=5, y=5)

        self.right = Frame(top, width=320, height=150)
        self.right.place(x=150, y=5)

        self.footer = Frame(top, width=480, height=30, bd=1, relief=RAISED, \
            highlightbackground="black", highlightthickness=1)
        self.footer.place(x=0, y=290)

        self.timeLabel = Label(self.footer, text="Connecter à "+time.strftime("%I:%M:%S %p"), font=('arial 10'), fg='black')
        self.timeLabel.place(x=5, y=3)
        
        self.drawImage(top)

        self.userlogin = Label(self.right, text="Vous etes connecter en tant que:", font=('arial 12 bold'), fg='black')
        self.userlogin.place(x=5, y=20)

        self.Name = Label(self.right, text="Nom: " + self.db_name, font=('arial 12'), fg='black')
        self.Name.place(x=5, y=50)

        self.Name = Label(self.right, text="Designation: " + self.db_designation, font=('arial 12'), fg='black')
        self.Name.place(x=5, y=80)

    def destroyTop(self, top):
        top.destroy()

    # function to close the top window
    def logout(self, top):
        MsgBox = tk.messagebox.askquestion('Deconnexion de application','Vous etes sur de vouloir vous deconnecter?', icon='warning')
        if MsgBox == 'yes':
            self.path = self.name + ".jpg"
            self.destroyTop(top)
            show_root()

    # function to open the appointment window    
    def appointment(self):
        if sys.platform.startswith('linux'):
            os.system("python3 appointment.py")
        elif sys.platform.startswith('win32'):
            os.system("python appointment.py")

    # function to open the update window  
    def update(self):
        if sys.platform.startswith('linux'):
            os.system("python3 update.py")
        elif sys.platform.startswith('win32'):
            os.system("python update.py")

    # function to open the display window 
    def display(self):
        if sys.platform.startswith('linux'):
            os.system("python3 display.py")
        elif sys.platform.startswith('win32'):
            os.system("python display.py")

    # function to open the display window  
    def delete(self):
        if sys.platform.startswith('linux'):
            os.system("python3 delete.py")
        elif sys.platform.startswith('win32'):
            os.system("python delete.py")

    def writeTofile(self):
        # Convert binary data to proper format and write it on Hard Disk
        with open(self.photoPath, 'wb') as file:
            file.write(self.photo)

    def drawImage(self, top):
        # function takes image from database and saves it to disk.
        sql_fetch_blob_query = "SELECT * from credentials where id = ?"
        c.execute(sql_fetch_blob_query, (self.id,))
        self.record = c.fetchall()
        for row in self.record:
            # print("Id = ", row[0], "Name = ", row[1])
            self.name  = row[1]
            self.photo = row[4]

            # save file to directory
            self.writeTofile()
            
            self.fileName = self.name + ".jpg"
            file_name = str(self.fileName)

            # draw image on canvas
            self.canvas = Canvas(self.left, width=120, height=120)  
            self.canvas.pack()
            self.img = ImageTk.PhotoImage(Image.open(file_name)) 
            self.canvas.create_image(0,0, anchor=NW, image=self.img)    
            self.canvas.image = self.img

            # deleteProfilePic(self.fileName)
            os.remove(self.fileName)

    def aboutMaster(self):
        about = Toplevel()
        about.geometry("480x320+360+180") 
        about.title("About")
        about.iconphoto(False, tk.PhotoImage(file="resources/icon.png"))

        self.leftAbout = Frame(about, width=130, height=130)
        self.leftAbout.place(x=5, y=30)

        self.rightAbout = Frame(about, width=120, height=250)
        self.rightAbout.place(x=150, y=25)

        self.imgCanvas = Canvas(self.leftAbout, width=120, height=120)  
        self.imgCanvas.pack()
        self.img = PhotoImage(file="resources/icon.png") 
        self.img_sized = self.img.subsample(5,5)
        self.imgCanvas.create_image(8,8, anchor=NW, image=self.img_sized)    
        self.imgCanvas.image = self.img

        self.photo = PhotoImage(file = "resources/github-100.png")
        self.photoimage = self.photo.subsample(3, 3)
       
        self.imgCanvas = Canvas(whatWindow, width=120, height=120)  
        self.imgCanvas.place(x=180, y=20)
        self.img = PhotoImage(file="resources/icon.png") 
        self.img_sized = self.img.subsample(5,5)
        self.imgCanvas.create_image(8,8, anchor=NW, image=self.img_sized)    
        self.imgCanvas.image = self.img

    # function for resetting password
    def reset_pass(self):
        resetWindow = Toplevel()
        resetWindow.geometry("480x320+360+180")
        resetWindow.title("Reinitialiser mot de passe")
        resetWindow.iconphoto(False, tk.PhotoImage(file="resources/icon.png"))

        tabControl = ttk.Notebook(resetWindow)        
        self.secret_ques = ttk.Frame(tabControl) 
        self.otp = ttk.Frame(tabControl) 
        
        tabControl.add(self.secret_ques, text ='Utiliser question secrete') 
        tabControl.add(self.otp, text ='Utiliser Email') 
        tabControl.pack(expand = 1, fill ="both") 

        self.id_label = Label(resetWindow, text="Login*", font=('arial 11'))
        self.id_label.place(x=40, y=50)
        self.id_label_ent = Entry(resetWindow,width=20)
        self.id_label_ent.place(x=170, y=52)

        '''''''''###Secret Question tab###'''''''''
        self.ques_label = Label(self.secret_ques, text="Question secrete*", font=('arial 11'))
        self.ques_label.place(x=40, y=110)

        # list of questions
        OptionList = ["Quel est le nom de votre premier chien?",
        "Quel est le troisieme prenom de votre père?",
        "Quel est votre livre favorie?"
        ]

        # OptionMenu
        self.variable = tk.StringVar(self.secret_ques)
        self.variable.set(OptionList[0])

        self.opt = tk.OptionMenu(self.secret_ques, self.variable, *OptionList)
        self.opt.config(width=30, font=('arial', 11))
        self.opt.place(x=170, y=103)
        self.ques_num = 0

        # callback method
        def callback(*args):  
            for i in range(len(OptionList)):    # assign question number to for query in the database
                if OptionList[i] == self.variable.get():
                    break

            self.ques_num = i
            print(str(self.ques_num)+": "+OptionList[i])

        self.variable.trace("w", callback)

        self.answer = Label(self.secret_ques, text="Votre reponse*", font=('arial 11'))
        self.answer.place(x=40, y=150)

        self.answer_ent = Entry(self.secret_ques, width=20)
        self.answer_ent.place(x=170, y=150)

        self.new_pass = Label(self.secret_ques,text="Nouveau mot de passe*", font=('arial 11'), fg='black')
        self.new_pass.place(x=40, y=190)

        self.new_pass_ent = Entry(self.secret_ques, width=20, show='*')
        self.new_pass_ent.place(x=170, y =190)

        # button to submit the answers
        self.submit_answer = Button(self.secret_ques, text="Soumettre", font=('arial 11'), width=12, height=2, command=self.subAnswerSecretQues)
        self.submit_answer.place(x=150, y=230)

        '''''''''###OTP tab###'''''''''
        self.footer = Frame(self.otp, width=480, height=30, bd=1, relief=RAISED, \
            highlightbackground="black", highlightthickness=1)
        self.footer.place(x=0, y=270)

        self.netStatus = Label(self.footer, text='', font=('arial 11 bold'))
        self.netStatus.place(x=5, y=0)
        updateStatusLabel(self)

        self.emailStatus = Label(self.otp, text='', font=('arial 11 bold'))
        self.emailStatus.place(x=100, y=110)

        self.Sub_loginID = Button(self.otp, text="Soumettre", font=('arial 11'), width=12, command=self.subVeriEmail)
        self.Sub_loginID.place(x=150, y=60)

        self.codeLabel = Label(self.otp, text="Code de verification*", font=('arial 11'))
        self.codeLabel.place(x=40, y=150)

        self.codeLabel_ent = Entry(self.otp, width=20)
        self.codeLabel_ent.place(x=170, y=150)

        self.new_pass_otp = Label(self.otp,text="Nouveau mot de passe*", font=('arial 11'), fg='black')
        self.new_pass_otp.place(x=40, y=190)

        self.new_pass_otp_ent = Entry(self.otp, width=20, show='*')
        self.new_pass_otp_ent.place(x=170, y =190)

        # button to submit the answers
        self.submit_answer_otp = Button(self.otp, text="Soumettre", font=('arial 11'), width=12, command=self.subAnswerOTP)
        self.submit_answer_otp.place(x=150, y=230)

    def subVeriEmail(self):
        self.forgotID = self.id_label_ent.get()

        sql_fetch_email_query = "Select * FROM credentials where id = ?"
        c.execute(sql_fetch_email_query, (self.forgotID, ))
        self.record = c.fetchall()
        for row in self.record:
            self.name = row[1]
            self.reg_email = row[11]
        
        # print(self.name)
        # print(self.reg_email)

        # send verification code
        if(is_connected(self)):
            updateStatusLabel(self)
            self.Sub_loginID["state"] = "Desactiver"
            self.emailStatus.configure(text='SVP patienté! envoie de email. . .', fg='black')
            self.verifyCode = sendVeriEmail(self, self.name, self.reg_email)
            print("Code: "+self.verifyCode)
        else:
            updateStatusLabel(self)

    def subAnswerOTP(self):
        self.newPass = self.new_pass_otp_ent.get()
        self.userID = self.id_label_ent.get()
        self.enteredVeriCode = self.codeLabel_ent.get()

        if self.verifyCode==self.enteredVeriCode:
            sql_pass_update_query = "UPDATE credentials SET pass=? where id=?"
            c.execute(sql_pass_update_query, (self.newPass, self.userID, ))
            conn.commit()
            print("Mot de passe changé")
        else:
            print("code de verification incorrect")
        
        self.Sub_loginID["state"] = "normal"
    
    def subAnswerSecretQues(self):
        tkinter.messagebox.showinfo(parent=self.top, title="Email envoyé", message="La vérification a été envoyée avec succès à votre adresse e-mail")  
        self.forgetID = self.id_label_ent.get()
        self.ans = self.answer_ent.get()
        # add sql query here:

        n = int(self.ques_num)
        sql_fetch_answer_query = "SELECT * FROM credentials where id = ?"
        c.execute(sql_fetch_answer_query, (self.forgetID,))
        self.record = c.fetchall()
        for row in self.record:
            self.secret_status = row[5+n*2]
            self.secret_answer = row[6+n*2]

        if self.secret_status and self.secret_answer == self.ans:
            sql_pass_update_query = "UPDATE credentials SET pass=? where id=?"
            c.execute(sql_pass_update_query, (self.new_pass_ent.get(), self.forgetID, ))
            conn.commit()
        else:
            print("Reponse secrete incorrect")

root = tk.Tk()
b = App(root)
root.geometry("540x380+360+180")
root.resizable(False, False)
root.title("Page de connexion de l'app de gestion hopital")
root.iconphoto(False, tk.PhotoImage(file="resources/icon.png"))
root.bind('<Return>', b.login)

def hide_root():
    # Hide root window
    root.withdraw()

def show_root():
    # Show root window
    root.deiconify()

def exitRoot(root):
    MsgBox = tk.messagebox.askquestion('Quitter Application','Voulez vous vraiment quitter?', icon='warning')
    if MsgBox == 'yes':
        root.destroy()

def updateStatusLabel(self):
    if(is_connected(self)):
        # set connected
        print("Status: Connecter")
        self.netStatus.configure(text='Internet: Connecter', fg='green')
        # self.Sub_loginID["state"] = "normal"
    else:
        # set not connected
        print("Status: Not connected")
        self.netStatus.configure(text='Internet: Non Connecter', fg='red')
        # self.Sub_loginID["state"] = "disabled"

# fuction to check internet connectivity
def is_connected(self):
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def sendVeriEmail(self, name, email):
    toaddrs = email

    # enter you email credentials
    username = '*****'
    password = '*****'
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    message = MIMEMultipart("alternative")
    message["Subject"] = "Forgot Password | MedFixture"
    message["From"] = username
    message["To"] = toaddrs

    html = """\
    <html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Forgot Password | MedFixture</title>

    <body>
        <p align="center" style="text-align: center;font-size: larger;">
            <img src="https://raw.githubusercontent.com/chauhannaman98/MedFixture/master/resources/icon.png" alt="Logo" width="80" height="80">
            <h3 align="center">MedFixture</h3>
        </p>
        <h1 align="center">Hi! """ + name + """ Seems like you forgot your password. </h1>
            <p style="text-align: center;font-size: larger;">Don't worry! Just enter the verification code
                given below.</p>
            <p style="text-align: center;font-size: larger;">Your verification code is :</p>
            <p class="veri-code" style="text-align: center;font-size: larger;font-family: 'Inconsolata', monospace;">"""+ x +"""</p>
    </body>
    <footer style="text-align: center;">
        <ul style="list-style-type: none;padding: 0;margin: 0;" , margin="0," padding="0">
            <li style="font-size: smaller;">An open-source project maintained by <a href="https://github.com/chauhannaman98">chauhannaman98</a></li>
            <li style="font-size: smaller;"><a href="https://chauhannaman98.github.io/MedFixture">Visit website</a></li>
        </ul>
    </footer>
    </html>
    """

    part1 = MIMEText(html, "html")
    message.attach(part1)
    print("Message built")

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        print("Logged in")
        server.sendmail(username, toaddrs, message.as_string())
        print("Verification code sent")
        self.emailStatus.configure(text='Code sent to your registered email', fg='green')
    except Exception as e:
        print(e)
    finally:
        server.quit()

    return x

if 'TRAVIS' in os.environ:
    root.update_idletasks()
else:
    root.mainloop()
