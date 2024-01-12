from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
import random
from kivy.clock import mainthread

# Set window size
Window.size = (1000, 800)

# Constants
ENEMY_SPEED = 0.5
CORRECT_COLOR = (0, 1, 0, 1)  # Green color for correct words
WRONG_COLOR = (1, 0, 0, 1)    # Red color for wrong words

class TypingAttackGame(BoxLayout):
    def __init__(self, **kwargs):
        super(TypingAttackGame, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Initialize variables
        self.score = 0
        self.enemies = []

        # Create widgets
        self.score_label = Label(text=f"Score: {self.score}", font_size=24)
        self.game_area = Widget()

        # Add TextInput for typing
        self.text_input = TextInput(
            multiline=False, 
            size_hint=(1, 1), 
            font_size=24, 
            background_color=(1, 1, 1, 1)  # Set background color to white
        )
        self.text_input.bind(on_text_validate=self.on_text_validate)

        # Move the TextInput to the bottom
        self.text_input.y = 0
        self.add_widget(self.text_input)

        # Add widgets to layout
        self.add_widget(self.score_label)
        self.add_widget(self.game_area)

        # Load words from file
        self.word_list = self.load_words_from_file("words.txt")

        # Schedule enemy spawning
        Clock.schedule_interval(self.spawn_enemy, 3.5)

        # Keyboard bindings
        self.keys_pressed = set()
        self.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)

        # Game loop
        Clock.schedule_interval(self.update, 1.0 / 60.0)
    
    @mainthread
    def set_focus(self, dt):
        self.text_input.focus = True

    def on_text_validate(self, instance):
        typed_word = instance.text
        word_matched = False  # Flag to check if any enemy matches the typed word

        for enemy in self.enemies:
            if typed_word == enemy.text:
                self.score += 10
                self.score_label.text = f"Score: {self.score}"
                self.game_area.remove_widget(enemy)
                self.enemies.remove(enemy)
                instance.text = ""  # Clear the TextInput after successful typing
                self.text_input.background_color = CORRECT_COLOR  # Set background color to green
                Clock.schedule_once(self.reset_text_input_color, 0.5)  # Reset color after 0.5 seconds
                word_matched = True  # Set the flag to True
                Clock.schedule_once(self.set_focus, 0.1)  # Set focus after a short delay
                break  # Exit the loop since we found a match

        if not word_matched:
            instance.text = ""  # Clear the TextInput after Enter is pressed
            self.text_input.background_color = WRONG_COLOR  # Set background color to red
            Clock.schedule_once(self.reset_text_input_color, 0.5)  # Reset color after 0.5 seconds
            Clock.schedule_once(self.set_focus, 0.1)  # Set focus after a short delay

    def reset_text_input_color(self, dt):
        self.text_input.background_color = (1, 1, 1, 1)  # Reset background color to white

    def load_words_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                words = [line.strip() for line in file.readlines() if line.strip()]
                print(f"Loaded words: {words}")
                return words
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return []

    def spawn_enemy(self, dt):
        if self.word_list:
            enemy_word = random.choice(self.word_list)
            enemy = Label(text=enemy_word)
            enemy.x = random.randint(0, Window.width - enemy.width)
            enemy.y = Window.height
            self.enemies.append(enemy)
            self.game_area.add_widget(enemy)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if text.isalpha():
            self.keys_pressed.add(text)

    def on_key_up(self, keyboard, keycode):
        if keycode[1] in self.keys_pressed:
            self.keys_pressed.remove(keycode[1])

    def update(self, dt):
        # Move enemies
        for enemy in self.enemies:
            enemy.y -= ENEMY_SPEED

            # Check for collision with bottom of the window
            if enemy.y < 0:
                self.game_area.remove_widget(enemy)
                self.enemies.remove(enemy)

    def on_touch_move(self, touch):
        # Move player with touch input
        if touch.y < self.game_area.height / 2:
            self.game_area.x = touch.x - self.game_area.width / 2

class TypingAttackApp(App):
    def build(self):
        return TypingAttackGame()

if __name__ == '__main__':
    TypingAttackApp().run()
