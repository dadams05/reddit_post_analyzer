# pylint: disable=missing-module-docstring,line-too-long
import os
import re
import json
from datetime import datetime
import praw
import requests
import torch
from dotenv import load_dotenv
from ollama import chat
from transformers import pipeline


# API keys
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# globals
REDDIT_LINK = "https://www.reddit.com/r/wallstreetbets/comments/1rpg0mb/welp_back_to_square_one/"  # reddit post to analyze
OUT_DIRECTORY = "out"  # directory to output files
FILE_NAME = f"analysis_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"  # name of file to save to
NUM_COMMENTS_REPLACE = None  # depth of comment subtrees to replace; can be None
SUBREDDITS = [  # subreddits to scrape from
    "wallstreetbets",
    "smallstreetbets",
    "StockMarket",
    "Shortsqueeze",
    "investing",
    "Daytrading",
]
BLACKLIST = [  # comments containing these words/phrases will be filtered out
    "[deleted]",
    "[removed]",
    "I am a bot",
    "https://preview.redd.it/",
    "![gif](giphy",
    "**User Report**",
    "I will be messaging you in",
    "[**Join WSB Discord**]",
]
POST_ID_REGEX = r"/comments/([a-z0-9]+)"
VISION_MODEL = "qwen3-vl:4b"
ANALYZER_MODEL = "llama3:8b"
DEVICE = 0 if torch.cuda.is_available() else -1 # set script to use gpu or cpu based on configuration
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SENTIMENT_ANALYZER = pipeline(
    "sentiment-analysis",
    model=MODEL,
    tokenizer=MODEL,
    device=DEVICE,
    truncation=True,
    max_length=512,
)


def download_image(image_url, filename):
    """Simple function to download an image given a URL and the filename to save it to"""
    try:
        response = requests.get(image_url, timeout=60) # 1 minute timeout
        response.raise_for_status()
        with open(filename, "wb") as image_file:
            image_file.write(response.content)
        print(f"{image_url} downloaded successfully to {filename}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")


if __name__ == "__main__":
    # main objects
    print(">> Starting")
    submission_id = re.findall(POST_ID_REGEX, REDDIT_LINK)[0]  # extract the id out of the URL
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
    submission = reddit.submission(submission_id)

    # set up output directories
    print(f'>> Setting up directories. Output will be saved in "{os.path.join(OUT_DIRECTORY, submission_id)}"')
    os.makedirs(OUT_DIRECTORY, exist_ok=True)  # create the output directory
    os.makedirs(os.path.join(OUT_DIRECTORY, submission_id), exist_ok=True)  # create the subdirectory for the post

    # start storing data
    print(">> Getting initial post data")
    data = {}
    data["title"] = submission.title
    data["created"] = str(datetime.fromtimestamp(submission.created_utc))
    data["selftext"] = submission.selftext
    data["id"] = submission.id
    data["score"] = submission.score
    data["url"] = submission.url
    data["permalink"] = submission.permalink
    data["num_comments"] = submission.num_comments
    data["filtered_num_comments"] = 0
    data["pos_count"] = 0
    data["neg_count"] = 0
    data["neu_count"] = 0
    data["comments"] = []

    # download images in the post
    index = 0
    images = []
    if "gallery" in submission.url or hasattr(submission, "media_metadata"):
        print(">> Gallery post: downloading images")
        if hasattr(submission, "gallery_data") and hasattr(submission, "media_metadata"):
            for item in submission.gallery_data["items"]:
                media_id = item["media_id"]
                url = submission.media_metadata[media_id]["s"]["u"]
                images.append(
                    {
                        "index": index,
                        "url": url,
                        "path": os.path.join(OUT_DIRECTORY, submission_id, f"{str(index)}.jpg"),
                    }
                )
                index += 1
    elif not submission.is_self:
        print(">> Image post: downloading image")
        images.append(
            {
                "index": index,
                "url": submission.url,
                "path": os.path.join(OUT_DIRECTORY, submission_id, f"{str(index)}.jpg"),
            }
        )
    else:
        print(">> Text post: no images")
    for i in images:
        download_image(i["url"], i["path"])

    # analyze all downloaded images from the post
    print(">> Analyzing images")
    for i in images:
        ollama_response = chat(
            model=VISION_MODEL,  # use a vision-capable model
            messages=[
                {
                    "role": "user",
                    "content": "Extract all visible text and summarize what this image is showing.",
                    "images": [i["path"]],
                }
            ],
        )
        i["analysis"] = ollama_response["message"]["content"]

    # inject the analyzed images back into or onto the end
    print(">> Injecting image analysis back into post text")
    text = submission.selftext
    for i in images:
        if i["url"] in text:
            text = text.replace(i["url"], i["analysis"])
        else:
            text += f"\n{i["analysis"]}\n"

    # get all comments from the post and filter them
    print(">> Downloading and filtering comments")
    comment_count = 0
    submission.comments.replace_more(limit=NUM_COMMENTS_REPLACE)
    for comment in submission.comments.list():
        comment_data = {}
        if (
            comment.body
            and not len(comment.body.split()) <= 5  # get comments at least 5 words
            and not any(keyword in comment.body for keyword in BLACKLIST) # remove bot comments
        ):
            # store comment information
            comment_data["id"] = comment.id
            comment_data["created"] = str(datetime.fromtimestamp(comment.created_utc))
            comment_data["score"] = comment.score
            # clean up the comment before storing it
            comment_body = comment.body.replace("\n", " ")
            comment_body = " ".join(comment_body.split())
            comment_data["body"] = comment_body
            # store the comment
            data["comments"].append(comment_data)
            comment_count += 1
    data["filtered_num_comments"] = comment_count

    # analyze the filtered comments
    print(">> Analyzing comment sentiment")
    pos_count = 0
    neg_count = 0
    neu_count = 0
    for comment in data["comments"]:
        analysis = SENTIMENT_ANALYZER(comment["body"])
        comment["sentiment"] = analysis[0]
        if analysis[0]["label"] == "positive":
            pos_count += 1
        elif analysis[0]["label"] == "negative":
            neg_count += 1
        elif analysis[0]["label"] == "neutral":
            neu_count += 1
    data["pos_count"] = pos_count
    data["neg_count"] = neg_count
    data["neu_count"] = neu_count

    # analyze the post and its contents
    print(">> Analyzing post and comments")
    PROMPT = f"""
You will be given a social media post from Reddit and comments made on it.
If there were pictures in the post, they have been analyzed and their summaries have been injected into the text at which they were inserted.
If the post had pictures attached, they have been analyzed and their summaries have been appended to the end of the text.
Be objective and summarize the entire post and then summarize the comments.
Give a paragraph summary and list the key points as bullets for both the post and the comments.
Be professional, technical, in-depth, precise, and accurate.
Additionally, give your own analysis of the post.

Post contents below:
{text}

Comments on post:
{"\n".join(f"- {comment["body"]}" for comment in data["comments"])}
            """
    ollama_response = chat(model=ANALYZER_MODEL, messages=[{"role": "user", "content": f"{PROMPT}"}])

    # save the data
    print(f'>> Saving data out to "{os.path.join(OUT_DIRECTORY, submission_id, f"{FILE_NAME}.json")}"')
    data["prompt"] = PROMPT
    data["analysis"] = ollama_response["message"]["content"]
    with open(
        os.path.join(OUT_DIRECTORY, submission_id, f"{FILE_NAME}.json"),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
