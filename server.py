from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/rumors', methods=['GET'])
def get_rumors():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')
    # Implement your logic to get bets here
    return jsonify({'bets': bets, 'favorite_sport': favorite_sport, 'favorite_team': favorite_team})

@app.route('/news', methods=['GET'])
def get_news():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')
    # Implement your logic to get bets here
    return jsonify({'bets': bets, 'favorite_sport': favorite_sport, 'favorite_team': favorite_team})

@app.route('/bets', methods=['GET'])
def get_bets():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')
    # Implement your logic to get bets here
    return jsonify({'bets': bets, 'favorite_sport': favorite_sport, 'favorite_team': favorite_team})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
