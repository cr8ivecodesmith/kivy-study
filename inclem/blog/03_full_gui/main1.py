"""
Bulding a Full GUI

Reference:
http://inclem.net/2019/12/18/kivy/kivy_tutorial_003_building_a_full_gui/

Main point(s):

- Adding Widgets to one another

"""
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class CalculatorApp(App):

    def build(self):
        # Initialize a layout widget as our `root`
        layout = BoxLayout(orientation='vertical')

        # Create button widgets
        b1 = Button(text='button 1')
        b2 = Button(text='button 2')

        # Add the button widgets as children of our `root`
        layout.add_widget(b1)
        layout.add_widget(b2)

        # Return the `root`
        return layout


if __name__ == '__main__':
    CalculatorApp().run()
