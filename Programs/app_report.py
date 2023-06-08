from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import bike_weather_app_report as bwa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    drive_mode = db.Column(db.String(10), nullable=False)
    avoid = db.Column(db.String(10), nullable=True)

@app.route('/result', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(desc(Post.id)).limit(1).all()
        for post in posts:
            departure_text, middle_texts, destination_text, save_name  = bwa.local_weather(post.departure, post.destination, post.time, post.drive_mode, post.avoid)
        print(departure_text)
        print(save_name)
        
        texts = {"departure_text" : departure_text, "middle_texts" : middle_texts, "destination_text" : destination_text }
        return render_template('result.html', posts=posts, texts=texts, save_name=save_name)
   
    else:
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        time = request.form.get('time')
        drive_mode = request.form.get('source')
        
        if drive_mode == "1":
            travel_mode = "driving"
        elif drive_mode == "2": 
            travel_mode = "walking"
        else:
            print("error")
            
        avoid_highway = request.form.get('highway')
        
        if travel_mode == "driving":
            #高速使うかの分岐
            # avoid_highway = input('高速を使いますか?: 1:使う 2:使わない').replace(' ','+')
            if avoid_highway == "1":
                avoid = None
            #高速道路を回避するので，2を選んだ場合にavoidに"highways"を代入する.
            elif avoid_highway == None: 
                avoid = "highways"
            else:
                print("error")
        else:
            avoid = None
        
        time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        new_post = Post(departure=departure, destination=destination, time=time, drive_mode=travel_mode, avoid=avoid)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect('/result')

@app.route('/')
def create():
    return render_template('create.html')


if __name__=='__main__':
    app.run(debug=True)