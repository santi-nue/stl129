# launcher/app.py
# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.app import App


class LauncherApp(App):
    def build(self):
        # Load the KV file and RETURN its root widget.
        return Builder.load_file("launcher/app.kv")

    def say_hello(self):
        self.root.ids.output.text = "Button pressed!"

    def clear_output(self):
        self.root.ids.output.text = "Waiting..."


if __name__ == "__main__":
    LauncherApp().run()
