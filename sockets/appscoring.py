import torch
from sentence_transformers import util


def run_predict_on_scoring_model(sentences1,sentences2,pretrained):
    """
    Uses a loaded model
    """
    return calculate_similarity(sentences1,sentences2,pretrained)
    

def calculate_similarity(sentences1,sentences2,pretrained):
    #Compute embedding for both lists
    embeddings1 = pretrained.model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = pretrained.model.encode(sentences2, convert_to_tensor=True)

    #Compute cosine-similarits
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)

    #Output the pairs with their score
    #for i in range(len(answers)):
    #    print("CORRECT: {} \n ANSWER: {} \n CosineScore: {:.4f} \t Score: {}".format(sentences1[0], sentences2[i], cosine_scores[0][i],scores[i]))

    return cosine_scores

                                        

