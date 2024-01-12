
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Set window size
Window.size = (800, 600)

# Constants
ENEMY_SPEED = 0.5

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

        # Add widgets to layout
        self.add_widget(self.score_label)
        self.add_widget(self.game_area)

        # Load words from file
        self.word_list = self.load_words_from_file("words.txt")

        # Schedule enemy spawning
        Clock.schedule_interval(self.spawn_enemy, 1)

        # Keyboard bindings
        self.keys_pressed = set()
        self.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)

        # Game loop
        Clock.schedule_interval(self.update, 1.0 / 60.0)

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
            self.input_text += text  # Append to input text

            # Check for matching enemies
            self.check_for_matches()

            # Check if any enemy has a matching text
            for enemy in self.enemies:
                if enemy.y < self.game_area.height / 2 and enemy.text == text:
                    self.score += 10
                    self.score_label.text = f"Score: {self.score}"
                    self.game_area.remove_widget(enemy)
                    self.enemies.remove(enemy)
                    break  # Break after handling one enemy (optional)
    def check_for_matches(self):
        for enemy in self.enemies:
            if enemy.y < self.game_area.height / 2 and enemy.text == self.input_text:
                self.score += 10
                self.score_label.text = f"Score: {self.score}"
                self.game_area.remove_widget(enemy)
                self.enemies.remove(enemy)
                self.input_text = ''  # Clear input text
                break               
    def on_key_up(self, keyboard, keycode):
        if keycode[1] in self.keys_pressed:
            self.keys_pressed.remove(keycode[1])

    def update(self, dt):
        # Move enemies
        for enemy in self.enemies:
            enemy.y -= ENEMY_SPEED

            # Check for collision with the bottom of the window
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
