import requests
from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db = SQLAlchemy(app)

class Post(db.Model):
    poll = db.Column(db.String(50), primary_key=True)
    option1 = db.Column(db.String(50),default='')
    option2 = db.Column(db.String(50),default='')
    option3 = db.Column(db.String(50),default='')
    option4 = db.Column(db.String(50),default='')
    c1 = db.Column(db.Integer,default=0)
    c2 = db.Column(db.Integer,default=0)
    c3 = db.Column(db.Integer,default=0)
    c4 = db.Column(db.Integer,default=0)


@app.route('/enter/<string:question>/<string:option>',methods=['GET'])
def fun(question,option):
     pollq = Post.query.get(question)
     
     if pollq.option1==option:
        pollq.c1 += 1
        db.session.commit()
        #return jsonify(pollq.c1)
     elif pollq.option2==option:
        pollq.c2 += 1
        db.session.commit()
        #return jsonify(pollq.c2)
     elif pollq.option3==option:
        pollq.c3 += 1
        db.session.commit()
        #return jsonify(pollq.c3)
     elif pollq.option4==option:
        pollq.c4 += 1
        db.session.commit()
        #return jsonify(pollq.c4)
        #return(pollq.c4)
     #db.session.commit()  

     stats = {
         'question':pollq.poll,
         'option1':pollq.option1,
         'option2':pollq.option2,
         'option3':pollq.option3,
         'option4':pollq.option4,
         'c1':pollq.c1,
         'c2':pollq.c2,
         'c3':pollq.c3,
         'c4':pollq.c4
     }


     return jsonify(stats)

@app.route('/enter', methods=['POST','GET'])
def index():
  
    if request.method == 'POST':
        new_poll = request.form.get('pollquestion')
        op1=request.form.get('option1')
        op2=request.form.get('option2')
        #op1=request.form.get('option1')
        if new_poll:
            #new_city_obj = City(name=new_city)
            if op1!='' and op2!='':
                new_poll_obj = Post(poll=new_poll,option1=op1,option2=op2)
                try :
                    db.session.add(new_poll_obj)
                    db.session.commit()
                except:
                    db.session.rollback()  
            #new_city_obj = City(name=new_city)
            #db.session.add(new_city_obj)
            #db.session.commit()
        
    cities = Post.query.all()

    
    weather_data = []

    for city in cities:

        

        weather = {
            'poll' : city.poll,
            'op1' : city.option1,
            'op2' : city.option2,
            'op3' : city.option3,
            'op4':city.option4,
            'c1':city.c1,
            'c2':city.c2,
            'c3':city.c3,
            'c4':city.c4
        }

        weather_data.append(weather)


    return render_template('myfe.html',weather_data=weather_data)
  





if __name__ == "__main__":
    app.run(host='0.0.0.0')



    