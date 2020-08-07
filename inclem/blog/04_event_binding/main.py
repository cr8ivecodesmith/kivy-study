"""
Event Binding

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_004_event_bindings/

Documentation Reference:

Main point(s):

- Events and Kivy properties

Notes:

- Event binding is a generic (and very important) Kivy concept
- Whenever you want one thing to trigger another, you look for an event to
  bind to.
- All (or Almost?) Kivy widget properties can be bound to.
- Only Kivy-properties can be bound to event handlers

"""  # noqa
from functools import partial

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


def print_button_text(instance, target):
    target.text += instance.text


def resize_label_text(label, new_height):
    label.font_size = 0.5 * label.height
    print('resize_label_text1')


def resize_label_text2(label, new_height):
    print('resize_label_text2')


def evaluate_result(instance, target):
    try:
        target.text = str(eval(target.text))
    except SyntaxError:
        target.text = 'Err'


def clear_label(instance, target):
    target.text = ''


class CalculatorApp(App):

    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        output_label = Label(size_hint_y=1)

        # We'll bind a handler to the `height` property of the output_label
        # so the font_size scales whenever the height changes
        #
        # You can also bind multiple handlers. They will be called in order
        # of binding.
        output_label.bind(height=resize_label_text)
        output_label.bind(height=resize_label_text2)

        button_symbols = ('1', '2', '3', '+',
                          '4', '5', '6', '-',
                          '7', '8', '9', '.',
                          '0', '*', '/', '=',)
        button_grid = GridLayout(cols=4, size_hint_min_y=2)
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        # Bind the print_button_text function on the `on_press` event
        # except for the '=' symbol which we'll bind a different handler.
        #
        # The `w.children` is a list of child widgets in reverse order. This
        # means the first element is always the last widget added.
        for button in button_grid.children[1:]:
            button.bind(on_press=partial(
                print_button_text, target=output_label
            ))

        # Bind the evaluate_result handler to the '=' symbol.
        button_grid.children[0].bind(on_press=partial(
            evaluate_result, target=output_label
        ))

        clear_button = Button(
            text='clear',
            size_hint_y=0.25,
            height=100
        )
        # Bind the clear_label handler to the 'clear' button.
        clear_button.bind(on_press=partial(
            clear_label, target=output_label
        ))

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)

        return root_widget


if __name__ == '__main__':
    CalculatorApp().run()
