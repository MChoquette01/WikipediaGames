from flask import Flask
from flask import render_template, request
from flask_bootstrap import Bootstrap
from flask_datepicker import Datepicker
app = Flask(__name__)
import APIHelper
import random
from datetime import datetime

# Hint on how to setup drag/drop in Flask: https://www.youtube.com/watch?v=koNz6XGbkpA

class WikiGame:

    def __init__(self):
        self.number_of_moves = 0

@app.route('/')
def welcome_screen():

    random.shuffle(article_rank)
    return render_template('puzzle.html', article_rank=article_rank, date=date_formal)

@app.route('/check', methods=['POST', 'GET'])
def check():
    """Report back to user how many spots are correct"""

    game.number_of_moves += 1
    if game.number_of_moves >= 1:
        moves_line = f"({game.number_of_moves} moves)"
    else:
        moves_line = f"({game.number_of_moves} move)"
    guessed_order = request.form['order'].split(',')
    correct_count = 0
    for i in range(len(guessed_order)):
        # if the ith article is correctly in the ith spot...
        if i + 1 == int(guessed_order[i]):
            correct_count += 1
    if correct_count == len(guessed_order):
        return f'You win! {moves_line}'
    else:
        return f'You have {correct_count} correct! {moves_line}'


@app.route('/new_game', methods=['POST', 'GET'])
def new_game():
    """Spin up a new game for a chosen date"""

    date = request.form['date-picker'].replace("-", "/")
    date_formal = datetime.strptime(date, "%Y/%m/%d").strftime("%B %d, %Y")
    article_rank = APIHelper.get_trending_articles(date=date)
    random.shuffle(article_rank)
    return render_template('puzzle.html', article_rank=article_rank, date=date_formal)


if __name__ == '__main__':
    date = datetime.now().strftime("%Y/%m/%d")
    date_formal = datetime.now().strftime("%B %d, %Y")
    article_rank = APIHelper.get_trending_articles(date=date)
    game = WikiGame()
    Bootstrap(app)
    datepicker = Datepicker(app)
    #app.run(debug=True, use_reloader=False, port=3134)  # for testing
    app.run(debug=True, host="0.0.0.0", port=3134)  # for deploying