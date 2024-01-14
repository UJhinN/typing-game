from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
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
        self.sound = SoundLoader.load("C:\\Users\\AVS_BP\\Downloads\\sound6.mp3") 
        self.sound.volume = 0.03
        self.sound.play()

        if not self.sound:
            print("Error loading sound files.")
        
        

        # Add TextInput for typing
        self.text_input = TextInput(
            multiline=False, 
            size_hint=(10, 1),  # Set height to None
            height=100,  # Set a specific height as needed
            font_size=30,
            background_color=(1, 1, 1, 1)
        )
        restart_button = Button(text="Restart", font_size=24, size_hint=(1, 0.0943))
        restart_button.bind(on_press=self.restart_game)
        self.add_widget(restart_button)

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
        Clock.schedule_interval(self.spawn_enemy, 2)

        # Keyboard bindings
        self.keys_pressed = set()
        self.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)

        # Game loop
        Clock.schedule_interval(self.update, 1.0 / 80.0)

        # Add timer label and start the countdown
        self.timer_label = Label(text="Time: 180", font_size=24)
        self.add_widget(self.timer_label)
        self.remaining_time = 180
        Clock.schedule_interval(self.update_timer, 1.0)

    def on_text_validate(self, instance):
        typed_word = instance.text
        word_matched = False

        for enemy in self.enemies:
            if typed_word == enemy.text:
                # Play correct sound
                if self.correct_sound:
                    self.correct_sound.play()
                word_matched = True
                break    

        if not word_matched:
            # Play incorrect sound
            if self.incorrect_sound:
                self.incorrect_sound.play()

        # Additional sound for testing
        if self.additional_sound:
            self.additional_sound.play()

        # Rest of your existing code...
    def switch_to_game_over_screen(self):
        game_over_screen = self.screen_manager.get_screen('game_over')
        game_over_screen.score = self.score
        self.screen_manager.current = 'game_over'

    def end_game(self):
        # Game Over logic
        print("Game Over!")

        # Stop the clock interval for updating the timer
        Clock.unschedule(self.update_timer)

        # Switch to the 'game_over' screen
        self.switch_to_game_over_screen()

    def restart_game(self, instance):
        # Reset the game state
        self.score = 0
        self.score_label.text = f"Score: {self.score}"
        
        self.remaining_time = 180
        self.timer_label.text = f"Time: {self.remaining_time}"

        # Clear existing enemies and spawn new ones
        self.enemies = []
        self.game_area.clear_widgets()
        self.spawn_enemy(0)  # Spawn initial enemies
        self.reset_enemy_speed()  # Reset enemy speed

        # Reset the text input
        self.text_input.text = ""
        if self.sound:
            self.sound.play()
        # Set focus to the text input after a short delay
        Clock.schedule_once(self.set_focus, 0.1)

    def reset_enemy_speed(self):
        global ENEMY_SPEED
        ENEMY_SPEED = 0.5

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
            enemy_font_size = random.randint(45, 50)

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

            # Check for collision with the bottom of the window
            if enemy.y < 0:
                self.handle_missed_word(enemy)

        # Check if the total score is a multiple of 40 to increase speed
        if self.score % 40 == 0 and self.score > 0:
            self.increase_enemy_speed()

    def increase_enemy_speed(self):
        global ENEMY_SPEED
        # Adjust the ENEMY_SPEED value to increase the falling speed
        ENEMY_SPEED += 0.001

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
        self.timer_label.text = f"Time: {max(0, self.remaining_time)}"  # Ensure the timer label doesn't show negative values

        # Check if time is up
        if self.remaining_time <= 0:
            self.end_game()

    def end_game(self):
        # Game Over logic

        # Check if the current score is higher than the existing high score
        if self.score > self.get_high_score():
            self.set_high_score(self.score)  # Update the high score
            self.show_high_score_screen()  # Switch to the High Score screen
        else:
            self.switch_to_game_over_screen()  # Switch to the 'game_over' screen

    def get_high_score(self):
        # Function to retrieve the high score from storage (e.g., a file)
        try:
            with open("high_score.txt", "r") as file:
                high_score = int(file.read())
                return high_score
        except FileNotFoundError:
            return 0

    def set_high_score(self, score):
        # Function to set the high score in storage (e.g., a file)
        with open("high_score.txt", "w") as file:
            file.write(str(score))

    def show_high_score_screen(self):
        # Switch to the High Score screen and pass the high score
        high_score_screen = self.screen_manager.get_screen('high_score')
        high_score_screen.high_score = self.get_high_score()
        self.screen_manager.current = 'high_score'

        # Stop the clock interval for updating the timer
        Clock.unschedule(self.update_timer)

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
            text="New Game",
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
        # Reset the game by switching to the game screen
        self.screen_manager.current = 'game'

        # Reset the remaining time to its initial value
        game_screen = self.screen_manager.get_screen('game')
        game_screen.children[0].remaining_time = 180

        # Reset the score to 0
        game_screen.children[0].score = 0
        game_screen.children[0].score_label.text = f"Score: {game_screen.children[0].score}"

        # Clear existing enemies and spawn new ones
        game_screen.children[0].enemies = []
        game_screen.children[0].game_area.clear_widgets()
        game_screen.children[0].spawn_enemy(0)  # Spawn initial enemies

        # Reset the text input
        game_screen.children[0].text_input.text = ""
        self.sound = SoundLoader.load("C:\\Users\\AVS_BP\\Downloads\\sound6.mp3") 
        self.sound.volume = 0.03
        if self.sound:
            self.sound.play()
        # Set focus to the text input after a short delay
        Clock.schedule_once(game_screen.children[0].set_focus, 0.1)

        # Update the timer label in the game screen
        game_screen.children[0].timer_label.text = f"Time: {game_screen.children[0].remaining_time}"
    
        game_screen.children[0].reset_enemy_speed()
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
    # def switch_to_start_screen(self, instance):
    #     # Switch back to the Start screen
    #     self.screen_manager.current = 'start'
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
            size_hint=(1, 0.4),
        )
        start_button.bind(on_press=self.start_game)

        # Add a button to view high score
        high_score_button = Button(
            text="High Score",
            font_size=24,
            size_hint=(1, 0.2),
        )
        high_score_button.bind(on_press=self.view_high_score)

        volume_up_button = Button(
            text="Volume Up",
            font_size=24,
            size_hint=(1, 0.2),
        )
        volume_up_button.bind(on_press=self.volume_up)

        volume_down_button = Button(
            text="Volume Down",
            font_size=24,
            size_hint=(1, 0.2),
        )
        volume_down_button.bind(on_press=self.volume_down)

        # Create layout for the Start screen
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(start_label)
        layout.add_widget(start_button)
        layout.add_widget(high_score_button)
        layout.add_widget(volume_up_button)
        layout.add_widget(volume_down_button)

        self.add_widget(layout)

    def view_high_score(self, instance):
        # Switch to the High Score screen
        self.screen_manager.current = 'high_score'

    def volume_up(self, instance):
        # Increase the volume
        game_screen = self.screen_manager.get_screen('game').children[0]
        if hasattr(game_screen, 'sound') and game_screen.sound:
            game_screen.sound.volume = min(1, game_screen.sound.volume + 0.1)
    def switch_to_start_screen(self, instance):
        self.screen_manager.current = 'start'
    def volume_down(self, instance):
        # Decrease the volume
        game_screen = self.screen_manager.get_screen('game').children[0]
        if hasattr(game_screen, 'sound') and game_screen.sound:
            game_screen.sound.volume = max(0, game_screen.sound.volume - 0.1)

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
        high_score_screen = HighScoreScreen(screen_manager, high_score=0, name='high_score')
        screen_manager.add_widget(high_score_screen)

        # Set the current screen to 'start'
        screen_manager.current = 'start'

        # Set Window to fullscreen
        Window.fullscreen = 'auto'
        
        return screen_manager


class HighScoreScreen(Screen):
    def __init__(self, screen_manager, high_score, **kwargs):
        super(HighScoreScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.high_score = high_score

        # Create widgets for the High Score screen
        high_score_label = Label(text=f"High Score: {self.high_score}", font_size=36)

        # Add a button to go back
        back_button = Button(
            text="Back",
            font_size=24,
            size_hint=(1, 0.5),
        )
        back_button.bind(on_press=self.go_back)

        # Create layout for the High Score screen
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(high_score_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        # Switch back to the Start screen
        self.screen_manager.current = 'start'
if __name__ == '__main__':
    TypingAttackApp().run()