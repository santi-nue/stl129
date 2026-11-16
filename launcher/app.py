# launcher/app.py
# -*- coding: utf-8 -*-

import os
import io
import traceback
import contextlib

from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock


class LauncherApp(App):
    def build(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kv_path = os.path.join(current_dir, "app.kv")

        # Return the root widget created from the KV file.
        return Builder.load_file(kv_path)

    def run_code(self):
        # Get the code from the TextInput in the KV file
        code = self.root.ids.code_input.text

        if not code.strip():
            self.set_output("Please paste some Python code first.")
            return

        self.set_output("Running...")

        output_buffer = io.StringIO()

        # Separate namespace for the pasted code
        user_globals = {
            "__name__": "__main__",
            "__builtins__": __builtins__
        }

        try:
            # Capture print() output and errors
            with contextlib.redirect_stdout(output_buffer):
                with contextlib.redirect_stderr(output_buffer):
                    exec(code, user_globals)

            output = output_buffer.getvalue().strip()

            if not output:
                output = "Code executed successfully, but nothing was printed."

        except Exception:
            partial_output = output_buffer.getvalue().strip()
            error_text = traceback.format_exc()

            if partial_output:
                output = partial_output + "\n\nERROR:\n" + error_text
            else:
                output = "ERROR:\n" + error_text

        self.set_output(output)

    def clear_output(self):
        self.set_output("Output cleared.")

    def set_output(self, text):
        # Update the output TextInput safely on Kivy's main thread
        Clock.schedule_once(lambda dt: setattr(
            self.root.ids.output_area,
            "text",
            text
        ))


if __name__ == "__main__":
    LauncherApp().run()
