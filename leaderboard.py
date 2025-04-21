# 202411
import json

FILE = "leaderboard.json"


def load_scores():
    with open(FILE, "r") as f:
        scores = json.load(f)  # Read and load the JSON data from the file
    return scores


def save_scores(score):
    scores = load_scores()
    scores.append(score)
    with open(FILE, "w") as f:
        json.dump(scores, f, indent=4)


def get_sorted_scores():
    scores = load_scores()
    scores.sort(reverse=True)  # Sort scores in descending order
    return scores
