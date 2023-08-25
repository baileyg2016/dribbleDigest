from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import rumors_controller, news_controller, betting_lines_controller, top_five_articles_controller, top_five_rumors_controller, top_betting_lines_controller, get_email_subject_from_articles_controller
from dataclasses import asdict
import threading
import json
import digest

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
    bets = body.get('includeBets')
    favorite_sport = body.get('favoriteSports')
    favorite_team = body.get('favoriteTeams')

    bets = betting_lines_controller(favorite_sport, favorite_team)

    # Implement your logic to get bets here
    return jsonify({'bets': bets})


@app.route('/', methods=['POST'])
def get_data():
    body = request.get_json()
    print(body)
    email = body.get('email')
    includeBets = body.get('includeBets')
    favorite_sport = body.get('favoriteLeagues')
    favorite_team = body.get('favoriteTeams')

    favorite_sport = [s.lower() for s in favorite_sport]
    
    # Create containers for the results
    articles = []
    rumors = []
    bets = []
    email_subject = ''

    # Define a function for each thread
    def fetch_articles():
        nonlocal articles
        articles = top_five_articles_controller(favorite_sport, favorite_team)

    def fetch_rumors():
        nonlocal rumors
        rumors = top_five_rumors_controller(favorite_sport, favorite_team)

    def fetch_bets():
        nonlocal bets
        if includeBets:
            bets = top_betting_lines_controller(
                favorite_sport, favorite_team)

    # Create the threads
    threads = []
    threads.append(threading.Thread(target=fetch_articles))
    threads.append(threading.Thread(target=fetch_rumors))
    if includeBets:
        threads.append(threading.Thread(target=fetch_bets))
    # threads.append(threading.Thread(target=fetch_email_subject))

    # Start the threads
    for thread in threads:
        thread.start()



    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # we don't want this as a thread because we have to wait for all of the articles
    email_subject = get_email_subject_from_articles_controller([a['content'] for a in articles])

    print('\n\n\n\n\n\n\n\n')
    print(email_subject)
    print(articles)
    print(rumors)
    print(bets)

    digest.send(email, email_subject, "1 Trade Each NFL Team Should Propose Before the 2023 Season", "https://media.bleacherreport.com/image/upload/w_800,h_533,c_fill/v1692802630/fwh2efa0ulz2d8q5fz72.jpg", articles, rumors, bets, includeBets)

    return jsonify({'articles': json.dumps(articles, default=str), 'rumors': json.dumps(rumors, default=str), 'bets': json.dumps(bets, default=str), 'email_subject': email_subject})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
