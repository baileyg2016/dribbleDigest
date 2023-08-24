from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import rumors_controller, news_controller, betting_lines_controller
from dataclasses import asdict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/rumors', methods=['GET'])
def get_rumors():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')
    rumors = rumors_controller(favorite_sport, favorite_team)

    rumors = [asdict(r) for r in rumors]

    # Implement your logic to get bets here
    return jsonify({"rumors": rumors})

@app.route('/news', methods=['GET'])
def get_news():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')

    articles = news_controller(favorite_sport, favorite_team)
    articles = [asdict(a) for a in articles]

    # Implement your logic to get bets here
    return jsonify({'bets': bets, 'favorite_sport': favorite_sport, 'favorite_team': favorite_team, 'articles': articles})

@app.route('/bets', methods=['GET'])
def get_bets():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')

    bets = betting_lines_controller(favorite_sport, favorite_team)

    # Implement your logic to get bets here
    return jsonify({ 'bets': bets })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
