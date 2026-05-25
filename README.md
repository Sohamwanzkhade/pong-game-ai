# 🎮 Pong Game AI

An interactive Pong game with AI opponent, dynamic difficulty adjustment, and full game analytics system.

## Phase 1: Pong Game ✅

### Features
- **Dual Control Systems**: Mouse movement + Arrow keys (Up/Down)
- **AI Opponent**: Intelligent computer player with dynamic difficulty
- **Real-time Physics**:
  - Ball collision detection with paddles and walls
  - Ball speed increases as rally continues
  - Paddle spin affects ball trajectory
- **Dynamic Difficulty**: AI adjusts based on score difference
- **Scoreboard**: Real-time score tracking
- **Game Statistics**: Ball speed, paddle speed, difficulty level display

### How to Play

1. **Open `index.html`** in your web browser
2. **Control the Left Paddle** (Green):
   - Move your mouse vertically, OR
   - Use UP/DOWN arrow keys
3. **Beat the AI** (Red paddle) to increase your score
4. **Reset** the game with the reset button

### Difficulty Levels
- **EASY**: AI has slower reaction time and misses occasionally
- **NORMAL**: Balanced gameplay (default)
- **HARD**: AI responds faster and tracks the ball more precisely
- **IMPOSSIBLE**: Maximum AI speed and accuracy

Difficulty automatically adjusts based on your performance!

### File Structure
```
.
├── index.html      # Game UI and structure
├── style.css       # Styling and responsive design
├── game.js         # Game logic and AI
└── README.md       # This file
```

---

## Phase 2: Data Analysis (Coming Soon) 📊
- Python script to analyze game statistics
- SQLite database to store game data
- Performance metrics and trend analysis

## Phase 3: Dynamic Difficulty (Coming Soon) 🎯
- Adapt AI difficulty based on historical performance
- Personalized game difficulty curves

## Phase 4: Cloud Integration (Coming Soon) ☁️
- Supabase integration for cloud saves
- Cross-device game progress sync
- Leaderboard system

---

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Game Rendering**: Canvas API
- **Physics**: Basic collision detection and velocity calculations

---

## Future Enhancements
- Sound effects and background music
- Power-ups and special abilities
- Multiplayer mode (local 2-player)
- Mobile touch controls
- Advanced AI using machine learning

---

**Created by**: Sohamwanzkhade  
**Repository**: https://github.com/Sohamwanzkhade/pong-game-ai