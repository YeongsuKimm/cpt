from flask import Flask, render_template, request, make_response, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random

app = Flask(__name__) # initiates flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3' # sets up route for SQL database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)


"""
Question class functionality:
- Constructor: Instantiate a question (takes in the question and its corresponding answer as parameters)
- create() method: adds a Question instance object to the database
- read() method: returns a dictionary with key-value pairs for 'question' and 'answer' for a certain question instance
"""
class Question(db.Model): # a Question class which represents a question 
    id = db.Column(db.Integer, primary_key=True) # defines the id column variable for the database
    question = db.Column(db.String(255), unique=True, nullable=False) # defines the actual question variable in the database
    answer = db.Column(db.String(255), unique=False, nullable=False) # defines the answer column in the database
    
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
    
    
"""
initQuestions() functionality:
- this function initiates several quiz questions into the database
- It defines 22 sample questions and then uses iteration to insert each question into the database
"""
def initQuestions(): 
    with app.app_context():
        db.create_all()
        # Questions pulled from Today.com at https://www.today.com/life/inspiration/trivia-questions-rcna39101
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
                
                
"""
User Class Functionality:
Constructor: Creates a User instance object with the parameters: 'uid' and 'score' (default set to 0)
getScore(): gets the user's score for a particular user
saveScore(): saves a new score for the user; this method also handles reassigning the rank for all the users 
create(): adds a User instance object to the database
"""
class User(db.Model): # database used to store data to be accessed and updated 
    id = db.Column(db.Integer, primary_key=True) # represents the id column of the User database table
    uid = db.Column(db.String(255), unique=True, nullable=False) # the uid variable column in the database; user id
    score = db.Column(db.Integer, primary_key=False) # the score variable column in the database; personal best score from the quiz
    rank = db.Column(db.Integer, primary_key=False) # the rank variable column in the database; unique and is assigned based on score 
    
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
            users = User.query.order_by(User.score.desc()).all() # gets all the users from the database based on descending score value
            rank = 1
            for user in users:
                user.rank = rank # reassigns the ranks starting from 1
                rank+=1
            db.session.commit() # commits changes to database
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
    
"""
initUsers() functionality:
- this function initiates several users into the database
- It defines 5 users with different scores 
"""
def initUsers():
    with app.app_context():
        db.create_all()
        u1 = User("Bear")
        u2 = User("Camel", score=1)
        u3 = User("Donkey", score=4)
        u4 = User("Rabbit", score=7)
        u5 = User("Dog", score=4)
        users = [u1,u2,u3,u4,u5]
        for user in users:
            try:
                user.create()
            except IntegrityError:
                db.session.remove()
                print("error")


"""
API that handles a request to the default index url, renders the 'index.html' template
"""
@app.route("/")
def home():
    return render_template("index.html")

"""
API that handles a GET request. 
- Iterates through the questions in the database and picks 10 random questions and inserts into 'response' dictionary 
- Returns the 'response' dictionary with the random sample questions for the quiz
"""
@app.route("/quiz", methods=["GET"])
def quiz():
    if request.method == "GET":
        questions = Question.query.all()
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
        return render_template("quiz.html",ques=response)

"""
API that handles a GET and POST request. 
- If GET request:
    - Simply renders the 'upload.html' file to provide the user an interface to upload questions
- If POST request:
    - Receives  the JSON data that contains the elements 'question' and 'answer'
    - Checks if the question is already in the database
    - Else creates a new Question instance and uploads that to the database 
    - If question instance is created, it renders the 'questions.html' file to display all the questions
"""
@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        data = request.json
        ques = str(data.get('question'))
        answer = str(data.get('answer'))
        questions = Question.query.all()
        for question in questions:
            if(question.read()["question"] == ques):
                return False
        quesObject = Question(ques, answer)
        quesObject.create()
        response = []
        for question in questions:
            response.append(question.read())
        return render_template("questions.html", questions_list=response)

        

"""
API that handles a GET and POST request
- If POST request: 
    - Handle the json data from the frontend and creates a new User instance and inserts into the database
    - Creates a dictionary for all the users from the database and appends each dictionary to a list
    - After upload success, it renders the 'leaderboard.html' with an updated version of the leaderboard with the list
- If GET request:
    - Creates a dictionary for all the users from the database and appends each dictionary to a list
    - Renders 'leaderboard.html' with the list as context
"""
@app.route("/user", methods=['GET','POST'])
def user():
    if request.method == 'POST': # selection 
        data = request.json # sequencing (to unpack the data received into variables)
        uid = data.get('uid') # sequencing
        score = int(data.get('score')) # sequencing
        usr = User.query.filter(User.uid == uid).first() # sequencing
        if usr: # selection (if the user exists in the database already)
            if(usr.score < score): # selection
                usr.saveScore(score);
        else: # selection (else create new instance and upload to db)
            usr = User(uid,score) 
            usr.create()
        users = User.query.order_by(User.rank).all()
        users_list = [] # utilization of lists to organize data 
        for user in users: # iteration (gets all the users from the db and organizes each into a dictionary to be added to a list)
            user_data = {
                'uid': user.uid,
                'score': user.score,
                'rank': user.rank
            }
            users_list.append(user_data)
        return render_template("leaderboard.html", users_list=users_list) # returns the updated list of users and their scores
    elif request.method == 'GET': # selection
        users = User.query.order_by(User.rank).all()
        users_list = []
        for user in users:
            user_data = {
                'uid': user.uid,
                'score': user.score,
                'rank': user.rank
            }
            users_list.append(user_data)
        return render_template("leaderboard.html", users_list=users_list)
        
""" 
API that handles a GET request
- If GET request:
    - Collects all the questions from the database and organizes it into a list of dictionaries
    - Each dictionary has a key-value pair of a question and its answer
    - Renders the 'questions.html' template with the context being the list of all questions
    - Frontend will use that context to display all the questions
"""
@app.route("/questions", methods=["GET"])
def question():
    if request.method == "GET":
        questions = Question.query.all()
        print(questions)
        response = []
        for question in questions:
            response.append(question.read())
        return render_template("questions.html", questions_list=response)


"""
Function to initialize all test data
"""
def init_data():
    initUsers()
    initQuestions()

if __name__ == '__main__': # if python file is run, initiate the data and keep the file running
    with app.app_context():
        db.create_all()
        init_data()
        app.run()