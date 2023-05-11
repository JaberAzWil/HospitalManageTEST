import sqlite3
import pytest
from tkinter import Tk
from delete import App

conn = sqlite3.connect('database.db')
c = conn.cursor()


@pytest.fixture
def app():
    # Créer une instance de la classe App
    root = Tk()
    app = App(master=root)
    yield app
    root.mainloop()


def test_search_db(app):

    # set input to search
    app.namenet.delete(0, "end")
    app.namenet.insert(0, "John Doe")

    # execute search
    app.search_db()

    # assert that the labels display the correct information
    assert app.ent1.cget("text") == "John Doe"
    assert app.ent2.cget("text") == 25
    assert app.ent3.cget("text") == "Male"
    assert app.ent4.cget("text") == "Paris"
    assert app.ent5.cget("text") == "2023-05-01 10:00"
    assert app.ent6.cget("text") == 601020304


def test_delete_db(app):
    app.namenet.insert(0, "Robot22")
    # # Ajouter un enregistrement dans la base de données
    c.execute("INSERT INTO appointments (name) VALUES (?)", ('Robot22',))
    conn.commit()

    # Appeler la fonction delete_db()
    app.delete_db()

    # Vérifier que l'enregistrement a bien été supprimé
    c.execute("SELECT * FROM appointments WHERE name=?", ('Robot22',))
    result = c.fetchone()
    assert result is None
