from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
import random
from kivy.clock import mainthread

# Set window size
Window.size = (2000, 1000)

# Constants
ENEMY_SPEED = 0.5
CORRECT_COLOR = (0, 1, 0, 1)  # Green color for correct words
WRONG_COLOR = (1, 0, 0, 1)    # Red color for wrong words

class TypingAttackGame(BoxLayout):
    def __init__(self, screen_manager=None, **kwargs):
        super(TypingAttackGame, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        # Initialize variables
        self.score = 0
        self.enemies = []

        # Create widgets
        self.score_label = Label(text=f"Score: {self.score}", font_size=36)
        self.game_area = Widget()

        # Add TextInput for typing
        self.text_input = TextInput(
            multiline=False, 
            size_hint=(10, 1),  # Set height to None
            height=100,  # Set a specific height as needed
            font_size=30,
            background_color=(1, 1, 1, 1)
        )
        self.text_input.bind(on_text_validate=self.on_text_validate)

        # Set the size of the TextInput box to be resizable
        self.text_input.size_hint_y = None

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

        # Add timer label and start the countdown
        self.timer_label = Label(text="Time: 300", font_size=24)
        self.add_widget(self.timer_label)
        self.remaining_time = 300
        Clock.schedule_interval(self.update_timer, 1.0)

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
            
            # Set the desired font size for the falling word
            enemy_font_size = random.randint(18, 36)

            enemy = Label(text=enemy_word, font_size=enemy_font_size)
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
                self.handle_missed_word(enemy)

    def handle_missed_word(self, enemy):
        # Remove the missed word from the game area and the list of enemies
        self.game_area.remove_widget(enemy)
        self.enemies.remove(enemy)

        # Deduct points for missing a word
        self.score -= 5
        self.score = max(0, self.score)  # Ensure the score does not go below zero

        # Update the score label
        self.score_label.text = f"Score: {self.score}"

        # Optionally, you can add additional feedback for the player when they miss a word
        # For example, change the color of the score label to indicate a penalty
        self.score_label.color = (1, 0, 0, 1)  # Red color
        Clock.schedule_once(self.reset_score_label_color, 0.5)  # Reset color after 0.5 seconds

    def reset_score_label_color(self, dt):
        self.score_label.color = (1, 1, 1, 1)  # Reset color to white

    def update_timer(self, dt):
        # Update the countdown timer
        self.remaining_time -= 1
        self.timer_label.text = f"Time: {self.remaining_time}"

        # Check if time is up
        if self.remaining_time <= 0:
            self.end_game()

    def end_game(self):
        # Game Over logic
        print("Game Over!")

        # Switch to the 'game_over' screen and pass the score
        game_over_screen = self.screen_manager.get_screen('game_over')
        game_over_screen.score = self.score
        game_over_screen.update_score_label()  # Update the score label
        self.screen_manager.current = 'game_over'
    def on_touch_move(self, touch):
        # Move player with touch input
        if touch.y < self.game_area.height / 2:
            self.game_area.x = touch.x - self.game_area.width / 2

class GameOverScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.score = 0  # Initialize score to 0

        # Create widgets for the Game Over screen
        game_over_label = Label(text="Game Over", font_size=48)
        score_label = Label(text=f"Your Score: {self.score}", font_size=36)

        restart_button = Button(
            text="Restart",
            font_size=24,
            size_hint=(1, 0.5),
        )
        restart_button.bind(on_press=self.restart_game)

        # Create layout for the Game Over screen
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(game_over_label)
        layout.add_widget(score_label)
        layout.add_widget(restart_button)

        self.add_widget(layout)

    def restart_game(self, instance):
        # Restart the game by switching to the game screen
        self.screen_manager.current = 'game'


    def end_game(self):
    # Game Over logic
        print("Game Over!")

    # Switch to the 'game_over' screen and pass the score
        game_over_screen = self.screen_manager.get_screen('game_over')
        game_over_screen.score = self.score
        self.screen_manager.current = 'game_over'
    # You can perform other actions here as needed
    def update_score_label(self):
        # Update the score label when called
        score_label = self.children[0].children[1]  # Assuming the score_label is the second child
        score_label.text = f"Your Score: {self.score}"

class StartScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

        # Create widgets for the Start screen
        start_label = Label(text="TYPING-ATTACK", font_size=48)
        start_button = Button(
            text="Start Game",
            font_size=36,
            color=(0, 1, 0, 1),
            size_hint=(1, 0.5),  # Adjust the size_hint as needed
        )
        start_button.bind(on_press=self.start_game)

        # Create layout for the Start screen
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(start_label)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        # Start the game by switching to the game screen
        self.screen_manager.current = 'game'
class TypingAttackApp(App):
    def build(self):
        # Create ScreenManager
        screen_manager = ScreenManager()

        # Create and add Start Screen to ScreenManager
        start_screen = StartScreen(screen_manager, name='start')
        screen_manager.add_widget(start_screen)

        # Create and add Game Screen to ScreenManager
        game_screen = Screen(name='game')
        game_screen.add_widget(TypingAttackGame(screen_manager))
        screen_manager.add_widget(game_screen)

        # Create and add Game Over Screen to ScreenManager
        game_over_screen = GameOverScreen(screen_manager, name='game_over')
        screen_manager.add_widget(game_over_screen)

        # Set the current screen to 'start'
        screen_manager.current = 'start'

        # Set Window to fullscreen
        Window.fullscreen = 'auto'

        return screen_manager

if __name__ == '__main__':
    TypingAttackApp().run()