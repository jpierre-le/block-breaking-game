# Block Breaking Game

A simple block-breaking game built using Python and Pygame.

## Overview

Block Breaking Game is a classic block-breaking game implemented in Python with realistic physics, sound effects, and celebratory animations. The game features:
- **Paddle Control:** Move the paddle using the left/right arrow keys.
- **Constant Speed Ball:** The ball maintains a constant speed for consistent gameplay.
- **Block Layout:** 12 blocks arranged in a grid (3 rows x 4 columns).
- **Sound Effects:** Collision sounds and a celebratory fanfare on game clear. *(Requires `hit.mp3` and `fanfare.mp3` files in the same directory.)*
- **Start Screen:** The game begins only after clicking the central "Start" button.
- **Confetti Animation:** Enjoy a fun confetti animation when you clear all blocks.
- **Score Board:** Your score is tracked and displayed in the top-right corner.

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jpierre-le/block-breaking-game.git
Navigate to the Project Directory:

bash
cd block-breaking-game
Install Dependencies:

bash
pip install pygame
Usage
Place Sound Files:

Make sure that hit.mp3 and fanfare.mp3 are located in the same directory as the game source code. If you use different files or paths, update the code accordingly.

Run the Game:

bash
python main.py
Gameplay:

On the start screen, click the "Start" button at the center to begin the game.
Use the left and right arrow keys to move the paddle.
Bounce the ball to break the 12 blocks.
When all blocks are broken, a celebratory confetti animation and fanfare will play.
If the ball falls below the paddle, the game is over and returns to the start screen.
Contributing
Contributions are welcome! Please feel free to submit issues or pull requests to improve the game.

License
This project is licensed under the MIT License.

Acknowledgements
Developed with Pygame
Inspired by classic block-breaking games.
