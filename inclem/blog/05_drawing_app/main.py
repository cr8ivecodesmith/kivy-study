"""
Drawing App

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_005_a_drawing_app/

Documentation Reference:

- https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas
- https://kivy.org/docs/api-kivy.graphics.vertex_instructions.html
- https://kivy.org/docs/api-kivy.graphics.context_instructions.html

Main point(s):

- Canvas instructions

Notes:

- Kivy's coordinate system follows the OpenGL format which means (0, 0) is
  x, y from the bottom left
- All widgets have a canvas
- The canvas is where you'll give instructions as to what to draw.
- All graphical representation of widgets are abstractions for the canvas.
- vertex instructions are for shapes
- context instructions are for color

"""  # noqa
from functools import partial

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle, Color


def update_rectangle(instance, value, target):
    target.pos = instance.pos
    target.size = instance.size


class DrawingWidget(Widget):
    # Since there is no built-in drawing widget, we'll create our own.
    def __init__(self):
        super().__init__()
        with self.canvas:
            Color(1, 1, 1, 1)  # rgba
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # The relative size and pos of the widget won't be set until
        # runtime. The problem is the object initialization happens before
        # runtime. So in order to get the final size and pos, we need a
        # handler that will make the adjustments.
        #
        # If you don't, you'll just see a 100x100 white square at the
        # bottom-left
        self.bind(
            pos=partial(update_rectangle, target=self.rect),
            size=partial(update_rectangle, target=self.rect)
        )


class DrawingApp(App):
    def build(self):
        root_widget = DrawingWidget()
        return root_widget


if __name__ == '__main__':
    DrawingApp().run()
