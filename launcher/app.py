# main.py

__version__ = "1.0.0"

import io
import contextlib
import traceback
import threading

from kivy import platform
from kivy.app import App
from kivy.clock import Clock


# Set a desktop window size only on desktop platforms.
# Do not force a size on Android; Android controls the app window.
if platform not in ("android", "ios"):
    from kivy.core.window import Window
    Window.size = (900, 650)


class PythonCodeRunnerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._running = False

    def run_code(self):
        if self._running:
            self.set_output("Already running. Please wait...")
            return

        code = self.root.ids.code_input.text

        if not code.strip():
            self.set_output("Please paste some Python code first.")
            return

        self._running = True
        self.set_output("Running...")

        # Run the code in a background thread so the Kivy UI stays responsive.
        thread = threading.Thread(
            target=self.execute_code,
            args=(code,),
            daemon=True
        )
        thread.start()

    def clear_output(self):
        self.set_output("Output cleared.")

    def execute_code(self, code):
        output_buffer = io.StringIO()

        # Use a separate namespace so user variables do not overwrite app variables.
        execution_globals = {
            "__name__": "__main__",
            "__builtins__": __builtins__
        }

        try:
            with contextlib.redirect_stdout(output_buffer):
                with contextlib.redirect_stderr(output_buffer):
                    exec(code, execution_globals)

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

        self._running = False
        self.set_output(output)

    def set_output(self, text):
        # Kivy UI widgets must be changed on the main thread.
        Clock.schedule_once(lambda dt: setattr(
            self.root.ids.output_area,
            "text",
            text
        ))


if __name__ == "__main__":
    PythonCodeRunnerApp().run()
