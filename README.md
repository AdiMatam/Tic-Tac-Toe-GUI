# Tic-Tac-Toe-GUI
Simple tic-tac-toe game with tkinter module in python.   
PLAYER vs BOT

## Dependencies
Pillow: Used to place images on display (pip install pillow)  
Numpy: Used to manage the board and predict moves (pip install numpy)

## Usage
Run `launcher.py`  
tkinter window should open upon running

## Contents
`imgs folder`: Contains the images for "X" and "O." Other images may be added, but the filename must be retained.  

`gamegui.py`: Contains main game class. Manages 'legal moves', turns, ensures that user may not interrupt bot. Bot decision making also included in this file  

`widgets.py`: Components of the game.  
- Board: Make boxes (slots) in which "X" and "O" is placed
- Watch: Stopwatch for the game. Shows time-elapsed
- Tally: Displays total games played, how many 'user' wins, how many 'bot wins'

`launcher.py`: Imports gamegui and launches the program
## Future Updates
- Different modes
    - Easy - random moves
    - Medium - current
    - Hard - minimax AI (work in progress)
- Multiplayer capability (local network)
- Start-Screen, to get into the game (allows one to set modes)