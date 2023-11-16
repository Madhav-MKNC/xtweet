# Utilities / helper stuff

# update articles list
def write_articles_urls(updated_list):
    updated_list = list(set(updated_list))
    with open('.articles_store.json', 'w') as file:
        json.dump(updated_list, file)

# list of articles
def read_articles_urls():
    if not os.path.exists('.articles_store.json'):
        urls = ["https://www.artificialintelligence-news.com/"]
        write_articles_urls(urls)
        return urls
    with open('.articles_store.json', 'r') as file:
        urls = json.load(file)
        if not urls:
            urls = ["https://www.artificialintelligence-news.com/"]
            write_articles_urls(urls)
            return urls