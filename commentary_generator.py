import json

def parse_pgn_with_stockfish_and_save(file_path, output_file, stockfish_api):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    games = []  # List to hold all game data
    current_game = {}  # Dictionary to hold metadata and moves for a single game
    moves = []  # List to hold moves
    reading_moves = False

    game_counter = 1  # Counter for game numbering

    for line in lines:
        line = line.strip()
        
        if line.startswith("["):  # Metadata lines
            key, value = line[1:-1].split(" ", 1)
            current_game[key] = value.strip('"')
        elif line == "":  # Empty line indicates the end of metadata/start of moves
            if not reading_moves:
                reading_moves = True
            else:
                # End of current game
                if moves:
                    # Process moves and enrich with Stockfish analysis
                    current_game["GameData"] = process_moves_with_stockfish(moves, stockfish_api)
                    games.append(current_game)
                current_game = {}
                moves = []
                reading_moves = False
        elif reading_moves:  # Moves section
            moves.extend(line.split())

    # Append the last game if not already added
    if current_game and moves:
        current_game["GameData"] = process_moves_with_stockfish(moves, stockfish_api)
        games.append(current_game)

    # Save games data to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(games, json_file, indent=4)

    print(f"Detailed game data saved to {output_file} successfully!")

def process_moves_with_stockfish(moves, stockfish_api):
    """
    Process the moves of a game and enrich them with Stockfish analysis.
    """
    move_data = {}
    fen = "starting FEN here"  # Replace with the starting FEN for chess
    for i, move in enumerate(moves):
        player = "White" if i % 2 == 0 else "Black"  # Determine player based on move index
        stockfish_result = get_stockfish_analysis(fen, stockfish_api)  # Simulated call to Stockfish API
        
        move_data[f"Move {i + 1}"] = {
            "Player": player,
            "FEN": fen,
            "Depth": stockfish_result["depth"],
            "StockfishResult": stockfish_result
        }
        
        # Update the FEN after this move (you can use a library like `python-chess` for FEN updates)
        fen = update_fen_with_move(fen, move)

    return move_data

def get_stockfish_analysis(fen, stockfish_api):
    """
    Simulated function to get Stockfish analysis for a given FEN.
    Replace this with actual API calls to Stockfish.
    """
    # Replace the below dictionary with real Stockfish output
    return {
        "success": True,
        "depth": 20,
        "evaluation": "+0.34",
        "bestMove": "e2e4",
        "nodes": 1234567
    }

def update_fen_with_move(fen, move):
    """
    Simulated function to update the FEN string after a move.
    Replace this with an actual implementation using a library like `python-chess`.
    """
    # Simulate a FEN update (this needs to be replaced with real logic)
    return fen + f" {move}"

# Example usage
input_file = "dataset-game1.pgn"  # Replace with your PGN file path
output_file = "refinedDataset.json"
stockfish_api = "https://stockfish.online/api/s/v2.php"  # Replace with your actual Stockfish API endpoint
parse_pgn_with_stockfish_and_save(input_file, output_file, stockfish_api)
