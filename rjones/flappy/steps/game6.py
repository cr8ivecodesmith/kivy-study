"""
Collision detection

"""
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


class Bird(Sprite):

    def __init__(self, pos, **kwargs):
        super().__init__(
            source='atlas://images/bird_anim/wing-up', pos=pos, **kwargs
        )
        self.velocity_y = 0
        self.gravity = -.3

    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y

        if self.velocity_y < -5:
            self.source = 'atlas://images/bird_anim/wing-up'
        elif self.velocity_y < 0:
            self.source = 'atlas://images/bird_anim/wing-mid'

    def on_touch_down(self, *args):
        self.velocity_y = 5.5
        self.source = 'atlas://images/bird_anim/wing-down'


class Background(Widget):

    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)

        self.image = Sprite(source=source)
        self.add_widget(self.image)

        self.size = self.image.size

        self.image_dup = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dup)

    def update(self):
        self.image.x -= 2
        self.image_dup.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dup.x = self.width


class Ground(Sprite):

    def update(self):
        self.x -= 2
        if self.x < -24:  # Ground repeats at 24px
            self.x += 24


class Game(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add the background
        self.background = Background(source='images/background.png')
        self.size = self.background.size
        self.add_widget(self.background)

        # Add the bird
        self.bird = Bird(pos=(20, self.height / 2))
        self.add_widget(self.bird)

        # Add the ground
        self.ground = Ground(source='images/ground.png')
        self.add_widget(self.ground)

        # Start the game loop
        Clock.schedule_interval(self.update, 1./60.)

    def update(self, *args):
        self.background.update()
        self.bird.update()
        self.ground.update()

        if self.bird.collide_widget(self.ground):
            print('Game over!')


class GameApp(App):

    def build(self):
        game = Game()
        Window.size = game.size
        return game


if __name__ == '__main__':
    GameApp().run()
