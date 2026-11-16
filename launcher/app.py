from kivy.app import App


class TestApp(App):
    def say_hello(self):
        self.root.ids.output.text = "Button pressed!"


if __name__ == "__main__":
    TestApp().run()
