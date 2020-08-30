from kivy.app import App
from kivy.uix.widget import Widget

from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock


class Sprite(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = self.texture_size


class Background(Sprite):

    def update(self):
        self.x -= 2


class Game(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background = Background(source='images/background.png')
        self.size = self.background.size
        self.add_widget(self.background)

        self.add_widget(Sprite(source='images/bird.png'))

        Clock.schedule_interval(self.update, 1./60.)

    def update(self, *args):
        self.background.update()


class GameApp(App):

    def build(self):
        game = Game()
        Window.size = game.size
        return game


if __name__ == '__main__':
    GameApp().run()
