
#import libraries
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cosine_score(question1, question2):
    #load model
    model  = SentenceTransformer("all-MiniLM-L6-v2")


    # Compute embedding for both lists
    embeddings1 = model.encode(question1, convert_to_tensor=True)
    embeddings2 = model.encode(question2, convert_to_tensor=True)


    # Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    # Output the pairs with their score
    for i in range(len(question1)):
        print("{} \t\t {} \t\t Score: {:.4f}".format(
            question1[i], question2[i], cosine_scores[i][i]
        ))
        a = " {:.4f}".format(cosine_scores[i][i])

        return a


if __name__ == "__main__":
    question1 = ["Can the processing of images replace the downlinking of images at time 2251?"]
    question2= ["How would the schedule be affected if the image downlink process were to be conducted in place of the image processing phase at the timestamp 14166?"]



    score= cosine_score(question1, question2)
    print(score)
