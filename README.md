# Chess_Playing_Dobot
### Packages in use:
- [python chess](https://python-chess.readthedocs.io/en/latest/) v1.9.3
- [python stockfish](https://pypi.org/project/stockfish/) v3.28.0
- [pygame](https://www.pygame.org/news) v2.1.2

-

### Setup
- Install Requirements with "pip install -r requirements.txt" <br>
- Download [ Stockfish chess engine ](https://stockfishchess.org/download/), unzip and copy the absolute path to the .exe file.<br>
Paste the absolute path to the .exe in line 10 of ChessEngine.py.
- To play against the own "AI", change the argument of the constructor argument against_stockfish of the ChessEngine object in ChessGame.py to "false".

#### Hint:
Make sure Stockfish has the right permissions to run on your system. <br>
Windows might block the .exe file. <br>

### How to play
- Run main.py
- Select a piece by clicking on it
- Select a square to move to by clicking on it
- Let the computer make its move by pressing spacebar
- If you want to undo a move, press 'u' on your keyboard
- If you want to reset the board, press 'r' on your keyboard
- 