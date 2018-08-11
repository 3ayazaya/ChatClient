from kivy.app import App
from kivy.uix.label import Label


class ClientApp(App):
    def build(self):
        return Label(text='Hui')

if __name__=='__main__':
    ClientApp().run()