
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import requests
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movies.db'
db = SQLAlchemy(app)


API_KEY = '6ff2c60e508fcbf095e8b43a17f7fdd3'
MOVIE_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
MOVIE_INFO_URL = 'https://api.themoviedb.org/3/movie'
MOVIE_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'



class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(1000), nullable=False)
# db.create_all()


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://m.media-amazon.com/images/M/MV5BMTcxNDQ5MzAyOV5BMl5BanBnXkFtZTYwMjkxMTU3._V1_FMjpg_UX1000_.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()
class Add_Form(FlaskForm):
    title = StringField('Title',[DataRequired()])
    submit = SubmitField('submit')

class Rating_Form(FlaskForm):
    rating = StringField('Rating')
    review = StringField('Review')
    submit = SubmitField('Submit')

@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking=len(all_movies)-i
    db.session.commit()
    return render_template("index.html", movies = all_movies)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = Add_Form()
    if form.validate_on_submit():
        response = requests.get(MOVIE_SEARCH_URL, params={"api_key":API_KEY, "query":form.title.data})
        data = response.json()['results']
        return render_template('select.html', data=data)
    return render_template('add.html', form=form)


@app.route('/movie-details')
def movie_details():
    movie_api_id = request.args.get('id')
    info_url = f"{MOVIE_INFO_URL}/{movie_api_id}"
    info = requests.get(info_url, params={"api_key":API_KEY, "language":"en_US"})
    info_data = info.json()
    new_movie = Movie(
        title = info_data['title'],
        description = info_data['overview'],
        img_url = f"{MOVIE_IMAGE_URL}{info_data['poster_path']}",
        year = info_data['release_date'].split('-')[0]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('rate_movie', id=new_movie.id))


@app.route('/rate-movie', methods=['POST','GET'])
def rate_movie():
    form = Rating_Form()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        if form.rating.data!='':
            movie.rating = float(form.rating.data)
            db.session.commit()
        if form.review.data!='':
            movie.review = form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)

@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))







if __name__ == '__main__':
    app.run(debug=True)
