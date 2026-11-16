# main.py

__version__ = "1.0.0"

import io
import contextlib
import traceback
import threading

from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


# Set a desktop window size only on desktop platforms.
# Do not force a size on Android; Android controls the app window.
if platform not in ("android", "ios"):
    from kivy.core.window import Window
    Window.size = (900, 650)


class PythonCodeRunnerApp(App):
    def build(self):
        self.title = "Python Code Runner"
        self._running = False

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        # Code input area
        self.code_input = TextInput(
            text=(
                "# Paste Python code here, then press Run code\n"
                "print('Hello from Kivy!')\n"
                "\n"
                "for i in range(3):\n"
                "    print(i)\n"
            ),
            font_size=sp(16),
            multiline=True,
            size_hint=(1, 0.55)
        )
        root.add_widget(self.code_input)

        # Run button
        run_button = Button(
            text="Run code",
            size_hint=(1, None),
            height=dp(48),
            bold=True
        )
        run_button.bind(on_press=self.run_code)
        root.add_widget(run_button)

        # Output label
        output_label = Label(
            text="Output:",
            size_hint=(1, None),
            height=dp(24),
            bold=True,
            halign="left",
            valign="middle"
        )
        output_label.bind(size=lambda instance, value: setattr(
            instance, "text_size", (instance.width, instance.height)
        ))
        root.add_widget(output_label)

        # Output area
        self.output = TextInput(
            readonly=True,
            font_size=sp(14),
            multiline=True,
            text="Ready.",
            size_hint=(1, 0.45)
        )
        root.add_widget(self.output)

        return root

    def run_code(self, instance):
        if self._running:
            self.set_output("Already running. Please wait...")
            return

        code = self.code_input.text

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
        Clock.schedule_once(lambda dt: setattr(self.output, "text", text))


if __name__ == "__main__":
    PythonCodeRunnerApp().run()
