"""
Hello World App

Explains the Kivy App Lifecycle
ohttps://kivy.org/doc/stable/guide/basic.html#kivy-app-life-cycle

"""
from kivy.app import App
from kivy.uix.label import Label


class HelloApp(App):  # Base class for the Kivy app

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    import kivy
    kivy.require('1.11.1')

    HelloApp().run()
