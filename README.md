Skybound Adventure ☁️
Skybound Adventure is a 2D side-scrolling platformer built with Python and pygame-ce (Pygame Community Edition). Jump between platforms, collect coins, defeat moving slimes, and reach the finish flag to complete each level.
Features
- Three levels with increasing difficulty
- Side-scrolling camera and parallax-style background
- Player movement and double jumping
- Floating platforms and gaps
- Collectible coins and a coin counter
- Moving slime enemies that can be defeated by jumping on them
- Three lives, restart, game-over, and victory screens
- Simple graphics drawn directly with Pygame; no external assets needed
Requirements
- Python 3.10 or newer (recommended)
- pygame-ce (see requirements.txt)
pygame-ce is imported in Python as pygame. You do not need to install the separate pygame package.

Installation
1. Clone the repository:
   git clone https://github.com/ajmastahking/SkyBoundAdventure.git
   cd SkyBoundAdventure
   Alternatively, download the project ZIP from GitHub and extract it.
2. (Optional) Create a virtual environment:
   Windows PowerShell:
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   macOS / Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   If you skip the virtual environment, install dependencies with:
   python -m pip install -r requirements.txt
3. Run the game:
   python skybound_adventure.py
   If using the Windows virtual environment without activating it:
   .\.venv\Scripts\python.exe skybound_adventure.py
Controls:
Key	Action
A / Left Arrow	Move left
D / Right Arrow	Move right
Space / W / Up Arrow	Jump (press again to double-jump)
Enter	Start game / continue to next level / play again
R	Restart from level 1
Esc	Quit


How to Play
1. Press Enter on the title screen.
2. Move across platforms and jump over gaps.
3. Collect coins along the way.
4. Jump onto slimes from above to defeat them; touching them from the side costs a life.
5. Reach the pink finish flag to advance.
6. Complete all three levels to win!
You start with three lives. Losing all three ends the run. Coins are counted separately for each level.
Project Structure
SkyBoundAdventure/
├── skybound_adventure.py   # Main game source code
├── README.md               # Project documentation
└── requirements.txt        # Python dependency
Running in Visual Studio Code
Open the project folder in VS Code and choose Python: Select Interpreter from the Command Palette (Ctrl+Shift+P). Select the Python environment where pygame-ce is installed (for example, .venv). Then run skybound_adventure.py.

If you see ModuleNotFoundError: No module named 'pygame', make sure the interpreter selected in VS Code is the same one used to install the dependencies.
Built With
- Python
- pygame-ce
Future Ideas
- Character animations and sprite sheets
- Sound effects and background music
- More levels, checkpoints, and boss fights
- A main menu with level selection
