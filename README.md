# Monopoly Board Game Simulator

A Python-based Monopoly board game simulator featuring object-oriented design with Player, GameBoard, Cell, and GameManager classes. The program implements a square map with 40 positions including start point, jail, bank, properties, chance events, and special tiles.

## Features

- **Object-Oriented Architecture**: Utilizes Player, Cell, GameBoard, and GameManager classes for modular code organization
- **10x10 Square Map Design**: Features 40 positions including start, jail, bank, properties, chance events, and special tiles
- **Complete Game Mechanics**: Implements dice rolling, property purchasing, rent payment, jail system, and random event handling
- **Multiplayer Support**: Supports 2-4 players with turn-based gameplay
- **Save/Load System**: JSON-based game state persistence with local text file storage
- **ASCII Board Display**: Clean, formatted board with player position tracking
- **Random Event System**: Includes money gains/losses, jail transfer, property stealing, and extra turns
- **Property Management**: Complete property ownership and rental fee collection system
- **Game Over Detection**: Automatic bankruptcy detection and winner determination

## Game Board Symbols

| Symbol | Description |
|--------|-------------|
| `0` | Start (Top-Left Corner) |
| `&` | Jail (Bottom-Right Corner) |
| `#` | Bank (Top-Right and Bottom-Left Corners) |
| `1-39` | Regular Spaces (Clockwise Path) |
| `$` | Property (Purchasable) |
| `?` | Chance Event |
| `!` | Special Property |
| `R/B/G/Y` | Player Markers (Red/Blue/Green/Yellow) |

## Getting Started

### Prerequisites

- Python 3.6 or higher
- No external dependencies required

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Monopoly-Game---Python-Simulator.git
cd Monopoly-Game---Python-Simulator

# Run the game
python main.py
```

### How to Play

1. **Start a New Game**: Run `python main.py` and select "New Game"
2. **Enter Player Information**: Input number of players (2-4) and player names
3. **Take Turns**: Each turn, press Enter to roll the dice
4. **Purchase Properties**: When landing on an unowned property, choose to buy it
5. **Pay Rent**: When landing on another player's property, pay rent automatically
6. **Collect Money**: Passing Go gives $200, landing on Bank gives $100
7. **Handle Events**: Chance and Special tiles trigger various events
8. **Avoid Jail**: If sent to jail, pay $50 to get out or wait 3 turns

## Project Structure

```
Monopoly-Game---Python-Simulator/
├── player.py          # Player class (name, money, position, properties)
├── game_board.py      # GameBoard class (map generation, display, cell management)
├── game_manager.py    # GameManager class (game flow, dice, event handling)
├── main.py            # Main program entry point
├── test_game.py       # Automated test script
├── test_save.txt      # Example save file
└── README.md          # Project documentation
```

## Game Mechanics

### Dice System
- Two six-sided dice rolled per turn
- Total roll determines movement distance (2-12)

### Property System
- Properties cost $100-$500 to purchase
- Rent ranges from $10-$100 based on property value
- Property owners collect rent from other players

### Jail System
- Landing on Go to Jail sends player directly to jail
- Players can pay $50 to exit or wait 3 turns
- No movement allowed while in jail

### Chance Events
- Collect $200
- Pay $100
- Go to Jail
- Get Extra Turn
- Move Back 3 Spaces

### Special Events
- Hotel Tax: Pay $50
- Amusement Park: Collect $100
- Developer: Steal Property from another player

## Save/Load System

The game automatically saves progress to `game_state.txt` in JSON format. The save file includes:
- Current turn number
- Current player index
- All player data (name, color, money, position, jail status)

## Built With

- **Python 3** - Programming language
- **Random Module** - Probability simulation
- **JSON Module** - Data serialization

## License

This project is for educational purposes.

## Acknowledgments

- Inspired by the classic Monopoly board game
- Designed for COMP9001 Final Project requirements

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
