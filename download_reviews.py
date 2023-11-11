import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import json
from tqdm import tqdm

BASEURL = "https://api2.openreview.net/notes?details=replyCount%2Cwritable%2Csignatures%2Cinvitation%2Cpresentation&domain=ICLR.cc%2F2024%2FConference&forum="

def fetch_data(paper_id, session):
    url = BASEURL + paper_id
    response = session.get(url)
    return response.json()

if __name__ == "__main__":
    papers = pd.read_csv("paperlist.csv")    
    with open("raw_paper_reviews.jsonl", "w") as f, requests.Session() as session:
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(fetch_data, paper.id, session) for paper in papers.itertuples()]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(papers)):
                data = future.result()
                f.write(json.dumps(data) + "\n")