"""
KV Lang Intro

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_007_introducing_kv_language/

Documentation Reference:

- https://kivy.org/doc/stable/guide/lang.html?
- https://kivy.org/docs/guide/lang.html#how-to-load-kv
- https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.collide_point

Main point(s):

- KV Language
- Building a GUI
- Integration with Python

Notes:

- This solution applies the KV Lang
- Kivy automatically loads a `.kv` file with the same name as the app class.
  In this case, a `drawing.kv` file will be loaded automatically when
  available.
- You can load another file: See [#how-to-load-kv].
- Binding logic will be applied on the next lesson


"""  # noqa
from functools import partial
from random import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle, Color, Line


def update_rectangle(instance, value, target):
    target.pos = instance.pos
    target.size = instance.size


def update_color(instance, value, target, sr, sg, sb):
    target.rgb = (sr.value, sg.value, sb.value)


class DrawingWidget(Widget):

    def __init__(self, *args, **kwargs):
        # There are other values being passed along whenever this is
        # initialized elsewhere (i.e. kv files) so the best practice is
        # to ensure those variables are passed along.
        super().__init__(*args, **kwargs)

        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle()

        self.bind(
            pos=partial(update_rectangle, target=self.rect),
            size=partial(update_rectangle, target=self.rect)
        )

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

        # Checks if the touch x,y is within our widget. If it's not,
        # don't do anything
        if not self.collide_point(*touch.pos):
            return

        with self.canvas:
            Color(random(), random(), random())
            self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return

        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]


class Interface(BoxLayout):
    pass


class DrawingApp(App):

    def build(self):
        root_widget = Interface()
        return root_widget


if __name__ == '__main__':
    DrawingApp().run()
