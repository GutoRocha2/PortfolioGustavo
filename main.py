##Instale o Kivy, para rodar, com o comando pip install kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

class createAccountWindow(Screen):
    name_input = ObjectProperty(None)  # Alterado para "name_input"
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        # Alterar self.name para self.name_input
        if self.name_input.text != "" and self.email.text != "" and self.email.text.count('@') == 1 and self.email.text.count('.') > 0:
            if self.password.text != '':
                db.add_user(self.email.text, self.password.text, self.name_input.text)
                self.reset()
                sm.current = 'login'
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = 'login'

    def reset(self):
        self.email.text = ''
        self.password.text = ''
        self.name_input.text = ''  # Alterado também aqui


class loginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = 'main'
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = 'create'

    def reset(self):
        self.email.text = ''
        self.password.text = ''

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ''

    def logOut(self):
        sm.current = 'login'

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = 'Account Name: ' + name
        self.email.text = 'Email: ' + self.current
        self.created.text = 'Created On: ' + created

class WindowManager (ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
    content = Label(text= 'Invalid username or password.'),
    size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
    content=Label(text='Please fill in all inputs with valid information.'),
    size_hint=(None, None), size =(400, 400))
    pop.open()

kv = Builder.load_file('mk.kv')
sm = WindowManager()
class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = {}  # Dicionário para armazenar os usuários
        self.load()

    def load(self):
        """Carrega os usuários do arquivo no formato 'email,senha,nome,criado_em'."""
        with open(self.filename, 'r') as file:
            for line in file:
                email, password, name, created = line.strip().split(',')
                self.users[email] = (password, name, created)

    def validate(self, email, password):
        """Valida se o e-mail e a senha estão corretos."""
        if email in self.users:
            stored_password, _, _ = self.users[email]
            return stored_password == password
        return False

    def add_user(self, email, password, name):
        """Adiciona um novo usuário ao arquivo e ao dicionário."""
        if email not in self.users:
            from datetime import datetime
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.users[email] = (password, name, created)
            with open(self.filename, 'a') as file:
                file.write(f"{email},{password},{name},{created}\n")

    def get_user(self, email):
        """Retorna os detalhes do usuário: senha, nome e data de criação."""
        return self.users[email] if email in self.users else None


db = DataBase('users.txt')
screens = [loginWindow(name='login'), createAccountWindow(name='create'),MainWindow(name='main')]

for Screen in screens:
    sm.add_widget(Screen)
    sm.current = 'login'

class MyMainapp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyMainapp().run()
