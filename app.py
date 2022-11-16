from flask import Flask, jsonify, request
import controllers.gamesController as gamesController

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Welcome to the Game Search Api!"


@app.route("/games")
def getGames():
    gameList = gamesController.getAll()
    return jsonify(gameList)


@app.route("/games/yearRange")
def getGamesByYearRange():
    args = request.args
    print(args)
    startYear = args.get('startYear')
    endYear = args.get('endYear')

    gameList = gamesController.getGamesByYearRange([startYear, endYear])
    return jsonify(gameList)


if __name__ == "__main__":
    app.run(debug=True)
