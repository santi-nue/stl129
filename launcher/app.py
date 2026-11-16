# launcher/app.py
# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.app import App


# Load the KV file explicitly.
# This must match the location of app.kv.
Builder.load_file("launcher/app.kv")


class LauncherApp(App):
    def say_hello(self):
        self.root.ids.output.text = "Button pressed!"

    def clear_output(self):
        self.root.ids.output.text = "Waiting..."


if __name__ == "__main__":
    LauncherApp().run()
