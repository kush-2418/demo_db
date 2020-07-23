#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:19:42 2020

@author: kush
"""
import urllib
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLEARDB_DATABASE_URL')


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'






# intitalize database
db = SQLAlchemy(app)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False)
    date= db.Column(db.DateTime, default=datetime.utcnow())
    
# Create function to return string when we add something
    def __repr__(self):
        return '<Name %>' %self.id    
   

 
subscribers = []
@app.route('/friends',methods=['POST','GET'])
def friends():
    title = "My Friend List"
    if request.method == "POST":
        friend_name = request.form.get('name')
        new_friend  = Friends(name=friend_name)
        # push to database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was in error adding in database"
    else:
        friends = Friends.query.order_by(Friends.date)
        return render_template("friends.html", title=title,friends=friends)

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "Update not done"
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

@app.route('/delete/<int:id>',methods=['POST','GET'])
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "Deletion not done"

@app.route('/')
def index():
    #return ("hello world")
    #title = "Kush Shrivastava Blog"
    return render_template("index.html")

@app.route('/about.html') # it can be about also with out .html if we are using url tag
def about():
    #title = "About Kush Shrivastava"
    names = ['Pranav','Shubham',"Prerana"]
    return render_template("about.html",names=names)

@app.route('/subscribe')
def subscribe():
    title = "Subscribe to my Email"
    return render_template("subscribe.html",title=title)

@app.route('/signup', methods=['POST'])
def signup():
    first_nm= request.form.get("first_name")
    last_nm =  request.form.get("last_name")
    email_add = request.form.get("email")
    message = "You have been subscribed to my email news letter "
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("kush.shri05@gmail.com", "iamgroot@7070")
    server.sendmail("kush.shri05@gmail.com",email_add, message)
    
    if not first_nm or not request.form.get("last_name") or not email_add:
        error_statement = " All Form Field Required..."
        return render_template("subscribe.html",error_statement=error_statement,first_name=first_nm,last_name=last_nm,email=email_add, subscribers=subscribers)
    subscribers.append(f"{first_nm} {last_nm} | {email_add}")
    title = "Thank You for Sign Up"
    return render_template("signup.html",title=title,first_name=first_nm,last_name=last_nm,email=email_add, subscribers=subscribers)

if __name__ == '__main__':
    app.run()
