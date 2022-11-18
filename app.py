from flask import Flask, jsonify, request
import controllers.games_controller as games_controller

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Welcome to the Game Search Api!"


@app.route("/games")
def get_games():
    game_list = games_controller.get_all()
    return jsonify(game_list)


@app.route("/games/yearRange")
def get_games_by_year_range():
    args = request.args
    start_year = args.get('start_year')
    end_year = args.get('end_year')

    game_list = games_controller.get_games_by_year_range([start_year, end_year])
    return jsonify(game_list)


if __name__ == "__main__":
    app.run(debug=True)
