import requests
import chess
import chess.pgn


def analyze_with_stockfish_api(fen, depth):
    """
    Sends the FEN and depth to Stockfish API for analysis using a GET request.

    Args:
        fen (str): The FEN string representing the board state.
        depth (int): Depth for Stockfish analysis (must be < 16).

    Returns:
        dict: The response from the Stockfish API or an error message.
    """
    if depth >= 16:
        depth = 15  # Adjust to the max accepted depth

    api_url = "https://stockfish.online/api/s/v2.php"  # Stockfish API endpoint

    params = {
        "fen": fen,
        "depth": depth
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        if not response.text.strip():
            return {"error": "Empty response from API"}

        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


def parse_pgn_and_analyze(pgn_file_path, depth=15):
    """
    Parses a .pgn file, iterates through multiple games, extracts all intermediate FEN positions for each move,
    and analyzes them using the Stockfish API.

    Args:
        pgn_file_path (str): Path to the .pgn file containing the games.
        depth (int): Depth for Stockfish analysis (default is 15).

    Returns:
        None
    """
    with open(pgn_file_path, 'r') as pgn_file:
        game_counter = 0

        while True:
            # Read each game in the PGN file
            game = chess.pgn.read_game(pgn_file)
            if game is None:  # End of file
                print("End of PGN file reached.")
                break
            
            game_counter += 1
            print(f"\nAnalyzing Game {game_counter}:")
            
            # Extract metadata from the game
            event = game.headers.get("Event", "Unknown Event")
            white_player = game.headers.get("White", "Unknown Player")
            black_player = game.headers.get("Black", "Unknown Player")
            result = game.headers.get("Result", "Unknown Result")
            
            print(f"Event: {event}")
            print(f"White: {white_player}")
            print(f"Black: {black_player}")
            print(f"Result: {result}")
            print("-" * 30)
            
            # Initialize the board and replay the game
            board = game.board()
            move_counter = 0

            for move in game.mainline_moves():
                board.push(move)  # Play the move
                move_counter += 1
                
                # Determine whether the move was made by White or Black
                player = "White" if move_counter % 2 == 1 else "Black"
                
                # Generate FEN for the current position
                current_fen = board.fen()
                
                # Call Stockfish API for analysis
                stockfish_output = analyze_with_stockfish_api(current_fen, depth)

                # Print results for the current move
                print(f"Move {move_counter} by {player}: {move}")
                print(f"FEN: {current_fen}")
                print(f"Stockfish Output: {stockfish_output}")
                print("-" * 30)

            print("=" * 50)


# Example Usage
if __name__ == "__main__":
    # Path to your .pgn file containing multiple games
    pgn_path = "datase.pgn"  # Replace with the actual path to your .pgn file
    
    # Call the function to parse the PGN file and analyze all moves
    parse_pgn_and_analyze(pgn_path, depth=15)
