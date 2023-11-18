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
MODEL = "gpt-3.5-turbo"

# no. of tweets to be displayed
MAX_ARTICLES = 5
Narticles = MAX_ARTICLES

# headers for get request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


# get urls for the articles from the articles-base-url
def get_articles_from_urls(urls=[]):
    if not urls:
        print("[-] No articles to crawl.")
        return []
    
    articles = []
    for url in urls:
        print(f"[*] Fetching articles from {url}...")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        article_elements = soup.find_all('article')
        if not article_elements:
            continue

        try:
            this_articles = [{
                'link': article.a['href'],
                'title': article.text.strip()
            } for article in article_elements]
            articles.extend(this_articles)
        except Exception as err:
            print("\033[31m" + '[error]', url, str(err) + "\033[m")
        
    return articles

# scrape webpage
def scrape_content(url):
    print(f"|- Scraping content from URL: {url}")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([p.text for p in paragraphs])
    # print(content) # remove this after testing
    return content

# summarize the content and convert into a tweet
def summarize_with_openai(content):
    print("|- Summarizing content with OpenAI...")
    prompt = [
        {
            'role' : 'system',
            'content' : "You will be given a certain scraped content. Don't worry, the creator has been asked for permission. You are to rephrase the content and write an interesting tweet about it from the perspective of a cool person who is also very intelligent and excited about new stuff. The person (he) will critique on the content wherever his opinions tell him to. So you are to make a tweet from his perspective. Give only the tweet as the response and nothing else. Make sure it looks like a real tweet and doesn't exceed the words limit which is 280 characters so make it short. Also, don't put any emojis or pictures in the tweet or any other extra characters like quotations or 'Tweet:'."
        },
        {
            'role' : 'user', 
            'content' : f" I am now giving you the content:\n\n{content}"
        }
    ]
    response = openai.ChatCompletion.create(
        messages = prompt,
        model = MODEL,
        temperature = 0.6,
    )
    print("|- Summary completed!")
    return response.choices[0]['message']['content']

# make title for the tweet
def make_title_with_openai(tweet):
    print("|- Making title with OpenAI...")
    prompt = [
        {
            "role": "system",
            "content": "You are an AI trained to create concise titles for tweets."
        },
        {
            "role": "user",
            "content": f"The following is the content of a tweet. Please provide a concise title for it in less than 6-7 words. The tweet is: \n\n{tweet}\n\nCan you suggest a suitable title? Just output the title with no other extra characters like quotations or 'Title:'."}
    ]
    response = openai.ChatCompletion.create(
        model = MODEL, 
        messages = prompt,
        max_tokens = 60
    )
    title = response['choices'][0]['message']['content'].strip()
    print(f"|- Title: {title}")
    return title

# compare two tweets for the better one
def compare_tweets(tweets, prev_tweet):
    print("[*] Starting comparison with OpenAI...")
    prompt = [
        {
            'role' : 'system',
            'content' : 'You will be given 10 different tweets from the same person. The person id confused as to which he should pick up and tweet on twitter. He is a sort of a nerd and a cool guy but is excited about new stuff and meaningful developments. However, he is relying on you as his AI assistant to select a tweet for him. He previously tweeted {prev_tweet}. I will be sending tweets in the format : 1. {tweet 1 content} \n 2. {tweet 2 content} ... \n 10. {tweet 10 content} . Fome the tweets given you are to select top 3, which go well with his previous tweet, not necessarily matching topics. Output format will be only space separated tweet number. e.g. If you think tweet number 3, 6 & 7 are best then output 3 6 7. I will now give you the tweets: '
        },
        {
            'role' : 'system', 
            'content' : 'You will be given 10 different tweets from the same person. The person id confused as to which he should pick up and tweet on twitter. He is a sort of a nerd and a cool guy but is excited about new stuff and meaningful developments. However, he is relying on you as his AI assistant to select a tweet for him. He previously tweeted {prev_tweet}. I will be sending tweets in the format : 1. {tweet 1 content} \n 2. {tweet 2 content} ... \n 10. {tweet 10 content} . Fome the tweets given you are to select top 3, which go well with his previous tweet, not necessarily matching topics. Output format will be only space separated tweet number. e.g. If you think tweet number 3, 6 & 7 are best then output 3 6 7. I will now give you the tweets: '
        }
    ]
    response = openai.ChatCompletion.create(
        messages = prompt,
        model = MODEL,
        temperature = 0.2,
    )
    summary = response.choices[0]['message']['content']
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
        model = MODEL,
        temperature = 0.3,
    )

    reply = response.choices[0]['message']['content']
    return reply


# main
def get_maal(base_urls=[]):
    articles = get_articles_from_urls(urls=base_urls)
    
    if not articles:
        print("[-] No articles found.")
        exit()

    print("[+] Total articles:", len(articles))

    global Narticles
    if len(articles) < MAX_ARTICLES:
        Narticles = len(articles)

    articles = random.sample(articles, Narticles)
    print(f"[+] Scraping {MAX_ARTICLES} articles randomly..")
    
    maal = []
    try:
        for i, article in enumerate(articles):
            try:
                url = article.get("link")
                print(f'[{i+1}]')
                content = scrape_content(url)
                tweet = summarize_with_openai(content)
                title = make_title_with_openai(tweet)
                
                maal.append({
                    'topic': title,
                    'content': tweet
                })
            except Exception as err:
                print("\033[31m" + '[error] fetching', url, str(err) + "\033[m")
    except KeyboardInterrupt: 
        print("closing...")
    except Exception as e:
        print("\033[93m" + '[!] Error occured:', str(err) + "\033[m")

    if not os.path.exists('tmp'): os.makedirs('tmp')
    with open('tmp/maal.json', 'w', encoding='utf-8') as file:
        json.dump(maal, file)
    
    print("[+] All topics processed!")
    return maal


if __name__ == "__main__":
    urls = ["https://vteam.ai/rss"]
    get_maal(urls)


