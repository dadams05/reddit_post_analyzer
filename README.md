# reddit_post_analyzer

This is a simple Python script that will analyze a Reddit post using Ollama.
- Analyzes the text of the post
- Analyzes any pictures attached in the post
- Analyzes all comments on the post
- Uses Reddit's official API via `PRAW`
- Filters out comments with blacklisted words

## Requirements

- Developed and tested with `Python 3.14.2`. Earlier versions may not be compatible.
- A Reddit API key is required:
  1. Create a Reddit developer application
  2. Select "script" as the application type
  3. Copy your `CLIENT ID` and `CLIENT SECRET`
  4. More info: https://www.reddit.com/r/reddit.com/wiki/api/
- [Ollama](https://ollama.com/) will need to be installed and running. This script uses the following models, so unless you change it to use others, you must also download these models:
   - `llama3:8b` for overall analysis
   - `qwen3-vl:4b` for image analysis
- When installing the `requirements.txt` file, it is also important to note you may need a different version of `pytorch`. By default, the `requirements.txt` will install `pytorch` for `Windows` and `CUDA 13.0+`. The version of `pytorch` you need to use can be figured out at [PyTorch](https://pytorch.org/get-started/locally/). You can check your CUDA version with `nvidia-smi` in a terminal.

## Usage

1. Clone this project: `git clone https://github.com/dadams05/reddit_comment_scraper.git`
2. Create a virtual environment: `py -m venv <name>`
3. Activate the virtual environemnt:
   - Windows: `.\<name>\Scripts\activate`
   - Linux: `source <name>/bin/activate`
4. Install the `requirements.txt` file (make sure your venv is activated). Remember you may need a different version
of `pytorch` depending on your setup: `pip install -r requirements.txt`
5. Create a `.env` file and put your API keys in it. Check the example file called `.env.example`.
6. Run `main.py` while in your virtual environment. It will analyzed the Reddit post linked at `REDDIT_LINK` and output the results into a `.json` file.

## Before Committing

1. Run `pip freeze > requirements.txt` if any additional dependencies were installed.
2. Run `pylint <space separated filenames>` on any Python files changed.
3. Run `black <space separated filenames>` on any Python files changed.

## Example Run

This is example console output of when the script is ran.

```bash
(.venv) py .\main.py
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 201/201 [00:00<00:00, 57044.12it/s]
RobertaForSequenceClassification LOAD REPORT from: cardiffnlp/twitter-roberta-base-sentiment-latest
Key                             | Status     |  | 
--------------------------------+------------+--+-
roberta.embeddings.position_ids | UNEXPECTED |  | 
roberta.pooler.dense.bias       | UNEXPECTED |  | 
roberta.pooler.dense.weight     | UNEXPECTED |  | 

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.
>> Starting
>> Setting up directories. Output will be saved in "out\1rpg0mb"
>> Getting initial post data
>> Gallery post: downloading images
https://preview.redd.it/9lfh63kvp3og1.jpg?width=1080&format=pjpg&auto=webp&s=81b5597d296c99e09caa485e139768ee9b17750c downloaded successfully to out\1rpg0mb\0.jpg
https://preview.redd.it/w760zomvp3og1.jpg?width=1080&format=pjpg&auto=webp&s=8da42a3f05e41fa18ad47d14eed0c5c9b5035bb9 downloaded successfully to out\1rpg0mb\1.jpg
https://preview.redd.it/loswuxovp3og1.jpg?width=1080&format=pjpg&auto=webp&s=ce53a4bb57b961db05c08169209cf58ea538abc2 downloaded successfully to out\1rpg0mb\2.jpg
https://preview.redd.it/a3i99mqvp3og1.jpg?width=1080&format=pjpg&auto=webp&s=771e0ae09cdbfa58663e2d09875ee5d69ae41816 downloaded successfully to out\1rpg0mb\3.jpg
https://preview.redd.it/zt36c4tvp3og1.jpg?width=1080&format=pjpg&auto=webp&s=69b1701c223664fa3fb5854b39d65fc1d25da7a7 downloaded successfully to out\1rpg0mb\4.jpg
https://preview.redd.it/dkw6u2vvp3og1.jpg?width=1080&format=pjpg&auto=webp&s=fe1e7c8f0d113ee497831d1a3c1587676100823d downloaded successfully to out\1rpg0mb\5.jpg
https://preview.redd.it/gib6adxvp3og1.jpg?width=1080&format=pjpg&auto=webp&s=280dedda44c3fe13c51b7a579ebd87ec3a1e3e97 downloaded successfully to out\1rpg0mb\6.jpg
>> Analyzing images
>> Injecting image analysis back into post text
>> Downloading and filtering comments
>> Analyzing comment sentiment
You seem to be using the pipelines sequentially on GPU. In order to maximize efficiency please use a dataset
>> Analyzing post and comments
>> Saving data out to "out\1rpg0mb\analysis_2026-03-11_01-07-25.json"
```

This is an example of the `.json` file that is outputted.

```json
{
    "title": "Welp. Back to square one.",
    "created": "2026-03-09 18:08:50",
    "selftext": "I think I'm done. Between me and my wife's account, overall loss several years of income playing options. At one point I was up nearly +$100k on my personal account. That was mostly with SPY, Nvda, and Tsla.  Then I started to bleed.  And tried to win the losses back. And then doubled down. And then tripled down. Sometime along the way, my account got permanently closed by RH (Can't even view my chart on that account anymore). Started playing on wife's after that.\n\nOriginally found out about options thanks to some news article mentioning this Sub and someone making tons on options. \nIn 2022 I sold 407 shares of Nvidia. That was before the 10-1 split. That's worth ~$750k now. Instead ... I'm now deep in the negative.\n\nHad some good plays, pretty spikes, went down to $200 within a week $200 -> $28k, only to lose $27k the next day. Did a juicy SPY 0dte play last week, and then blew entire account next day on the 5th with yolo on spy calls, and then it tanked. Took 15 mins to wipe out the account. Got a little desperate and a little extra dumb.\n\nGot a decent job now, working 70-80hr weeks for OT. Opened a Webull (RH is too tempting to play options cuz that green/red gives a dopamine rush or something). Now I'll just be throwing a few grand a month on a SPY/Nvidia ect, and just let it do its thing. Some day/decade, I'll get that $160k+ back via slow growth I guess. It's been a fun run. Got addicted. Going full broke fixed that addiction I think. Time to give up on that \"get rich quick\" dream. Got ~$90k debt to pay off and be debt free finally.\n\nSeeing SPY today shoot up and watching a $0.04 0dte go  to $5.68 this morning made me sick..... After I blew the entire account just last week making that same dumb bet.... Woulda recovered all my losses and some today had I waited.\n\nPics 5-6 is the 0dte today that makes me wanna kick myself. 4 was last week's play. 3 is the shares I had once upon a time. 2 is original account closed. 1 is me today.\n\nLast pic is my original accounts 2022 statement.  Adding my loss writeoffs + wife's overall = ~$160k loss.  Now sure on how the wash sale number gets added up so didn't count that towards by ~$160k loss. I don't want to know my actual total loss.\n* * * * * *\nSlow and steady now. Back to collecting shares.\nEnjoy the photo dumps.\nJust thinking about this again makes me feel depressed. At 28yo, honestly thought I'd be further in life.",
    "id": "1rpg0mb",
    "score": 1688,
    "url": "https://www.reddit.com/gallery/1rpg0mb",
    "permalink": "/r/wallstreetbets/comments/1rpg0mb/welp_back_to_square_one/",
    "num_comments": 470,
    "filtered_num_comments": 322,
    "pos_count": 51,
    "neg_count": 165,
    "neu_count": 106,
    "comments": [
        {
            "id": "o9kszlc",
            "created": "2026-03-09 18:25:25",
            "score": 1616,
            "body": "> Going full broke fixed that addiction I think. > Woulda recovered all my losses and some today had I waited Hate to be the one to tell you… you’re still addicted. You’re just a broke addict now.",
            "sentiment": {
                "label": "negative",
                "score": 0.7321282029151917
            }
        },
        {
            "id": "o9ku6p5",
            "created": "2026-03-09 18:32:13",
            "score": 253,
            "body": "Lmfao you lost so badly that RH didn’t even let you respawn",
            "sentiment": {
                "label": "negative",
                "score": 0.9102975726127625
            }
        },
        {
            "id": "o9kst3q",
            "created": "2026-03-09 18:24:24",
            "score": 443,
            "body": "You belong to the hall of fame. Sold Nvidia before the AI run-up and proceed to lose it all lol.",
            "sentiment": {
                "label": "neutral",
                "score": 0.43785223364830017
            }
        }
    ],
    "prompt": "\nYou will be given a social media post from Reddit and comments made on it.\nIf there were pictures in the post, they have been analyzed and their summaries have been injected into the text at which they were inserted.\nIf the post had pictures attached, they have been analyzed and their summaries have been appended to the end of the text.\nBe objective and summarize the entire post and then summarize the comments.\nGive a paragraph summary and list the key points as bullets for both the post and the comments.\nBe professional, technical, in-depth, precise, and accurate.\nAdditionally, give your own analysis of the post.\n\nPost contents below:\nI think I'm done. Between me and my wife's account, overall loss several years of income playing options. At one point I was up nearly +$100k on my personal account. That was mostly with SPY, Nvda, and Tsla.  Then I started to bleed.  And tried to win the losses back. And then doubled down. And then tripled down. Sometime along the way, my account got permanently closed by RH (Can't even view my chart on that account anymore). Started playing on wife's after that.\n\nOriginally found out about options thanks to some news article mentioning this Sub and someone making tons on options. \nIn 2022 I sold 407 shares of Nvidia. That was before the 10-1 split. That's worth ~$750k now. Instead ... I'm now deep in the negative.\n\nHad some good plays, pretty spikes, went down to $200 within a week $200 -> $28k, only to lose $27k the next day. Did a juicy SPY 0dte play last week, and then blew entire account next day on the 5th with yolo on spy calls, and then it tanked. Took 15 mins to wipe out the account. Got a little desperate and a little extra dumb.\n\nGot a decent job now, working 70-80hr weeks for OT. Opened a Webull (RH is too tempting to play options cuz that green/red gives a dopamine rush or something). Now I'll just be throwing a few grand a month on a SPY/Nvidia ect, and just let it do its thing. Some day/decade, I'll get that $160k+ back via slow growth I guess. It's been a fun run. Got addicted. Going full broke fixed that addiction I think. Time to give up on that \"get rich quick\" dream. Got ~$90k debt to pay off and be debt free finally.\n\nSeeing SPY today shoot up and watching a $0.04 0dte go  to $5.68 this morning made me sick..... After I blew the entire account just last week making that same dumb bet.... Woulda recovered all my losses and some today had I waited.\n\nPics 5-6 is the 0dte today that makes me wanna kick myself. 4 was last week's play. 3 is the shares I had once upon a time. 2 is original account closed. 1 is me today.\n\nLast pic is my original accounts 2022 statement.  Adding my loss writeoffs + wife's overall = ~$160k loss.  Now sure on how the wash sale number gets added up so didn't count that towards by ~$160k loss. I don't want to know my actual total loss.\n* * * * * *\nSlow and steady now. Back to collecting shares.\nEnjoy the photo dumps.\nJust thinking about this again makes me feel depressed. At 28yo, honestly thought I'd be further in life.\n### Extracted Visible Text:  \n- **Top Bar**:  \n  - Time: `9:10`  \n  - Status icons: `4G`, `battery 81%`  \n- **Account Sections**:  \n  - `Investing`: `- $490.87` (with `▲ 0.00%` in green)  \n  - `Roth IRA`: `$15.08` (with `▲ 0.00%` in green)  \n  - `Credit Card`: `+` (plus icon, likely for adding a card)  \n- **Main Investment Summary**:  \n  - `- $490.87`  \n  - `▼ $79,777.60 Past year` (red downward arrow)  \n  - `Rewards Season` (green button)  \n- **Timeframe Selector**: `1W`, `1M`, `3M`, `YTD`, `1Y` (highlighted), `ALL`  \n- **Additional Labels**:  \n  - `Buying power`  \n  - `Account deficit` (with orange alert icon `⚠️`)  \n- **Futures Section**:  \n  - `Futures >`  \n  - `Your open futures positions will appear here.`  \n- **Bottom Navigation**:  \n  - Icons: Chart, Settings, Search, Profile  \n\n---\n\n### Summary of the Image:  \nThis is a **financial app screenshot** showing an **investing account with a deficit of $490.87** (marked with a red downward trend), while the **Roth IRA** shows a small balance of $15.08 (unchanged). A **significant loss of $79,777.60 over the past year** is highlighted. The app features a **graph depicting a downward trajectory in the investment account**, with timeframes for viewing the data (e.g., \"1Y\" is selected).  \n\nKey red flags include:  \n- An **\"Account deficit\" alert** (orange warning icon).  \n- A **\"Rewards Season\" promotion** (green button).  \n\nOther sections include *Credit Card* (for adding cards), *Buying power*, and a *Futures* section (currently empty). The interface suggests the user is managing investments and has experienced a notable decline in their primary investment account, likely due to market volatility.\n\n### Extracted Text:\n- **Status Bar**:  \n  - Time: `2:07`  \n  - Icons (e.g., notifications, connectivity)  \n  - Network: `5G`  \n  - Battery: `32%`  \n- **Main Message**:  \n  - `This account is closed`  \n  - `Your Robinhood account was permanently closed, and it can't be reopened.`  \n- **Button**: `Got it`  \n\n### Summary:  \nThe image shows a **Robinhood app notification** indicating a **permanently closed account**. The screen has a black background with green-themed illustrations of a futuristic cityscape (buildings, people, and structures). The key message states the account cannot be reopened, accompanied by a `Got it` button for acknowledgment. The status bar at the top includes time (`2:07`)...",
    "analysis": "This is a very long and detailed social media post from Reddit, with many comments made by users in response. The original poster (OP) is discussing their experiences with investing in the stock market, specifically with options trading. They claim to have lost $90,000 over several years, which they had invested in options trading.\n\nThe majority of the comments are concerned about the OP's behavior and how it may affect their relationship with their wife. Many users suggest that the OP is lying to their wife about the extent of their losses and that this could lead to serious problems in their marriage.\n\nSome common themes in the comments include:\n\n1. Addiction: Many users describe the OP's behavior as addictive, implying that they are unable to stop themselves from continuing to invest in options trading despite the negative consequences.\n2. Lack of self-awareness: Some commenters suggest that the OP is not taking responsibility for their actions and is instead blaming external factors (such as luck or market conditions) for their losses.\n3. Impact on relationships: Many users express concern about how the OP's behavior may affect their relationship with their wife, particularly if they are hiding the extent of their losses from her.\n4. Financial literacy: Some commenters suggest that the OP lacks a basic understanding of finance and investing, which has led them to make poor decisions.\n\nOverall, this social media post and its comments reflect a broader conversation about the risks and consequences associated with investing in options trading."
}
```

## Future Ideas

- Start up a local server on a port to give a web ui
- Display the `.json` results on a web page ui
- Add optional Dockerfile for Ollama instead of having to download it and all the models