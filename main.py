
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import chess
import chess.engine

# Initialize the Flask application
app = Flask(__name__)

# Define the homepage route
@app.route('/')
def homepage():
    # Render the index.html file
    return render_template('index.html')

# Define the start game route
@app.route('/start_game')
def start_game():
    # Get the desired rating for the computer opponent
    rating = request.args.get('rating')

    # Initialize the chess game
    game = chess.Board()

    # Create the chess engine
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")

    # Set the engine's rating
    engine.configure({'Skill Level': rating})

    # Redirect to the game page
    return redirect(url_for('game', game=game, engine=engine))

# Define the make move route
@app.route('/make_move')
def make_move():
    # Get the current game state and the user's move
    game = chess.Board(request.args.get('game'))
    user_move = request.args.get('move')

    # Make the user's move
    game.push_san(user_move)

    # Get the computer's response move
    response_move = engine.play(game, chess.engine.Limit(time=0.1))

    # Update the game state
    game.push(response_move.move)

    # Return the updated game state
    return {'game': game.fen()}

# Define the get analysis route
@app.route('/get_analysis')
def get_analysis():
    # Get the current game state
    game = chess.Board(request.args.get('game'))

    # Evaluate the position
    score = engine.analyse(game, chess.engine.Limit(depth=20))

    # Get the best move
    best_move = score['pv'][0]

    # Return the analysis
    return {'score': score['score'], 'best_move': best_move}

# Define the about route
@app.route('/about')
def about():
    # Render the about.html file
    return render_template('about.html')

# Define the help route
@app.route('/help')
def help():
    # Render the help.html file
    return render_template('help.html')

# Start the Flask application
if __name__ == '__main__':
    app.run()
