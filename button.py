from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyGame(App):
    def build(self):
        # สร้างหน้าต่างและปุ่ม
        layout = BoxLayout(orientation='vertical')
        button = Button(text='Click me!', size_hint=(None, None), size=(200, 100))
        button.bind(on_press=self.on_button_click)
        
        # เพิ่มปุ่มลงในหน้าต่าง
        layout.add_widget(button)
        
        return layout

    def on_button_click(self, instance):
        print('Button clicked!')

if __name__ == '__main__':
    MyGame().run()