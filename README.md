# 🐍 Snake Game (Mini Project)

A classic Snake Game built using **Python** and **Pygame** to explore 2D game development, UI interaction, and real-time gameplay mechanics.

---

## 🎯 Project Objectives

- Design a playable snake game in Python
- Use **Pygame** for 2D graphics and event handling
- Implement features like:
  - Difficulty selection (Easy/Medium/Hard)
  - Score tracking
  - Game over scenarios with visuals

---

## 🛠️ Tech Stack

- **Language:** Python 3  
- **Libraries:**  
  - `pygame` (graphics, game loop, events)  
  - `random` (standard library, food placement)  
- **Tools:** VS Code  
- **OS:** Windows  

---

## 🧩 System Architecture

### Modules:
- Game Initialization
- Difficulty Selection Screen
- Main Game Loop (Movement, Food, Score, Collision)
- Game Over Screens

---

## 🧪 Implementation Overview

1. Game window setup using Pygame
2. User selects difficulty level
3. Game loop begins:
   - Responds to keyboard input
   - Updates snake position
   - Detects collision with wall, self, or obstacles
   - Draws game elements
4. Displays Game Over screen based on the type of collision

---

## 📸 Screenshots

Find the screenshot folder [**`Snake Game SS`**](./Snake%20Game%20SS/) in this repo for images like:

- Start Window
- Difficulty Selection
- Gameplay (Easy, Medium, Hard)
- Pause/Resume
- Game Over (Wall, Obstacle, Self)

---

## ✅ Results

- Fully functional snake game with difficulty levels
- Smooth gameplay across modes
- Responsive user input
- Real-time score updates

---

## ⚔️ Challenges Faced

| Challenge | Solution |
|----------|----------|
| Speed scaling with gameplay | Incremented speed as snake length increased |
| Difficulty tuning | Separated logic for Easy, Medium, Hard modes |

---

## 📚 References

- [Pygame Docs](https://www.pygame.org/docs/)
- [GeeksForGeeks - Snake Game Tutorial](https://www.geeksforgeeks.org/snake-game-in-python/)

---

## 📦 How to Run

1. Install Pygame:
   ```bash
   pip install pygame
