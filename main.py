from flask import Flask, render_template, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3'  # SQLite database for demonstration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), unique=True, nullable=False)
    answer = db.Column(db.String(255), unique=False, nullable=False)
    
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
    
    def create(self):
        try:
            db.session.add(self) 
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    def read(self):
        return {
            "question":self.question,
            "answer":self.answer
        }
    
    
def initQuestions():
    with app.app_context():
        db.create_all()
        q1 = Question("What occasion corresponds to the longest day of the year?", "summer solstice")
        q2 = Question("What is the distance from earth to the sun?", "93 million miles")
        q3 = Question("What sport was featured on the first curved U.S. coin in 2014?", "Baseball")
        q4 = Question("Which country is the largest in the world?", "Russia")
        q5 = Question("M&M’S Fruit Chews would eventually become what popular candy?", "Starburst")
        q6 = Question("According to Guinness World Records, what's the best-selling book of all time?", "The Bible")
        q7 = Question("What U.S. state is home to Acadia National Park?", "Maine")
        q8 = Question("What is the only food that can never go bad?", "Honey")
        q9 = Question("What was the first animal to ever be cloned?", "A sheep")
        q10 = Question("What is the name of the pet dinosaur on the TV cartoon 'The Flintstones'?", "Dino")
        q11 = Question("What identity document is required to travel to different countries around the world?", "A passport")
        q12 = Question("Who is considered the 'Father of Relativity'?", "Albert Einstein")
        q13 = Question("Edie Falco and James Gandolfini star in what series about the life of a New Jersey mob boss?", "The Sopranos")
        q14 = Question("Nearly all fossils are preserved in what type of rock?", "Sedimentary")
        q15 = Question("What guitarist notably performed on the Michael Jackson song 'Beat It'?", "Eddie Van Halen")
        q16 = Question("What is August’s birthstone?", "Peridot")
        q17 = Question("What is Prince Harry’s official first name?", "Henry")
        q18 = Question("What is the fifth sign of the zodiac?", "Leo")
        q19 = Question("Which branch of the U.S. armed forces used the slogan 'It’s not just a job, it’s an adventure'?", "The Navy")
        q20 = Question("By U.S. law, exit signs must be one of what two colors?", "Green or red")
        q21 = Question("What is an eight-sided shape called?", "Octagon")
        q22 = Question("When was Earth Day first celebrated?", "1970")

        questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22]
        for question in questions:
            try: 
                question.create()
            except IntegrityError:
                db.session.remove()
                print("error")
                
                
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    score = db.Column(db.Integer, primary_key=False)
    rank = db.Column(db.Integer, primary_key=False)
    
    def __init__(self,uid,score=0):
        self.uid = uid
        self.score = score
        self.rank = None
    
    def getScore(self):
        return self.score
    
    def saveScore(self,score):
        try:
            self.score = score
            db.session.commit() 
            users = User.query.order_by(User.score.desc()).all()
            rank = 1
            for user in users:
                user.rank = rank
                rank+=1
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    def create(self):
        try:
            db.session.add(self) 
            db.session.commit() 
            users = User.query.order_by(User.score.desc()).all()
            rank = 1
            for user in users:
                user.rank = rank
                rank+=1
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
def initUsers():
    with app.app_context():
        db.create_all()
        u1 = User("User1")
        u2 = User("user2", score=12)
        u3 = User("User3")
        u4 = User("User4")
        u5 = User("User5")
        users = [u1,u2,u3,u4,u5]
        for user in users:
            try:
                user.create()
            except IntegrityError:
                db.session.remove()
                print("error")
                
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/trivia", methods=["GET"])
def trivia():
    if request.method == "GET":
        questions = Question.query.all()
        # print(len(questions))
        sample = []
        while len(sample) < 10:
            index = random.randrange(1,len(questions))
            if(questions[index] not in sample):
                sample.append(questions[index])
        response = {}
        index = 1
        for i in sample:
            response[str(index)] = i.read()
            index+=1
        return render_template("trivia.html",ques=response)

@app.route("/user", methods=['GET','POST'])
def user():
    if request.method == 'POST':
        data = request.json
        uid = data.get('uid')
        score = int(data.get('score'))
        usr = User.query.filter(User.uid == uid).first()
        if usr:
            if(usr.score < score):
                usr.saveScore(score);
        else:
            usr = User(uid,score)
            usr.create()
        return "upload success"
    elif request.method == 'GET':
        users = User.query.order_by(User.rank).all()
        print(users)
        users_list = []
        for user in users:
            user_data = {
                'uid': user.uid,
                'score': user.score,
                'rank': user.rank
            }
            users_list.append(user_data)
        return render_template("leaderboard.html", users_list=users_list)
        # render template later
        
def init_data():
    initUsers()
    initQuestions()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_data()
        app.run()