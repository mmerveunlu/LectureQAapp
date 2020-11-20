import json
import sys
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/')
from os.path import join
import webvtt

import statics

def generate_json(ppath,question,path):
    """ from given passage and question generates json format
    acceptable by QA models 

    Args: 
      @ppath: string, the path of the subtitle file
      @question: string, the question asked by user
      @path: string, where to save the json  
    Return:
      None
    """
    # finds the related passage from statics
    # get the content as text 
    vtt = webvtt.read(join(statics.PREVPATH,ppath)) 
    lines = []
    for line in vtt: 
        lines.extend(line.text.strip().splitlines())
    # join lines by empty space to form a passage    
    passage = " ".join(lines)

    # form json-type dict for the input
    data = {"version":"1.0"}
    with open(path,"a+") as fp:
        qa = {"question":question, "answers"=[]}
        p = {"context":passage, "qas"=[qa]}
        article = {"title":lecture,"passages":[p]}
        data['data'] = [article]
        json.dump(data,fp)

def get_predicted_answer(path):
    """reads and returns predicted answer from given path """
    
    return 
    


        
def run_model(passage,question):
    """runs the model and returns predicted answers """
    # first generate json for 1-sample
    # use datetime to name the input file
    dt = datetime.now().strftime("%Y%m%d_%H%M_%S")
    # where to save the passage+question pair
    path = join(statics.SERVERDPATH,"data-"+dt+".json")
    generate_json(passage,question,path)

    # run the model to get the prediction
    
    return
            


        
