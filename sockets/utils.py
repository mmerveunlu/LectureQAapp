import json
import sys
from os.path import join
import webvtt
from datetime import datetime
from appmodel import run_predict_on_model

PREVPATH = "../"
SERVERDPATH = "../../dataFromClient/"

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
    vtt = webvtt.read(join(PREVPATH,ppath)) 
    lines = []
    for line in vtt: 
        lines.extend(line.text.strip().splitlines())
    # join lines by empty space to form a passage    
    passage = " ".join(lines)

    # form json-type dict for the input
    data = {"version":"1.0"}

    qaid = ppath.split("/")[1].split(".")[0] + "_" + path.split("/")[1][4:]
    qa = {"question":question,"id":qaid, "answers":[]}
    p = {"context":passage, "qas":[qa]}
    article = {"title":ppath,"paragraphs":[p]}
    data['data'] = [article]
    # returns only data value of data dict
    return data['data']
    # TODO: save the jsons later
    # removed to test the speed #TODO add later
    #with open(path,"a+") as fp:
    #    json.dump(data,fp)

def get_predicted_answer(path):
    """reads and returns predicted answer from given path """
    with open(path) as fp:
        return list(json.load(fp).values())[0]
   
        
def run_model(passage,question):
    """runs the model and returns predicted answers """
    # first generate json for 1-sample
    # use datetime to name the input file
    dt = datetime.now().strftime("%Y%m%d_%H%M_%S")
    # where to save the passage+question pair
    path = join(SERVERDPATH,"data-"+dt+".json")
    data = generate_json(passage,question,path)
    # run the model to get the prediction

    predict_file = path.split("/")[-1]
    # TODO: change output dir
    data_dir = SERVERDPATH
    output_dir = "/work/merve/responses/"
    model_path = "/work/merve/merve-tezboun-qa/bert-model/experiments/bert-large-cased-whole-word-masking-finetuned-squad_batch4_epoch16_seq256-eng-exp1"
    run_predict_on_model(data_dir=data_dir,
                         model_path=model_path,
                         output_dir=output_dir,
                         predict_file=predict_file,
                         data=data)

    answer_path = join(output_dir,"predictions_"+predict_file)
    return get_predicted_answer(answer_path)

            


        
