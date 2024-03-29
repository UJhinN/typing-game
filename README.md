## 🌟 Installation
To use this project, you'll need to install the necessary libraries. You can do this using pip:
```bash
pip install kivy
```

## :rocket: Project typing-attack-game

"Typing Attack" is a game in which players must type guard words The game uses random words from the "words.txt" and check information (TextInput) to destroy enemies (enemies) that float down from above. Players gain points when they type correctly and destroy enemies. The game uses increased time and speed of enemies to play.

## :computer: Program operation

This program is a typing game presented in a GUI format using the Kivy framework. Kivy is a Python framework for building applications and games with a graphical user interface (GUI). The program consists of multiple screens that manage different states of the application:

1) Start Screen:

Displays the game name "TYPING-ATTACK," "Start Game" button, "High Score" button, and volume control button.
When the "Start Game" button is pressed, it switches to the Game screen.
Pressing the "High Score" button switches to the High Score screen.
The volume control button is used to adjust the game volume.

2) Game Screen:

Inherits from BoxLayout and displays the main game screen.
Initializes default values for game components such as score, enemies, sound, etc.
Imports enemies with random words from the words.txt file.
Players must type words correctly as enemies drop down.
Correctly typed words increase the score and remove the corresponding enemy.
Mistyped words result in score penalties.
The game has a timer, and when time runs out, the game ends.
The game speed increases at even score intervals.

3) Game Over Screen:

Displays the "Game Over" message, final score, and "New Game" button.
The "New Game" button resets the game and goes back to the Game screen.

4) High Score Screen:

Displays the current high score and a "Back" button.
The "Back" button returns to the Start screen.

5) Game Mechanics:

Enemies drop from the top, and players must type the corresponding words.
Players score points for correctly typed words and receive penalties for mistyped words.
The game has a timer, and it ends when time runs out.
The game speed increases at even score intervals.
Sound effects are used for correct and incorrect typing.

6) File and Data Handling:

Words for the game are loaded from the words.txt file.
High scores are stored in the high_score.txt file.

7) Volume Control:

The game includes sound effects for correct and incorrect typing.
A volume control button is provided.