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
    # Ensure depth is within the acceptable range
    if depth >= 16:
        depth = 15  # Adjust to the max accepted depth
    
    api_url = "https://stockfish.online/api/s/v2.php"  # Stockfish API endpoint
    
    # Prepare the parameters for the GET request
    params = {
        "fen": fen,
        "depth": depth
    }
    
    try:
        # Send the GET request with the parameters
        response = requests.get(api_url, params=params)
        
        # Check for a successful response
        response.raise_for_status()  # Raises an exception for 4xx/5xx HTTP status codes
        
        # Check if the response is empty
        if not response.text.strip():
            return {"error": "Empty response from API"}
        
        # Try to parse the JSON response
        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


def parse_pgn_to_api_format(pgn_file_path, depth=15):
    """
    Parses a .pgn file and extracts FEN positions along with the specified depth for Stockfish API input.

    Args:
        pgn_file_path (str): Path to the .pgn file containing the games.
        depth (int): Depth for Stockfish analysis (default is 15).

    Returns:
        list: A list of dictionaries, each containing the FEN and depth for Stockfish.
    """
    games_data = []

    with open(pgn_file_path, 'r') as pgn_file:
        while True:
            # Read each game in the PGN file
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # No more games to read
            
            # Initialize the board and replay the game
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)  # Play the move
            
            # Get the final FEN position of the game
            final_fen = board.fen()
            
            # Append FEN and depth as a Stockfish API-friendly format
            games_data.append({
                "fen": final_fen,
                "depth": depth
            })
    
    return games_data


# Example Usage
if __name__ == "__main__":
    # Path to your .pgn file
    pgn_path = "lichess_db_standard_rated_2013-11.pgn"  # Replace with the actual path to your .pgn file
    
    # Call the function to parse the PGN file
    stockfish_inputs = parse_pgn_to_api_format(pgn_path, depth=15)

    # Iterate over the parsed games and analyze with Stockfish API
    for i, game_data in enumerate(stockfish_inputs):
        print(f"Analyzing Game {i+1}:")
        print(f"FEN: {game_data['fen']}")
        print(f"Depth: {game_data['depth']}")
        
        # Get the Stockfish analysis result
        stockfish_output = analyze_with_stockfish_api(game_data['fen'], game_data['depth'])
        
        # Print the Stockfish output for each game
        print("Stockfish Output:", stockfish_output)
        print("-" * 30)
