"""
Handling Data

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_009_finishing_the_drawing_app/

Documentation Reference:

- https://kivy.org/doc/stable/api-kivy.properties.html


Main point(s):

- Passing data between widgets
- Creating Kivy properties

Notes:

- Unlike a normal Python class property, a Kivy property can be bound to
  event handlers.
- There Kivy property equivalents to almost all Python data types (i.e.
  list, string, integer, etc)
- On a technical implementation stand-point, a Kivy property is a type of
  Python descriptor: https://docs.python.org/3/howto/descriptor.html


"""  # noqa
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.graphics import Color, Line
from kivy.properties import ListProperty, NumericProperty


class DrawingWidget(Widget):

    target_color_rgb = ListProperty([0, 0, 0])
    target_width_px = NumericProperty(0)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

        if not self.collide_point(*touch.pos):
            return

        with self.canvas:
            # Color should now change depending on the value of
            # target_color_rgb
            Color(*self.target_color_rgb)

            # Line width should also adapt to the value of target_width_px
            self.line = Line(
                points=[touch.pos[0], touch.pos[1]],
                width=self.target_width_px
            )

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return

        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]

    def on_target_color_rgb(self, instance, value):
        # Every bindable property has a on_{property} method!
        # We can still use:
        # self.bind(target_color_rgb=self.on_target_color_rgb)
        # to manually bind this event!
        print(f'target_color_rgb changed to {self.target_color_rgb}')


class Interface(BoxLayout):
    pass


class DrawingApp(App):

    def build(self):
        root_widget = Interface()
        return root_widget


if __name__ == '__main__':
    DrawingApp().run()
