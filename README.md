## 🌟 Installation
To use this project, you'll need to install the necessary libraries. You can do this using pip:
```bash
pip install kivy
```

## :rocket: Project typing-attack-game

"Typing Attack" is a game in which players must type guard words The game uses random words from the "words.txt" and check information (TextInput) to destroy enemies (enemies) that float down from above. Players gain points when they type correctly and destroy enemies. The game uses increased time and speed of enemies to play.

## :computer: Program operation
1) Start Screen (StartScreen class): This is the start screen that displays the game name and a "Start Game" button when the player clicks this button. The program will change to the Game Screen.

2) Game Screen (TypingAttackGame class): This is the game's home screen with the play area, TextInput fields for typing words, and a "Restart" button to start a new game. The game uses random words from the "words.txt" file and destroys enemies that float down. The player must type the correct word to destroy the enemy and gain points. The timer will be counted down and the game will end when the timer runs out.

3) Game Over Screen (class GameOverScreen): This is the splash screen when the game ends, showing the score the player will get and has a "New Game" button to start a new game.

4) Main App (TypingAttackApp class): The main class used to create and manage screens and screen transitions. It includes ScreenManager. to manage all screens. The app will start at the "Start Screen" screen and when the player clicks "Start Game" it will switch to the "Game Screen" screen.