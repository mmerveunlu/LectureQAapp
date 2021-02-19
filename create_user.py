#!/usr/bin/env python

""" 
In the interpreter: 
 >> from LectureQAInterface import db, app
 >> from LectureQAInterface.models import User
 >> from LectureQAInterface.create_user import generate_password, 
 >> from werkzeug.security import generate_password_hash
 >> with app.app_context(): 
        db.init_app(app) 
        password = generate_password(12) 
        new_user = User(email="deneme@hotmail.com",name="deneme deneme",password=generate_password_hash(password,method="sha256")) 
        db.session.add(new_user) 
        db.session.commit()
""" 
""" creates users """
from . import db, app
from .models import User
from werkzeug.security import generate_password_hash
import argparse

import random


def generate_password(length):
    """creates a random password for a given length """
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*().,?0123456789'
    password = ''
    for c in range(length):
        password += random.choice(chars)
    return password

def remove_user(email):
    """ removes given user by email """
    with app.app_context():
        db.init_app(app)

        new_user = User.query.filter_by(email=email).first()
        db.session.delete(new_user)
        db.session.commit()
    
def add_user(email,name,length):
    """ adds the user with email and name"""
    # connect db and app
    with app.app_context():
        db.init_app(app)

        password = generate_password(length)
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    print("User %s added" %(email))
    return password

def add_mult_users(infile,outfile,length):
    """creates multiple user from input file, writes to output file """
    # open input file to read names
    with open(infile) as fp:
        lines = fp.readlines()
    with open(outfile,"w+") as fp:
        for line in lines:
            name = line.split(",")[0]
            email = line.split(",")[1].replace("\n","")
            password=add_user(email,name,length)
            fp.write(",".join([name,email,password]))
    print("All users added and saved into %s ",outfile)        

def main():
    
    parser = argparse.ArgumentParser(description='Creating new users')
    parser.add_argument('--length', type=int, nargs='l',
                    help='the length of the password')
    parser.add_argument('--number',type=int,nargs='n',
                    help='number of users to be added')
    parser.add_argument('--output',type=string,nargs='o',
                    help='filepath where to store the users')
    parser.add_argument('--input',type=string,nargs='i',
                    help="filepath where the users information")
    
    args = parser.parse_args()




    
