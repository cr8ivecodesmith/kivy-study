"""
Hello World

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_001_say_hello/

Main point(s):

- Starting an app
- Getting Kivy running

"""
from kivy.app import App
from kivy.uix.label import Label


class HelloApp(App):

    def build(self):
        # Kivy applications are composed of `widgets` in a tree-like structure
        # starting from the `root` widget.

        # Widgets perform relatively small tasks like displaying a text.
        # Examples:
        # Labels, Buttons, or Layouts (which contains other
        # widgets and controls their positions).

        # The build method initializes the `root` widget.
        root_widget = Label(text='Hello world!')
        return root_widget


if __name__ == '__main__':
    # NOTE: Unlike a typical game engine/game programming,
    # Kivy controls the "game/application loop" as in any
    # GUI/Event-based frameworks.

    # Run the application
    HelloApp().run()
