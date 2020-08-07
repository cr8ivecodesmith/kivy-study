"""
Kivy Environment Variables

You can configure several environment variables when building or running
your Kivy app. You can also set them up within your app.


Environment variables reference:
https://kivy.org/doc/stable/guide/environment.html

"""
from kivy.app import App
from kivy.uix.label import Label


class HelloApp(App):  # Base class for the Kivy app

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    import os
    import kivy

    kivy.require('1.11.1')

    # Configure Kivy Environment variables
    os.environ['KIVY_NO_CONSOLELOG'] = '1'  # No console output

    # Map settings to the Config object
    # i.e. Config.set('kivy', 'log_level', 'warning')
    os.environ['KCFG_KIVY_LOG_LEVEL'] = 'error'

    HelloApp().run()
