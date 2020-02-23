# Robo-advisor 
Hello Welcome to my robo-advisor program! In this program you will input a stock ticker(no longer than 6 characters) and it will output key stock metrics and give you a decision whether to buy, hold, or sell the selected stock.

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip

## Setup

### Repo-Setup
Use the GitHub.com online interface to create a new remote project repository called something like "robo-advisor". When prompted by the GitHub.com online interface, let's get in the habit of adding a "README.md" file and a Python-flavored ".gitignore" file (and also optionally a "LICENSE") during the repo creation process. After this process is complete, you should be able to view the repo on GitHub.com at an address like `https://github.com/YOUR_USERNAME/robo-advisor`.

After creating the remote repo, use GitHub Desktop software or the command-line to download or "clone" it onto your computer. Choose a familiar download location like the Desktop.

After cloning the repo, navigate there from the command-line:

```sh
cd ~/Desktop/robo-advisor
```
### Environment Setup
Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```
### Installation of Packages
From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

### API key setup

In the .env file located in Desktop/robo-advisor, insert your own API key like the example below

```sh
ALPHAVANTAGE_API_KEY="abc123"
```

## Running the program

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo_advisor.py
```
