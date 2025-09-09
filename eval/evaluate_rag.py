# Example skeleton using ragas; requires a dataset of (question, ground truth) and a retriever callable.
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_precision, context_recall

def run_eval(dataset):
    # dataset: ragas DatasetDict-like with columns question, contexts, answer, ground_truth
    result = evaluate(dataset, metrics=[answer_relevancy, faithfulness, context_precision, context_recall])
    print(result)
