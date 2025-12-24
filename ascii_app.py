from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Button, Label, Select, Static
from textual import on
import pyfiglet
import os
import glob
from datetime import datetime

class ASCIIApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #sidebar {
        width: 30;
        dock: left;
        background: $panel;
        padding: 1 2;
        border-right: heavy $primary;
    }

    #main-content {
        padding: 1 2;
        width: 100%;
        height: 100%;
        align: center middle;
    }

    #ascii-output {
        width: 100%;
        height: auto;
        border: solid $accent;
        padding: 1;
        text-align: center;
        color: $text;
        overflow: auto;
    }

    .title {
        text-align: center;
        margin-bottom: 2;
        color: $secondary;
        text-style: bold;
    }

    Input {
        margin-bottom: 1;
    }

    Select {
        margin-bottom: 1;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }

    #status-msg {
        color: $success;
        text-align: center;
        margin-top: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.fonts = []
        self.default_font = "ansi_shadow" # Use ansi_shadow as close match to screensaver
        self.current_art = ""

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Settings", classes="title")
                yield Label("Text:")
                yield Input(placeholder="Type here...", id="text-input")
                yield Label("Font:")
                yield Select([], id="font-select", allow_blank=False)
                yield Button("Save to File", id="save-btn", variant="primary")
                yield Label("", id="status-msg")
            
            with Container(id="main-content"):
                yield Static("", id="ascii-output")

        yield Footer()

    def on_mount(self) -> None:
        # Check for custom fonts in ./fonts directory and install them
        # This is necessary because pyfiglet needs fonts to be in its internal directory to load by name easily.
        custom_fonts_path = os.path.join(os.getcwd(), 'fonts')
        installed_fonts = pyfiglet.FigletFont.getFonts()
        
        if os.path.exists(custom_fonts_path):
            flag_new_fonts_installed = False
            for file in glob.glob(os.path.join(custom_fonts_path, '*.flf')):
                font_name = os.path.splitext(os.path.basename(file))[0]
                # If font is not already known to pyfiglet, install it
                if font_name not in installed_fonts:
                    try:
                        pyfiglet.FigletFont.installFonts(file)
                        flag_new_fonts_installed = True
                    except Exception as e:
                        # Silently fail or log? For TUI, maybe just ignore
                        pass
        
        # Reload fonts list if we installed anything
        self.fonts = sorted(pyfiglet.FigletFont.getFonts())
        
        # Populate select
        font_options = [(f, f) for f in self.fonts]
        
        # Try to set default font, fallback if not found
        default = self.default_font if self.default_font in self.fonts else "standard"
        
        select = self.query_one("#font-select", Select)
        select.set_options(font_options)
        select.value = default
        
        # Focus input
        self.query_one("#text-input").focus()

    @on(Input.Changed, "#text-input")
    def on_input_changed(self, event: Input.Changed) -> None:
        self.update_ascii()

    @on(Select.Changed, "#font-select")
    def on_font_changed(self, event: Select.Changed) -> None:
        self.update_ascii()

    def update_ascii(self) -> None:
        text = self.query_one("#text-input", Input).value
        font = self.query_one("#font-select", Select).value
        
        if not text:
            self.current_art = ""
            self.query_one("#ascii-output", Static).update("")
            return

        try:
            # Check if font is a custom file path or installed font
            # This is a simplified check. PyFiglet usually expects just the name if installed.
            # If it's a custom font in our list that isn't standard, we need to handle it.
            # For now, let's assume standard fonts + basic handling. 
            # If we really want custom folder support, we need to tell pyfiglet where to look 
            f = pyfiglet.Figlet(font=font)
            self.current_art = f.renderText(text)
            self.query_one("#ascii-output", Static).update(self.current_art)
        except Exception as e:
            self.query_one("#ascii-output", Static).update(f"Error loading font: {e}")

    @on(Button.Pressed, "#save-btn")
    def save_art(self) -> None:
        if not self.current_art:
            self.query_one("#status-msg", Label).update("Nothing to save!")
            return
            
        font = self.query_one("#font-select", Select).value
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{font}.txt"
        save_dir = os.path.join(os.getcwd(), "saved_art")
        
        filepath = os.path.join(save_dir, filename)
        
        try:
            with open(filepath, "w") as f:
                f.write(self.current_art)
            
            self.query_one("#status-msg", Label).update(f"Saved!")
        except Exception as e:
            self.query_one("#status-msg", Label).update(f"Error: {str(e)}")

        # Clear status message after 3 seconds
        self.set_timer(3, lambda: self.query_one("#status-msg", Label).update(""))

if __name__ == "__main__":
    app = ASCIIApp()
    app.run()
