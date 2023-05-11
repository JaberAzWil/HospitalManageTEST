# for Python3
import tkinter as tk
from tkinter import Label, Entry, Button
import sqlite3
import tkinter.messagebox

conn = sqlite3.connect('database.db')
c = conn.cursor()


class App:
    def __init__(self, master):
        self.master = master
        # heading label
        self.heading = Label(
            master,
            text="Changer rendez-vous",
            fg='black',
            font=('arial 18'))
        self.heading.place(x=180, y=40)

        # search criteria -->name
        self.name = Label(
            master,
            text="Entrer nom du patient",
            font=('arial 12'))
        self.name.place(x=70, y=100)

        # entry for  the name
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=300, y=100)

        # search button
        self.search = Button(
            master,
            text="Rechercher",
            width=12,
            height=1,
            bg='steelblue',
            command=self.search_db)
        self.search.place(x=230, y=150)

    # function to search

    def search_db(self):
        self.input = self.namenet.get()

        # execute sql
        sql = "SELECT * FROM appointments WHERE name LIKE ?"
        self.res = c.execute(sql, (self.input,))
        for self.row in self.res:
            self.name1 = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.time = self.row[6]
            self.phone = self.row[5]

        # creating the update form
        self.uname = Label(
            self.master,
            text="Nom du patient",
            font=('arial 12'))
        self.uname.place(x=70, y=220)

        self.uage = Label(self.master, text="Age", font=('arial 12'))
        self.uage.place(x=70, y=260)

        self.ugender = Label(self.master, text="Genre", font=('arial 12'))
        self.ugender.place(x=70, y=300)

        self.ulocation = Label(self.master, text="Localité", font=('arial 12'))
        self.ulocation.place(x=70, y=340)

        self.utime = Label(
            self.master,
            text="Date de rendez-vous",
            font=('arial 12'))
        self.utime.place(x=70, y=380)

        self.uphone = Label(
            self.master,
            text="Numero de telephone",
            font=('arial 12'))
        self.uphone.place(x=70, y=420)

        # entries for each labels==============================================
        # ===================filling the search result in the entry box to update
        self.ent1 = Label(self.master, text=self.name1, font=('arial 12'))
        self.ent1.place(x=300, y=220)

        self.ent2 = Label(self.master, text=self.age, font=('arial 12'))
        self.ent2.place(x=300, y=260)

        self.ent3 = Label(self.master, text=self.gender, font=('arial 12'))
        self.ent3.place(x=300, y=300)

        self.ent4 = Label(self.master, text=self.location, font=('arial 12'))
        self.ent4.place(x=300, y=340)

        self.ent5 = Label(self.master, text=self.time, font=('arial 12'))
        self.ent5.place(x=300, y=380)

        self.ent6 = Label(self.master, text=self.phone, font=('arial 12'))
        self.ent6.place(x=300, y=420)

        # button to execute update
        self.delete = Button(
            self.master,
            text="SUPPRIMER",
            width=20,
            height=2,
            bg='red',
            command=self.delete_db)
        self.delete.place(x=200, y=480)

    def delete_db(self):
        try:
            if tkinter.messagebox.askyesno(
                "Vous etes surs?",
                    "Supprimer l'enregistrement ?"):
                # delete the appointment
                sql2 = "DELETE FROM appointments WHERE name=?"
                c.execute(sql2, (self.namenet.get(),))
                conn.commit()
                tkinter.messagebox.showinfo("Reussie", "Suppression reussie")
        except BaseException:
            tkinter.messagebox.showerror("Erreur", "La suppression a échoué")


# creating the object
root = tk.Tk()
b = App(root)
root.geometry("640x620+100+50")
root.resizable(False, False)
root.title("Changer rendez-vous")
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

# end the loop
root.mainloop()
