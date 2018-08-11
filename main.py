import socket
from threading import Thread
from time import sleep


from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '650')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# get ip address
host=ip.getsockname()[0]
ip.close()

port = 0
s.bind((host, port))
s.setblocking(0)
name = socket.gethostname()
server = ("94.250.254.43", 9090)
shutdown = False


class ClientApp(App):

    def sendMsg(self, instance):

            message = self.writeTextInput.text
            if message != "":
                s.sendto(("[" + name + "] :: " + message).encode("utf-8"), server)

            self.readText.text += "[" + name + "] :: " + message + "\n"
            self.writeTextInput.text = ''

    def reciveMsg(self, sock):
        while (shutdown!=True):
            try:
                message, addr = sock.recvfrom(1024)
                self.readText.text += message.decode("utf-8") + "\n"
                sleep(0.2)
            except:
                pass

    def build(self):
        writeSendLayout=BoxLayout(spacing=20)
        verticalLayout=BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        sendButton=Button(text="Send", on_press=self.sendMsg)
        self.writeTextInput=TextInput(size_hint_x=5)
        self.readText=TextInput(size_hint_y=12)

        verticalLayout.add_widget(self.readText)
        verticalLayout.add_widget(writeSendLayout)

        writeSendLayout.add_widget(self.writeTextInput)
        writeSendLayout.add_widget(sendButton)

        s.sendto(("[" + name + "] => join chat ").encode("utf-8"), server)


        try:
            th = Thread(target=self.reciveMsg, name="Recive", args=(s,))
            th.start()
        except:
            pass


        return verticalLayout

if __name__=='__main__':
    ClientApp().run()
    s.sendto(("[" + name + "] <= left chat ").encode("utf-8"), server)
    s.close()
    shutdown = True