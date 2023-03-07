from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Creating Database
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///books-library.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

# Creating Table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

db.create_all()
all_books=[]

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', all_books = all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method=='POST':
        book_id = request.form['id']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    bookid = request.args.get('id')
    book = Book.query.get(bookid)
    return render_template('edit.html', book=book)

@app.route('/delete')
def delete():
    
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    app.run(debug=True)

