"""
This program runs a flask server with an interface. 
To run the program: 
   >> python run_app.py 
Then: 
   http://127.0.0.1:5000 

It is tested on a development server. 

Contact: Merve Ünlü (m.merve.unlu@gmail.com)
 
"""

from flask import Flask, render_template, request
from utils import get_questions, save_asked_questions
import statics

import sys
sys.path.insert(1, '/sockets/')
from sockets.appclient import run_client

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    The function generates the manin page. 
    Gives a lecture video and the form. 
    """
    return render_template('index.html')



@app.route('/lecture', methods=['GET', 'POST'])
def form():
    """
    The function generates the main page. 
    Gives a lecture video and the form. 
    """
    # Init page will be lecture 1
    ylink = statics.lectures["lecture1"]["ylink"]
    subtitle = statics.lectures["lecture1"]["subtitle"]
    chkey = statics.lectures["lecture1"]["key"]
    questions = get_questions(chkey,statics.DATAPATH)
    return render_template('video-question-page.html', ylink=ylink, subtitle=subtitle, questions=questions)


@app.route('/question', methods=['GET', 'POST'])
def question():
    """
    The function generates the page after
    clicking to ask another question.
    """
    if not request.form.get('ylink'):
        # Init page will be lecture 1
        ylink = statics.lectures["lecture1"]["ylink"]
        subtitle = statics.lectures["lecture1"]["subtitle"]
        chkey = statics.lectures["lecture1"]["key"]

    else:
        ylink = request.form['ylink']
        subtitle = request.form['subtitle']
        # find the chapter key from dict
        for k,v in statics.lectures.items():
            if v['ylink'] == ylink:
                chkey = v["key"]
    questions = get_questions(chkey,statics.DATAPATH)        
    # if a lecture is selected render page
    for lecture in statics.lectures.keys():
        if request.form.get(lecture):
            ylink = statics.lectures[lecture]["ylink"]
            subtitle = statics.lectures[lecture]["subtitle"]
            # get the example questions for the lecture
            chkey = statics.lectures[lecture]["key"]
            questions = get_questions(chkey,statics.DATAPATH)
    return render_template('video-question-page.html', ylink=ylink, subtitle=subtitle, questions=questions)

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    """
    The function generates the page after a question is asked. 
    """
    ylink = request.form['ylink']
    subtitle = request.form['subtitle']
    # find the chapter key from dict
    for k,v in statics.lectures.items():
        if v['ylink'] == ylink:
            chapter = v["key"]

    # Run the client app to get the answer from the server
    # HOST, PORT comes from statics file
    response = run_client(statics.HOST,statics.PORT,subtitle,request.form['question'])
    # Check if returned response is None
    if not response:
        # TODO Error
        print("No response")
        answer_text = "--"
    else:
        answer_text = response
    
    # answer_text = "NLP people call a large pile of text a corpus"
    # save asked questions into a file
    save_asked_questions(chapter,
                         request.form['question'],
                         request.form['userName'],
                         request.form['studentID'],
                         statics.QPATH)
    
    return render_template('video-answer-page.html',
                           question=request.form['question'],
                           answer=answer_text,
                           ylink=ylink,
                           subtitle=subtitle)


if __name__ == "__main__":
    app.run()
