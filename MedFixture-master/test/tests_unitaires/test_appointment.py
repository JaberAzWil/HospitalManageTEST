import pytest
import tkinter as tk
from appointment import App
import tkinter.messagebox


@pytest.fixture
def app():
    # Créer une instance de la classe App
    root = tk.Tk()
    app = App(master=root)
    root.withdraw()  # cacher la fenêtre principale
    root.update()  # forcer la mise à jour de l'interface
    yield app


def test_add_appointment_ok(app):
    # Remplir les inputs de l'utilisateur
    app.name_ent.insert(0, 'John Doe')
    app.age_ent.insert(0, '25')
    app.var.set('Male')
    app.location_ent.insert(0, 'Paris')
    app.time_ent.insert(0, '2023-05-01 10:00')
    app.phone_ent.insert(0, '0601020304')

    # Appeler la fonction add_appointment de l'instance de la classe App
    app.add_appointment()
    assert 'ok' in tkinter.messagebox.showwarning(
        "Attention", "Veuillez remplir tous les détails")


def test_add_appointment_error(app):

    # Remplir les inputs de l'utilisateur
    app.name_ent.insert(0, 'John Doe')
    app.age_ent.insert(0, '25')
    app.var.set('')
    app.location_ent.insert(0, 'Paris')
    app.time_ent.insert(0, '2023-05-01 10:00')
    app.phone_ent.insert(0, '0601020304')

    # Appeler la fonction add_appointment de l'instance de la classe App
    with pytest.raises(ValueError):
        app.add_appointment()
