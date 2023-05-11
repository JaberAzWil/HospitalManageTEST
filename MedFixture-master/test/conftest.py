import pytest
from tkinter import Tk

# @pytest.fixture()
# def client():
#     with app.test_client() as client:
#         yield client


@pytest.fixture
def app(App):
    # Initialisation de l'application
    root = Tk()
    app = App(root)
    yield app
    root.destroy()
