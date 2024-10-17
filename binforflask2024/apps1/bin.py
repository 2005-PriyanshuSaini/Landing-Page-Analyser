from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy #this is usd to maintain a database from flask
from datetime import datetime
import pandas as pd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #if you are using mysql then you can make one with it too but this is easy to use and maintain
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# this is just a data base for the sql which is used here for the data storage
class data(db.Model):
    Sr = db.Column(db.Integer, primary_key=True)
    exampleInputEmail1 = db.Column(db.String(200), nullable=False)
    exampleInputName1 = db.Column(db.String(200), nullable=False)
    exampleInputUrl1 = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self) -> str:
    return f"{self.Sr} - {self.exampleInputEmail1} - {self.exampleInputName1} - {self.exampleInputUrl1}"

#to run this we need to import 'python' cmd in terminal adn then 'from app import db'
#then 'db.create_all()' to create a file for db
#now we just exit by 'exit()'  this was just to create a db and to view it we just drag and drop the file into sqlite viewer


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='post':
        print("post")
    Data = data(exampleInputEmail1="priyanshusaini9991@gmail.com", exampleInputName1="Arka Consultancy", exampleInputUrl1="www.google.com")
    db.session.add(data)
    db.session.commit
    allData = data.query.all()
    # print(allData)
    return render_template('index.html', allData=allData)
    # return 'Hello, World! from flask'

@app.route('/show')
def products():
    allData = data.query.all()
    print(allData)
    return 'products from flask'

if __name__ == '__main__':
    app.run(debug=True)
