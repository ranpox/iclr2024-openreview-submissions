import json
import csv
import statistics

def process_line(line):
    data = json.loads(line)
    paper_id = None
    title = ""
    paper_ratings = []

    for note in data["notes"]:
        if "title" in note["content"]:
            title = note["content"]["title"]["value"]
            paper_id = note["id"]
        elif "rating" in note["content"]:
            rating = int(note["content"]["rating"]["value"].split(":")[0])
            paper_ratings.append(rating)

    if len(paper_ratings) > 1:
        avg_rating = sum(paper_ratings) / len(paper_ratings)
        std_dev = statistics.stdev(paper_ratings)
    elif len(paper_ratings) == 1:
        avg_rating = paper_ratings[0]
        std_dev = 0  # Standard deviation is 0 if there's only one rating
    else:
        avg_rating = None
        std_dev = None

    return paper_id, title, avg_rating, std_dev, paper_ratings

# Collecting data
papers_data = []
with open("raw_paper_reviews.jsonl", "r") as f:
    for line in f:
        paper_data = process_line(line)
        papers_data.append(paper_data)

# Sorting by average score (descending) and then by standard deviation (ascending)
papers_data.sort(key=lambda x: (x[2] is not None, x[2], -x[3] if x[3] is not None else None), reverse=True)

# Writing to CSV with index
with open("paper_reviews.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Index", "ID", "Title", "Average Score", "Standard Deviation", "Individual Scores"])

    for index, (paper_id, title, avg_rating, std_dev, paper_ratings) in enumerate(papers_data, start=1):
        csvwriter.writerow([index, paper_id, title, avg_rating, round(std_dev, 2) if std_dev is not None else None, "-".join(map(str, paper_ratings))])
