"""
KV Lang Intro

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_007_introducing_kv_language/

Documentation Reference:


Main point(s):

- KV Language
- Building a GUI
- Integration with Python

Notes:

- This example solves the layout w/o the KV Lang.
- This can be very verbose and unwieldly as our application becomes more
  complex.
- The GUI/layout code is mixed with the logic code


"""  # noqa
from functools import partial
from random import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle, Color, Line


def update_rectangle(instance, value, target):
    target.pos = instance.pos
    target.size = instance.size


def update_color(instance, value, target, sr, sg, sb):
    target.rgb = (sr.value, sg.value, sb.value)


class DrawingWidget(Widget):

    def __init__(self):
        super().__init__()

        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle()

        self.bind(
            pos=partial(update_rectangle, target=self.rect),
            size=partial(update_rectangle, target=self.rect)
        )

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

        with self.canvas:
            Color(random(), random(), random())
            self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2)

    def on_touch_move(self, touch):
        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]


class DrawingApp(App):

    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        drawing_widget = DrawingWidget()

        red_slider = Slider(min=0, max=1, value=0.5,
                            size_hint_y=None, height=50)
        green_slider = Slider(min=0, max=1, value=0.5,
                              size_hint_y=None, height=50)
        blue_slider = Slider(min=0, max=1, value=0.5,
                             size_hint_y=None, height=50)

        color_row = BoxLayout(orientation='horizontal',
                              size_hint_y=None, height=50)
        color_label = Label(text='output color:')
        color_widget = Widget()

        # Draw a rectangle on the color_widget and update the size
        with color_widget.canvas:
            output_color = Color(
                red_slider.value, green_slider.value, blue_slider.value
            )
            output_rectangle = Rectangle()
        color_widget.bind(
            pos=partial(update_rectangle, target=output_rectangle),
            size=partial(update_rectangle, target=output_rectangle)
        )

        # Update the value on output_color whenever the color slider values
        # changes.
        red_slider.bind(value=partial(
            update_color, target=output_color,
            sr=red_slider, sg=green_slider, sb=blue_slider
        ))
        green_slider.bind(value=partial(
            update_color, target=output_color,
            sr=red_slider, sg=green_slider, sb=blue_slider
        ))
        blue_slider.bind(value=partial(
            update_color, target=output_color,
            sr=red_slider, sg=green_slider, sb=blue_slider
        ))

        # Put everything together
        root_widget.add_widget(drawing_widget)
        root_widget.add_widget(red_slider)
        root_widget.add_widget(green_slider)
        root_widget.add_widget(blue_slider)
        root_widget.add_widget(color_row)

        color_row.add_widget(color_label)
        color_row.add_widget(color_widget)

        return root_widget


if __name__ == '__main__':
    DrawingApp().run()
