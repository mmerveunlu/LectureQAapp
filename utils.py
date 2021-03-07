import json
from datetime import datetime
from .statics import * 
import webvtt
from os.path import join
import string

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
    for caption in webvtt.read(join(SPATH,subtitle)):
        if answer[:len(answer)//2] in caption.text:
            return caption.start_in_seconds

def find_answer_in_video_advance(subtitle,answer):
    """ 
    returns the seconds where the answer starts in the video, 
    first concatenate subtitle text and searches the answer 
    more advance than find_answer_in_video
    Args: 
        subtitle: string, path of the subtitle file 
        answer: string, the predicted answer
    Returns: 
        ; float, seconds where the answer starts
    """
    caption_text = ""
    # concatenate the subtitle
    for caption in webvtt.read(join(SPATH,subtitle)):
        caption_text += caption.text + " "
    ans_start = caption_text.find(answer)
    char_nbr = 0
    # looks for the character number
    # which shows the first character of the answer text
    for caption in webvtt.read(join(SPATH,subtitle)): 
        char_nbr += len(caption.text) + 1  
        if char_nbr > ans_start:
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
    if chapter_name in data.keys():
        return data[chapter_name]
    else:
        return []

def save_asked_questions_answers(chapter,question,userEmail,response,qpath):
    """
    saves asked questions with answers into a file 
    Args:
      chapter: string, the key of the chapter
      question: string, the question text asked by user
      userEmail: string, the email of the user
      reponse: string, the answer from the server
      qpath: string, the path of the question file
    """
    with open(qpath,"a+") as fp:
        line = SEP.join([datetime.now().strftime(format="%d:%m:%Y-%H:%M:%S"),
                         chapter,question,response,userEmail,"\n"])
        fp.write(line)

def save_asked_questions(chapter,question,userEmail,qpath):
    """
    saves asked questions into a file 
    Args:
      chapter: string, the key of the chapter
      question: string, the question text asked by user
      username: string, the name and surname of the user 
      userID: string, the student id of the user 
      qpath: string, the path of the question folder
    """
    # get the user name

    # remove punctuations
    table = str.maketrans(dict.fromkeys(string.punctuation))
    no_punctuation= userEmail.split("@")[0].translate(table)
    file_user = join(qpath,no_punctuation+".txt")
    
    with open(file_user,"a+") as fp:
        line = SEP.join([datetime.now().strftime(format="%d:%m:%Y-%H:%M:%S"),
                         chapter,question,"\n"])
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
    chapter_dict = {key:[] for key in chapter_keys}
    for a in data: 
        for p in a['paragraphs']: 
            for qa in p['qas']: 
                chapter_dict[qa['id'][1:8]].append(qa['question']) 
    with open("example-questions.json","w") as fp:
        json.dump(chapter_dict,fp,indent=4,sort_keys=True)
    


def process_example_questions(file_path):
    """for a given path, read the questions 
    adds punctuations and capitalize 
    saves the dict to the same file 
    """
    with open(file_path) as fp:
        data = json.load(fp)
    # question words    
    q_words = ['how','what','when','which','why']
    # question verbs 
    q_tuple = ('can','are','is','do','does') 
    new_data = dict() 
    for key,value in data.items(): 
        new_data[key] = [] 
        for q in value: 
            if any(x in q for x in q_words): 
                q = q+ "?"
                new_data[key].append(q.capitalize())
            elif q.startswith(q_tuple):
                q = q+ "?"
                new_data[key].append(q.capitalize())
            else:
                q = q + "."
                new_data[key].append(q.capitalize())
                
    with open("example-questions.json","w") as fp: 
        json.dump(new_data,fp)
