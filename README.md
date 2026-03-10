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
- When installing the `requirements.txt` file, it is also important to note you may need a different version of `pytorch`. By default, the `requirements.txt` will install `pytorch` for `Windows` and `CUDA 13.0+`. The version of `pytorch` you need to use can be figured out at [PyTorch](https://pytorch.org/get-started/locally/). You can check your CUDA version with `nvidia-smi`.

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

This is example output of when the script is ran.
