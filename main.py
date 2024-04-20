from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.sqlite3'  # SQLite database for demonstration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), unique=True, nullable=False)
    answer = db.Column(db.String(255), unique=False, nullable=False)
    
    def __init__(self, question, answer):
        self._question = question
        self._answer = answer
    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/trivia")
def trivia():
    return render_template("trivia.html", question="helo")


def init_data():
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()
