from flask import Flask, render_template, url_for, request
from config import Config
import netflix_randomizer

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        genre = request.form.get('genres')
        print(genre)
        movie = netflix_randomizer.randomize(genre)
        movie_title = movie['title']
        movie_desc = movie['description']
        movie_img = movie['img']

    else:
        movie = netflix_randomizer.randomize('children')
        movie_title = movie['title']
        movie_desc = movie['description']
        movie_img = movie['img']
        genre = 'all'

    return render_template('home.html', title='Home', movie_title=movie_title, movie_desc=movie_desc, movie_img=movie_img, genre=genre)


if __name__ == '__main__':
    app.run(debug=True)
