from flask import Blueprint
from . import db

import time

main = Blueprint('main', __name__)

import sys
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/sockets/')
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/')

from flask import Flask, render_template, request
from flask_login import login_required, current_user
from .utils import get_questions, save_asked_questions_answers, save_asked_questions, find_answer_in_video_advance
from .statics import * 

from .sockets.appclient import run_client

def get_parameters(video_id,chapter):
    """returns the values related to chapter and video number 
    check from the static.dict object
    """
    lectures = lecture_dict[chapter]
    return lectures[video_id]['ylink'],\
        lectures[video_id]['subtitle'],\
        lectures[video_id]['key'],\
        lectures[video_id]['title'],\
        lectures

def get_lectures(chapter):
    """returns the related lectures dict 
    
    """
    return lecture_dict[chapter]

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
    return render_template('list.html',name=current_user.name,video_dict=video_dict,counts=counts)


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
        # video_id = request.url.split("=")[1]
        video_id = request.args.get('video_id')
        chapter = request.args.get('chapter')
        if not video_id.startswith("video"):
            video_id = "video"+video_id
        ylink,subtitle,chkey,title,lectures = get_parameters(video_id,chapter)
    else:
        # if the page is accessed from send another question button
        # url. will be empty
        ylink = request.form['ylink']
        subtitle = request.form['subtitle']
        chapter = request.args.get('chapter')
        lectures = get_lectures(chapter)
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
                           name=current_user.name,
                           videos=lectures,
                           chkey=chapter)

@main.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():
    """
    The function generates the page after a question is asked. 
    """

    ylink = request.form['ylink']
    subtitle = request.form['subtitle']
    chapter = request.args.get('chapter')
    lectures = get_lectures(request.args.get('chapter'))
    # find the chapter key from dict
    for k,v in lectures.items():
        if v['ylink'] == ylink:
            chkey = v["key"]
            title = v["title"]
    # save asked questions by user name
    # save_asked_questions(chkey,
    #                     request.form['question'],
    #                     current_user.email,
    #                     STATFOLDER)

    # Run the client app to get the answer from the server
    # HOST, PORT comes from statics file
    # response = run_client(HOST,PORT,subtitle,request.form['question'])
    response = None
    try_nbr = 1
    while((not response) and (try_nbr<MAX_TRY_NBR)):
        print("Trying to ask the server try: ",try_nbr)
        response = run_client(HOST,PORT,subtitle,request.form['question'])
        try_nbr += 1
        time.sleep(3)

    # TODO: Test response remove before git
    # response = "a continuous time system is a system where the input is a continuous time signal and this input results in an output"

    # Check if returned response is None    
    if not response:
        # TODO Error
        print("No response from the server after %d calls " %(MAX_TRY_NBR))
        answer_text = "--"
    else:
        answer_text = response
        start_second = find_answer_in_video_advance(subtitle,answer_text)
        ylink = ylink+"&start="+str(start_second)

    # save asked questions into a file
    save_asked_questions_answers(chkey,
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
                           name=current_user.name,
                           chkey=chkey,
                           videos=lectures,
                           chapter=chapter)
