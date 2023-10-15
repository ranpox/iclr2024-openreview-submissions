import requests
import json
from tqdm import tqdm

BASE_URL = "https://api2.openreview.net/notes?content.venueid=ICLR.cc%2F2024%2FConference%2FSubmission&details=replyCount%2Cinvitation%2Coriginal&domain=ICLR.cc%2F2024%2FConference"
LIMIT = 1000

HEADERS = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

def fetch_data(offset=0, limit=LIMIT):
    """Fetch data from OpenReview API."""
    url = f"{BASE_URL}&limit={limit}&offset={offset}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def fetch_all_papers():
    """Retrieve all papers from OpenReview."""
    initial_data = fetch_data()
    count = initial_data["count"]
    print(f"Total number of papers: {count}")
    
    all_papers = []
    for offset in tqdm(range(0, count, LIMIT)):
        data = fetch_data(offset)
        all_papers.extend(data["notes"])

    return all_papers, count

def save_to_file(papers, count):
    """Save paper data to a JSON file."""
    paperlist = {"notes": papers, "count": count}
    with open("paperlist.json", "w") as f:
        json.dump(paperlist, f, indent=4)

if __name__ == "__main__":
    papers, count = fetch_all_papers()
    save_to_file(papers, count)
