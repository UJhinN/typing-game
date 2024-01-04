import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import random

class FallingInputBox(TextInput):
    def fall(self, speed=1):
        self.y -= speed  # Adjust the falling speed

class TypingGame(BoxLayout):
    falling_input_box = ObjectProperty(None)
    word_label = ObjectProperty(None)
    score_label = ObjectProperty(None)
    target_word = ""
    fruits = ["apple", "banana", "orange", "grape", "watermelon"]  # Add more fruits as needed
    score = 0  # Initialize score

    def __init__(self, **kwargs):
        super(TypingGame, self).__init__(**kwargs)

        # Set up the falling input box
        self.falling_input_box = FallingInputBox(
            pos=(Window.width / 2 - 100, Window.height - 100),
            size=(200, 30),
            multiline=False
        )
        self.add_widget(self.falling_input_box)

        # Set up the word label
        self.word_label = Label(text="", pos=(Window.width / 2, Window.height - 150), font_size=20)
        self.add_widget(self.word_label)

        # Set up the score label
        self.score_label = Label(text="Score: 0", pos=(10, Window.height - 30))
        self.add_widget(self.score_label)

        # Set up Clock for object movement and updates
        self.clock_event = Clock.schedule_interval(self.update, 1.0/120.0)  # Decreased update frequency

        # Choose the initial target word
        self.choose_target_word()

        # Bind the text property of falling_input_box to handle_collision
        self.falling_input_box.bind(text=self.handle_collision)
        self.time_left = 30  # ตั้งค่าเวลาเริ่มต้นที่ 30 วินาที
        self.time_label = Label(text=f"Time left: {self.time_left}", pos=(Window.width - 150, Window.height - 30))
        self.add_widget(self.time_label)


    def update(self, dt):
        # Move the falling input box with a slower falling speed
        self.falling_input_box.fall(speed=1)

        # Check for game over conditions
        if self.check_game_over():
            self.game_over()

    def handle_collision(self, instance, value):
        # Check each character individually for correctness
        typed_word = value
        correct = all(typed_char == target_char for typed_char, target_char in zip(typed_word, self.target_word))

        if correct and len(typed_word) == len(self.target_word):
            # Add 10 points for correct input
            self.score += 10
            self.score_label.text = f"Score: {self.score}"

            # Reset the falling input box position and choose a new target word
            self.falling_input_box.y = Window.height - 100
            self.falling_input_box.text = ""
            self.choose_target_word()

            # Check if the player wins
            if self.score >= 100:
                self.win()
        elif not correct:
            # Subtract half of the current score for incorrect input
            self.score = max(0, self.score - self.score // 2)
            self.score_label.text = f"Score: {self.score}"

            # Reset the falling input box position and choose a new target word for incorrect input
            self.falling_input_box.y = Window.height - 100
            self.falling_input_box.text = ""
            self.choose_target_word()

    def check_game_over(self):
        # Check if the falling input box reached the bottom
        return self.falling_input_box.y + self.falling_input_box.height < 0

    def game_over(self):
    # Stop the clock
        self.clock_event.cancel()

    # Remove existing widgets
        self.clear_widgets()

    # Create game over label
        game_over_label = Label(text="Game Over!", font_size=30)
        self.add_widget(game_over_label)

    # Display final score and time
        final_label = Label(text=f"Final Score: {self.score}\nTime taken: {30 - self.time_left:.2f} seconds", font_size=20)
        self.add_widget(final_label)

    # Create restart button
        restart_button = Button(text="Restart", on_press=self.restart_game)
        self.add_widget(restart_button)


    def win(self):
        # Stop the clock
        self.clock_event.cancel()

        # Remove existing widgets
        self.clear_widgets()

        # Create win label
        win_label = Label(text="WIN!", font_size=30)
        self.add_widget(win_label)

        # Create restart button
        restart_button = Button(text="Restart", on_press=self.restart_game)
        self.add_widget(restart_button)

    def restart_game(self, instance):
        # Remove game over or win widgets
        self.clear_widgets()

        # Restart the game
        self.__init__()

    def choose_target_word(self):
        # Randomly choose a new target word from the list of fruits
        self.target_word = random.choice(self.fruits)
        self.word_label.text = self.target_word
    def update(self, dt):
    # Move the falling input box with a slower falling speed
        self.falling_input_box.fall(speed=1)

    # Check for game over conditions
        if self.check_game_over():
            self.game_over()

    # Update the timer
        self.time_left -= dt
        self.time_label.text = f"Time left: {max(0, int(self.time_left))}"

    # Check if time is up
        if self.time_left <= 0:
            self.game_over()




class TypingGameApp(App):
    def build(self):
        game = TypingGame()
        return game

if __name__ == "__main__":
    TypingGameApp().run()
