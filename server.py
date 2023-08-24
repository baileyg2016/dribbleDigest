from flask import Flask, jsonify, request
from flask_cors import CORS
from main import scrape_espn_article, scrape_bleacher_report, get_bleacher_report_article, get_espn_data, bleacher_report_rumor_to_article
from dataclasses import asdict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/rumors', methods=['GET'])
def get_rumors():
    body = request.get_json()
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')
    rumors = []
    for sport in favorite_sport:
      rumors.extend(scrape_bleacher_report(sport))

    # Implement your logic to get bets here
    return jsonify({rumors: rumors})

@app.route('/news', methods=['GET'])
def get_news():
    body = request.get_json()

    articles = []
    bets = body.get('bets')
    favorite_sport = body.get('favorite_sport')
    favorite_team = body.get('favorite_team')

    for sport in favorite_sport:
      rumors = scrape_bleacher_report(sport)[:25]
      articles.extend([bleacher_report_rumor_to_article(rumor) for rumor in rumors])
      articles.extend(get_espn_data(sport))
    # print(articles)
    articles = [asdict(a) for a in articles]

    # Implement your logic to get bets here
    return jsonify({'bets': bets, 'favorite_sport': favorite_sport, 'favorite_team': favorite_team, 'articles': articles})

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
