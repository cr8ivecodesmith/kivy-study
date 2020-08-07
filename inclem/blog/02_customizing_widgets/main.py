"""
Customization Widgets

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_002_improving_appearance/

Main point(s):

- Modifying Widget appearance
- Kivy properties

"""
from kivy.app import App
from kivy.uix.label import Label


class HelloApp(App):

    def build(self):
        # The [Label](https://kivy.org/docs/api-kivy.uix.label.html)
        # documentation shows us what properties we can change.

        # The default font size is 15sp. This is special Kivy syntax that
        # adjusts the font size depending on the device setting. On a desktop
        # that's on a non-hdpi display, this translates to 15px.
        # We'll make it simple for now and set it to 100.

        # Kivy also allows to place `markup` within the string to allow
        # further customization via the
        # [markup](https://kivy.org/docs/api-kivy.uix.label.html#markup-text)
        # syntax.

        root_widget = Label(
            font_size=100,
            italic=True,
            markup=True,
        )
        root_widget.text = (
            '[color=#ff0000]Hello[/color] '
            '[color=#00ff00]world![/color]'
        )

        # In a similar way, you can look into how to customize widgets through
        # the docs.

        return root_widget


if __name__ == '__main__':
    HelloApp().run()
