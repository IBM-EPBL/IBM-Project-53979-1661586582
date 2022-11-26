from flask import Flask, jsonify, request
from newsapi import NewsApiClient
import re
from collections import Counter

from newsapi.newsapi_exception import NewsAPIException

app = Flask(__name__)

newsapi = NewsApiClient(api_key='2f8ecf96502842f284ab864d0a0ba76b')


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route('/generic/')
def get_generic_headlines():
    generic_headlines = newsapi.get_top_headlines(language='en')
    generic_headlines = generic_headlines['articles']
    generic_headlines = get_valid_articles(generic_headlines)[0:5]
    return jsonify(articles=generic_headlines)


@app.route('/cnn-fox/')
def get_cnn_fox_headlines():
    cnn_headlines = newsapi.get_top_headlines(sources='cnn', language='en')
    fox_headlines = newsapi.get_top_headlines(sources='fox-news', language='en')
    
    cnn_headlines = cnn_headlines['articles']
    fox_headlines = fox_headlines['articles']
    cnn_headlines = get_valid_articles(cnn_headlines)[0:4]
    fox_headlines = get_valid_articles(fox_headlines)[0:4]
    hl = cnn_headlines + fox_headlines
    
    return jsonify(articles=hl)


@app.route('/word-cloud/')
def get_word_cloud_words():
    top_headlines = newsapi.get_top_headlines(language='en', page_size=100)
    
    # extract titles
    titles = [article["title"] for article in top_headlines["articles"]]
    # extract words from titles
    title_words = [re.findall(r'[a-zA-Z]+', t) for t in titles]
    words = []
    for title in title_words:
        words.extend(title)
    
    # remove stop words
    stop_words = []
    with open("stopwords_en.txt", 'r') as file:
        for line in file:
            stop_words.append(line.rstrip())
            
    words = [word for word in words if word.lower() not in stop_words]
    cnt = Counter()
    for word in words:
        cnt[word] += 1
    word_cloud_words = [{"word": count[0], "size": count[1]*3}
                        for count in cnt.most_common(30)]
    return jsonify(words=word_cloud_words)


@app.route('/get-sources/<category>')
def get_sources_for_category(category):
    sources = newsapi.get_sources(language='en')
    if category != "all":
        sources = newsapi.get_sources(category=category,
                                      language='en',
                                      country='us')
    source_names = [s["name"] for s in sources["sources"]]
    source_ids = [s["id"] for s in sources["sources"]]
    source_names = source_names[0:10] if len(source_names) > 10 else source_names
    source_ids = source_ids[0:10] if len(source_ids) > 10 else source_ids
    return jsonify(source_names=source_names, source_ids=source_ids)


@app.route('/search/')
def get_search_results():
    args = request.args.to_dict()
    try:
        if args["src"] == "all":
            response = newsapi.get_everything(q=args["kw"],
                                              from_param=args["from"],
                                              to=args["to"],
                                              language="en",
                                              sort_by="publishedAt",
                                              page_size=100)
        else:
            response = newsapi.get_everything(q=args["kw"],
                                              sources=args["src"],
                                              from_param=args["from"],
                                              to=args["to"],
                                              language="en",
                                              sort_by="publishedAt",
                                              page_size=100)
    except NewsAPIException as ne:
        message = eval(str(ne))
        return jsonify(message)
    
    # if success, then return first 15 articles
    if response["status"] == "ok":
        response["articles"] = get_valid_articles(response["articles"])[0:15]
    return jsonify(response)


def get_valid_articles(articles):
    required_keys = ["author", "description", "title", "url", "urlToImage",
                     "publishedAt"]

    valid_articles = [h for h in articles
                      if all(h[key] for key in required_keys)]
    valid_articles = [h for h in valid_articles
                      if h["source"]["name"] is not None]
    return valid_articles


if __name__ == '__main__':
    app.run(port=5000,host="0.0.0.0")
