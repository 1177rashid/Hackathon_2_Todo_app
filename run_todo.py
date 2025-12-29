"""
Startup script for Todo Application with proper encoding configuration.
This ensures emojis and colors display correctly on Windows.
"""
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    # Change console code page to UTF-8
    os.system('chcp 65001 > nul')

    # Reconfigure stdout and stderr to use UTF-8
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run main
from main import main

if __name__ == "__main__":
    main()
