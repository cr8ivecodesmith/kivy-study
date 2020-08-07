"""
Kivy Configuration

Reference:
https://kivy.org/doc/stable/guide/config.html

"""
from kivy.app import App
from kivy.uix.label import Label

from kivy.config import Config


class HelloApp(App):  # Base class for the Kivy app

    def build(self):

        # Should print "warning"
        print('\n-> KIVY LOG_LEVEL - {}\n'.format(
            Config.get('kivy', 'log_level')))

        return Label(text='Hello world')


if __name__ == '__main__':
    import os
    from pathlib import Path

    import kivy

    kivy.require('1.11.1')

    # Set the project path to the current application directory
    PROJECT_PATH = Path(__file__).parent.absolute()
    os.environ['KIVY_HOME'] = PROJECT_PATH.as_posix()

    # Look for the config file on this directory
    CONFIG_FILE = PROJECT_PATH.joinpath('.config').as_posix()

    # Load and set additional configurations and save
    Config.read(CONFIG_FILE)

    # set additional configuration here...
    Config.set('kivy', 'log_level', 'warning')

    Config.write()

    # Run the app
    HelloApp().run()
