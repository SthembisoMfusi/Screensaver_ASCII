# ASCII Art Generator TUI

A terminal-based application to generate ASCII art from text, featuring custom font support and file saving.

## Features
- **Live Preview**: Type and see the ASCII art instantly.
- **Font Selection**: Choose from over 400+ installed fonts including the default `ansi_shadow`.
- **Custom Fonts**: Add your own `.flf` files to the `fonts/` directory, and the app will load them automatically on startup.
- **Save to File**: Save your creations to the `saved_art/` directory with a single click.

## How to Run

### Linux / MacOS
Simply run the provided script:
```bash
./run.sh
```

Or manually:
```bash
# Create virtual env
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python ascii_app.py
```

## Adding Custom Fonts
1. Download a `.flf` font file (e.g. from [patorjk.com](http://patorjk.com/software/taag/)).
2. Place it in the `fonts/` directory.
3. Restart the application.