import json
from datetime import datetime
import statics
import webvtt
from os.path import join

def find_answer_in_video(subtitle,answer):
    """ 
    returns the seconds where the answer starts in the video 
    searchs it in the subtitle
    Args: 
        subtitle: string, path of the subtitle file 
        answer: string, the predicted answer
    Returns: 
        ; float, seconds where the answer starts
    """
    # only checks where the start of the answer occurs
    for caption in webvtt.read(join(statics.SPATH,subtitle)):
        if answer[:len(answer)//2] in caption.text:
            return caption.start_in_seconds


def get_questions(chapter_name, qpath):
    """ 
    returns previously asked questions for a given chapter
    Args:
     chapter_name: string, the key of the chapter name
      ex: ch01_0_0
     qpath: string, the path of the data file, contains questions 
            for each chapter 
    Returns: 
     list of string, questions text
    """
    with open(qpath) as fp:
        data = json.load(fp)
    return data[chapter_name]

def save_asked_questions(chapter,question,username,userID,qpath):
    """
    saves asked questions into a file 
    Args:
      chapter: string, the key of the chapter
      question: string, the question text asked by user
      username: string, the name and surname of the user 
      userID: string, the student id of the user 
      qpath: string, the path of the question file
    """
    with open(qpath,"a+") as fp:
        line = statics.SEP.join([datetime.now().strftime(format="%d:%m:%Y-%H:%M:%S"),
                        question,username,userID,"\n"])
        fp.write(line)

def save_questions(datapath):
    """save the example questions into a file
    Args: 
      datapath: string, the path of the json file
    Returns: 
      None,
    """
    # open json file
    with open(datapath) as fp:
        data = json.load(fp)['data']
    # for each chapter key find questions
    chapter_dict = {key:[] for key in statics.chapter_keys}
    for a in data: 
        for p in a['paragraphs']: 
            for qa in p['qas']: 
                chapter_dict[qa['id'][1:8]].append(qa['question']) 
    with open("example-questions.json","w") as fp:
        json.dump(chapter_dict,fp,indent=4,sort_keys=True)
    


