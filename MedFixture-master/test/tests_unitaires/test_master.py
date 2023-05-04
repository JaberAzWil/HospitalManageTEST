import sqlite3
import pytest
from tkinter import *   
import tkinter as tk
from master import App

conn = sqlite3.connect('database.db')
c = conn.cursor() 

@pytest.fixture
def app():
    # Créer une instance de la classe App
    root = tk.Tk()
    app = App(master=root)
    yield app
    root.mainloop()

def test_login_success(app):
    # Set up
    app.login_id_ent.insert(0, 'johndoe')
    app.password_ent.insert(0, 'password123')
    c.execute("INSERT INTO credentials (id, name, password, designation) VALUES (?, ?, ?, ?)",
              ('johndoe', 'John Doe', 'password123', 'admin'))
    conn.commit()
    
    # Call function
    app.login(None)
    app.login_id_ent.insert(0, 'johndoe')
    
    c.execute("SELECT * FROM credentials WHERE name=?", ('johndoe',))
    result = c.fetchone()
    assert result is not None
    
# def test_login_failure(app):
#     # Set up
#     app.login_id_ent.insert(0, 'johndoe')
#     app.password_ent.insert(0, 'wrongpassword')
    
#     with pytest.raises(ValueError):
#         app.login(None)