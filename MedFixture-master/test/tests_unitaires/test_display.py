import sqlite3
import pytest
from tkinter import *   
import tkinter as tk
from display import App

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
