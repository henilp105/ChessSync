# ChessSync

ChessSync is a real-time chess synchronization application that uses Redis for state management. It enables players to synchronize their chess games seamlessly across multiple devices and platforms. The application also integrates a chess engine for validating moves and providing game functionality.

live website: https://chess-sync.vercel.app/

## Features

- **Real-time Synchronization:** Sync game state in real-time across all connected devices.
- **Redis-based State Management:** Efficiently manage and store game states using Redis.
- **Chess Engine Integration:** Built-in chess engine for move validation.
- **Cross-Platform Support:** Play on different devices and platforms.
- **Move Validation:** Ensure all moves comply with chess rules.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/henilp105/ChessSync.git
   cd ChessSync
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Execution

To start the ChessSync application, run:

```bash
python main.py
```

## Configuration

You can configure ChessSync using environment variables. Create a `.env` file in the root directory with the following content:

```
REDIS_HOST=localhost
SECRET_KEY=your_secret_key_here
```

Ensure that Redis is running on the specified host and port.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
