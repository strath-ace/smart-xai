# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# The main file used for scoring results for bertscore and cosine similarity
# ===========================================================================================================
from evaluate import load
from sentence_transformers import SentenceTransformer, util
import torch

device = torch.device('cuda')
def bert_score(candidate, references):
    bertscore = load("bertscore")

  
    results = bertscore.compute(predictions=candidate, references=references, model_type="microsoft/deberta-xlarge-mnli", num_layers=40, device=device)
    print(results["precision"])

    return results["precision"], results["recall"], results["f1"]


def cosine_score(question1, question2):
    #load model
    model  = SentenceTransformer("all-MiniLM-L6-v2", device=device)


    # Compute embedding for both lists
    embeddings1 = model.encode(question1, convert_to_tensor=True)
    embeddings2 = model.encode(question2, convert_to_tensor=True)

    # Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    # return cosine_scores
    # Output the pairs with their score
    for i in range(len(question1)):
        print("{} \t\t {} \t\t Score: {:.4f}".format(
            question1[i], question2[i], cosine_scores[i][i]
        ))
        a = "{:.4f}".format(cosine_scores[i][i])

        return a



if __name__ == "__main__":

    explanations_generated = [["Can the processing of images replace the downlinking of images at time 2251?"]]
    refs = ["What would happen if taking of images was scheduled instead of processing of images at time 7316?"]
    # scored_results = bert_score(explanations_generated[0], refs)
    question1 = ["Can the processing of images replace the downlinking of images at time 2251?"]
    question2 = [
    "How would the schedule be affected if the image downlink process were to be conducted in place of the image processing phase at the timestamp 14166?"]

    cosine_score = cosine_score(question1, question2)
    # precision, recall, f1 = bert_score(explanations_generated[0], refs)

    # print(scored_results, len(scored_results))
    # for i in range(0,len(scored_results)):
    #     if i == 0:
    #         column = "J"
    #         print(column, i, scored_results[i][0])
    #     elif i == 1:
    #         column = "K"
    #         print(column, i, scored_results[i][0])
    #     else:
    #         column = "L"
    #         print(column, i, scored_results[i][0])



