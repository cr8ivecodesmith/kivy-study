"""
Bulding a Full GUI

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_003_building_a_full_gui/

Documentation Reference:
- https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html
- https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html
- https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.size_hint

Main point(s):

- Adding Widgets to one another

"""  # noqa
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class CalculatorApp(App):

    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        # The size_hint_y property means this widget is about 1x as large
        # as its siblings relative to the parent's size.
        output_label = Label(size_hint_y=1)

        # The grid layout will be a child under the `root`, however the actual
        # numpad buttons will be its children.
        button_symbols = ('1', '2', '3', '+',
                          '4', '5', '6', '-',
                          '7', '8', '9', '.',
                          '0', '*', '/', '=',)
        button_grid = GridLayout(cols=4, size_hint_min_y=2)
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        clear_button = Button(
            text='clear',
            size_hint_y=0.25,
            height=100
        )

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)

        return root_widget


if __name__ == '__main__':
    CalculatorApp().run()
