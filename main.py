import kivy
import nltk
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from nltk.corpus import words

nltk.download('words')

#----------------- GAME VARIABLE -----------------#
letters = [chr(i) for i in range(97, 123)]
length_select = [True, False, False, False, False, False, False]
word_objects = []
len_indexes = []
list_ofword = []
active_string = ""
submit = ""
txt_color, txt_color_2 = "", ""
total_type = 0
lives = 4
level = 0
scroll_offset = 0
item_height = 40
visible_items = 15
length = 1
paused = True
new_lvl = True
music_paused = False
cheat = False
active = False
active_2 = False

class FallingInputBox(TextInput):
    def fall(self, speed=0.005):
        self.y -= speed

class TypingGame(BoxLayout):
    falling_input_box = ObjectProperty(None)
    word_label = ObjectProperty(None)
    score_label = ObjectProperty(None)
    target_word = ""
    wordlist = words.words()
    score = 0  # เพิ่มแอตทริบิวต์ score

    wordlist.sort(key=len)
    for i in range(len(wordlist)):
        if len(wordlist[i]) > length:
            length += 1
            len_indexes.append(i)
    len_indexes.append(len(wordlist))

    def __init__(self, **kwargs):
        super(TypingGame, self).__init__(**kwargs)

        self.falling_input_box = FallingInputBox(
            pos=(Window.width / 2 - 100, Window.height - 100),
            size=(200, 30),
            multiline=False
        )
        self.add_widget(self.falling_input_box)

        self.word_label = Label(text="", pos=(Window.width / 2, Window.height - 150), font_size=20)
        self.add_widget(self.word_label)

        self.score_label = Label(text="Score: 0", pos=(10, Window.height - 30))
        self.add_widget(self.score_label)

        self.clock_event = Clock.schedule_interval(self.update, 1.0/120.0)

        self.choose_target_word()

        self.falling_input_box.bind(text=self.handle_collision)
        self.time_left = 300
        self.time_label = Label(text=f"Time left: {self.time_left}", pos=(Window.width - 150, Window.height - 30))
        self.add_widget(self.time_label)

    def update(self, dt):
        self.falling_input_box.fall(speed=0.25)

        if self.check_game_over():
            self.game_over()

        self.time_left -= dt
        self.time_label.text = f"Time left: {max(0, int(self.time_left))}"

        if self.time_left <= 0:
            self.game_over()

    def handle_collision(self, instance, value):
        typed_word = value
        correct = all(typed_char == target_char for typed_char, target_char in zip(typed_word, self.target_word))

        if correct and len(typed_word) == len(self.target_word):
            self.score += 10
            self.score_label.text = f"Score: {self.score}"

            self.falling_input_box.y = Window.height - 100
            self.falling_input_box.text = ""
            self.choose_target_word()

            if self.score >= 9999:
                self.win()
        elif not correct:
            self.score = max(0, self.score - self.score // 2)
            self.score_label.text = f"Score: {self.score}"

            self.falling_input_box.y = Window.height - 100
            self.falling_input_box.text = ""
            self.choose_target_word()

    def check_game_over(self):
        return self.falling_input_box.y + self.falling_input_box.height < 0

    def game_over(self):
        self.clock_event.cancel()
        self.clear_widgets()

        game_over_label = Label(text="Game Over!", font_size=30)
        self.add_widget(game_over_label)

        final_label = Label(text=f"Final Score: {self.score}\nTime taken: {30 - self.time_left:.2f} seconds", font_size=20)
        self.add_widget(final_label)

        restart_button = Button(text="Restart", on_press=self.restart_game)
        self.add_widget(restart_button)

    def win(self):
        self.clock_event.cancel()
        self.clear_widgets()

        win_label = Label(text="WIN!", font_size=30)
        self.add_widget(win_label)

        restart_button = Button(text="Restart", on_press=self.restart_game)
        self.add_widget(restart_button)

    def restart_game(self, instance):
        self.clear_widgets()
        self.__init__()

    def choose_target_word(self):
        self.target_word = random.choice(self.wordlist)
        self.word_label.text = self.target_word

class TypingGameApp(App):
    def build(self):
        sm = ScreenManager()

        start_page = StartPage(name="start", app=self)
        game_screen = Screen(name="game")  # เปลี่ยน TypingGame เป็น Screen

        # เพิ่ม TypingGame เป็นวิดเจ็ตลงใน Screen
        game_screen.add_widget(TypingGame())

        sm.add_widget(start_page)
        sm.add_widget(game_screen)

        sm.current = "start"

        return sm

class StartPage(Screen):
    def __init__(self, app, **kwargs):
        super(StartPage, self).__init__(**kwargs)
        self.app = app

        start_button = Button(text="Start", on_press=self.start_game, size_hint=(None, None), size=(200, 100), background_color=(0, 1, 0, 1))
        start_button.pos = (Window.width / 2 - start_button.width / 2, Window.height / 2 - start_button.height / 4)

        self.add_widget(start_button)
        self.children.append(start_button)

    def on_window_resize(self, window, width, height):
        self.ids.start_button.pos = (width / 2 - self.ids.start_button.width / 2, height / 2 - self.ids.start_button.height / 2)

    def start_game(self, instance):
        self.app.root.current = "game"

if __name__ == "__main__":
    TypingGameApp().run()