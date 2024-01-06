import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class MyApp(App):

    def build(self):
        self.layout = GridLayout(cols=5, rows=5)
        for i in range(25):
            self.layout.add_widget(Label(text=""))
        return self.layout

    def on_touch_down(self, touch):
        x, y = touch.pos
        i, j = int(y // (self.layout.height / 5)), int(x // (self.layout.width / 5))
        
        cell_index = i * 5 + j
        cell = self.layout.children[cell_index]
        
        if cell.text == "":
            cell.text = "o"
            if self.check_level(i, j):
                self.next_level()

    def check_level(self, i, j):
        count_row = sum(1 for k in range(5) if self.layout.children[i * 5 + k].text == "o")
        count_col = sum(1 for k in range(5) if self.layout.children[k * 5 + j].text == "o")
        return count_row == int(self.layout.children[i * 5].text) and count_col == int(self.layout.children[j].text)

    def next_level(self):
        for widget in self.layout.children:
            widget.text = ""
        self.layout.children[0].text = "2"
        self.layout.children[1].text = "3"

if __name__ == "__main__":
    MyApp().run()