# -*- coding: utf-8 -*-
# author: Nishant Sharma (https://github.com/sevendaystoglory/)
# author: Madhav Kumar (https://github.com/madhav-mknc/)

import requests
from bs4 import BeautifulSoup

import random
import json

import openai

import os
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI
openai.api_key = os.environ["OPENAI_API_KEY"]


# get urls for the articles from the articles-base-url
def get_articles_from_url(url):
    print(f"[*] Fetching articles from {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_elements = soup.find_all('article')
    articles = [{
        'link': article.a['href'],
        'title': article.text.strip()
    } for article in article_elements]
    return articles

# scrape webpage
def scrape_content(url):
    print(f"[*] Scraping content from URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return ' '.join([p.text for p in paragraphs])

# summarize the content and convert into a tweet
def summarize_with_openai(content):
    print("[*] Summarizing content with OpenAI...")
    prompt = [{'role' : 'system', 'content' : "You will be given a certain scraped content. Don't worry, the creator has been asked for permission. You are to rephrase the content and write an interesting tweet about it from the perspective of a cool person who is also very intelligent and excited about new stuff. The person (he) will critique on the content wherever his opinions tell him to. So you are to make a tweet from his perspective. You can make it long or short depending on the level on interest or the mood of the person you are inpersonating. Give only the tweet as the response and nothing else. Make sure it looks like a real tweet!"}]
    prompt.append({'role' : 'user', 'content' : f" I am now giving you the content:\n\n{content}"})
    response = openai.ChatCompletion.create(
        messages = prompt,
        model = "gpt-4",
        temperature = 0.6,
    )
    print("[+] Summary completed!")
    return response.choices[0]['message']['content']

# make title for the tweet
def make_title_with_openai(tweet):
    print("[*] Making title with OpenAI...")
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"You will be given the content of a tweet. Frame a title in less than 6-7 words. Respond only with the title and nothing else. I will now proceed to give you the content of the tweet: \n\n{tweet}",
        max_tokens=150
    )
    title = response.choices[0].text.strip()
    print(f"[+] Title: {title}")
    return title

# compare two tweets for the better one
def compare_tweets(tweets, prev_tweet):
    print("Starting comparison with OpenAI...")
    prompt = [{'role' : 'system', 'content' : 'You will be given 10 different tweets from the same person. The person id confused as to which he should pick up and tweet on twitter. He is a sort of a nerd and a cool guy but is excited about new stuff and meaningful developments. However, he is relying on you as his AI assistant to select a tweet for him. He previously tweeted {prev_tweet}. I will be sending tweets in the format : 1. {tweet 1 content} \n 2. {tweet 2 content} ... \n 10. {tweet 10 content} . Fome the tweets given you are to select top 3, which go well with his previous tweet, not necessarily matching topics. Output format will be only space separated tweet number. e.g. If you think tweet number 3, 6 & 7 are best then output 3 6 7. I will now give you the tweets: '}]
    
    prompt = [{'role' : 'system', 'content' : 'You will be given 10 different tweets from the same person. The person id confused as to which he should pick up and tweet on twitter. He is a sort of a nerd and a cool guy but is excited about new stuff and meaningful developments. However, he is relying on you as his AI assistant to select a tweet for him. He previously tweeted {prev_tweet}. I will be sending tweets in the format : 1. {tweet 1 content} \n 2. {tweet 2 content} ... \n 10. {tweet 10 content} . Fome the tweets given you are to select top 3, which go well with his previous tweet, not necessarily matching topics. Output format will be only space separated tweet number. e.g. If you think tweet number 3, 6 & 7 are best then output 3 6 7. I will now give you the tweets: '}]
    response = openai.ChatCompletion.create(
        messages = prompt,
        model = "gpt-4",
        temperature = 0.2,
    )
    summary = response.choices[0]['message']['content']
    print("Summary completed!")
    return summary


# edit the tweet
def edit_tweet(suggestion="", tweet=""):
    prompt = [
        {
            'role' : 'system', 
            'content' : "You will be given a certain tweet. You are to enchance minimally the content as per the instrcutions provided by the user. Output only the final edited tweet and nothing else, for any exceptions you will output the same tweet. The user prompt will look like.\n\nTweet: {content of the tweet}\nInstruction: {user instructions}."
        },
        {
            'role': 'user',
            'content': f"Tweet: {tweet}\nInstruction: {suggestion}"
        }
    ]

    response = openai.ChatCompletion.create(
        messages = prompt,
        model = "gpt-4",
        temperature = 0.3,
    )

    reply = response.choices[0]['message']['content']
    return reply


# main
def get_maal(base_url):
    articles = get_articles_from_url(base_url)
    
    if not articles:
        print("[-] No articles found.")
        exit()

    MAX_ARTICLES = 5
    if len(articles) > MAX_ARTICLES:
        articles = random.sample(articles, MAX_ARTICLES)
    
    maal = []
    try:
        for i, article in enumerate(articles):
            url = article.get("link")
            print(f'[{i+1}] {url}')
            content = scrape_content(url)
            tweet = summarize_with_openai(content)
            title = make_title_with_openai(tweet)
            
            maal.append({
                'topic': title,
                'content': tweet
            })
    except KeyboardInterrupt: 
        print("closing...")
    except Exception as e:
        print("[!] Error occured:",str(e))

    with open('maal.json', 'w', encoding='utf-8') as file:
        json.dump(maal, file)
    print("[+] All topics processed!")
    return maal


if __name__ == "__main__":
    base_url = "https://www.artificialintelligence-news.com/"
    get_maal(base_url=base_url)


