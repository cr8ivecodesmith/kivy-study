"""
Draw Something

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_006_lets_draw_something/

Documentation Reference:


Main point(s):

- Handling touch or mouse input
- More canvas instructions

Notes:

- Drawing always come in pairs of vertex and instruction

"""  # noqa
from random import random

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle, Color, Line


def update_rectangle(instance, value):
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size


class DrawingWidget(Widget):
    # Since there is no built-in drawing widget, we'll create our own.
    def __init__(self):
        super().__init__()

        with self.canvas:
            # Draw a white background
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

            # Draw a red rectangle
            self.rect_color = Color(1, 0, 0, 1)  # Resets the color
            Rectangle(size=(300, 100), pos=(300, 200))

        # Bind handler to size and pos updates
        self.bind(pos=update_rectangle, size=update_rectangle)

    def on_touch_down(self, touch):
        # Calling super here propagates the touch event to this widget's
        # children as well.
        super().on_touch_down(touch)

        with self.canvas:
            Color(random(), random(), random())
            self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2)

    def on_touch_move(self, touch):
        # Kivy knows we're still referencing the line initialized in the
        # on_touch_down event hence we don't need another canvas context
        # here.
        # It will only reset on a new on_touch_down event.
        self.line.width += 0.15
        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]


class DrawingApp(App):
    def build(self):
        root_widget = DrawingWidget()
        return root_widget


if __name__ == '__main__':
    DrawingApp().run()
