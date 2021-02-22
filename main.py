from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

import sys
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/sockets/')
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/')

from flask import Flask, render_template, request
from flask_login import login_required, current_user
from .utils import get_questions, save_asked_questions, find_answer_in_video_advance
from .statics import * 

from .sockets.appclient import run_client


@main.route('/')
def index():
    """
    The function generates the manin page.
    Gives a lecture video and the form.
    """
    return render_template('index.html')


@main.route('/list')
@login_required
def list():
    """
    The function generates the manin page.
    Gives a lecture video and the form.
    """
    return render_template('list.html',name=current_user.name)


@main.route('/video', methods=['GET', 'POST'])
@login_required
def question():
    """
    The function generates the page after
    clicking to ask another question.
    """
    if not request.form.get('ylink'):
        # if the page is accessed from list
        #  request.form will be empty
        video_id = request.url.split("=")[1]
        # Init page will be lecture 1
        ylink = lectures[video_id]["ylink"]
        subtitle = lectures[video_id]["subtitle"]
        chkey = lectures[video_id]["key"]
        title = lectures[video_id]["title"]

    else:
        # if the apge is accessed from send another question button
        # url. will be empty
        ylink = request.form['ylink']
        subtitle = request.form['subtitle']
        # find the chapter key from dict
        for k,v in lectures.items():
            # start is a substring added to the youtube links
            # to find the chkey, we need to remove &start= part
            # from the youtube links
            if "start" in ylink:
                ylink = ylink.split("start")[0][:-1]
            if v['ylink'] == ylink:
                chkey = v["key"]
                title = v["title"]
    questions = get_questions(chkey,DATAPATH)
    # if a lecture is selected render page
    for lecture in lectures.keys():
        if request.form.get(lecture):
            ylink = lectures[lecture]["ylink"]
            subtitle = lectures[lecture]["subtitle"]
            # get the example questions for the lecture
            chkey = lectures[lecture]["key"]
            title = lectures[lecture]["title"]
            questions = get_questions(chkey,DATAPATH)
            
    return render_template('video-question-page.html',
                           ylink=ylink,
                           subtitle=subtitle,
                           questions=questions,
                           title = title,
                           name=current_user.name)

@main.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():
    """
    The function generates the page after a question is asked. 
    """
    ylink = request.form['ylink']
    subtitle = request.form['subtitle']
    # find the chapter key from dict
    for k,v in lectures.items():
        if v['ylink'] == ylink:
            chapter = v["key"]
            title = v["title"]

    # Run the client app to get the answer from the server
    # HOST, PORT comes from statics file
    response = run_client(HOST,PORT,subtitle,request.form['question'])
    
    # TODO: Test response remove before git
    # response = "a continuous time system is a system where the input is a continuous time signal and this input results in an output"

    # Check if returned response is None    
    if not response:
        # TODO Error
        print("No response")
        answer_text = "--"
    else:
        answer_text = response
        start_second = find_answer_in_video_advance(subtitle,answer_text)
        ylink = ylink+"&start="+str(start_second)

    # save asked questions into a file
    save_asked_questions(chapter,
                         request.form['question'],
                         current_user.email,
                         answer_text,
                         QPATH)
    
    return render_template('video-answer-page.html',
                           question=request.form['question'],
                           answer=answer_text,
                           ylink=ylink,
                           subtitle=subtitle,
                           title=title,
                           name=current_user.name)
