import json
import requests
import datetime

# remove this line and replace this NYTimes_API variable with your own NYTimes API key
from api_keys import NYTimes_API
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

giphy_API = "http://api.giphy.com/v1/gifs/translate?s="
gipy_API_key = "&api_key=dc6zaTOxFJmzC"
localtime = datetime.datetime.strftime(datetime.datetime.now(), '%m-%d')

def get_article_data():
    r = requests.get(NYTimes_API)
    data = r.json()

    with open('article_meta.json', 'r') as file:
        RESULTS = json.loads(file.read())

    # clear data
    RESULTS["children"] = []

    for article in data["results"]:

        # send to alchemy for keywords
        response = alchemyapi.keywords('text', article["abstract"])

        if response['status'] == 'OK':
            article_keywords = []

            for keyword in response['keywords']:
                article_kw = keyword['text'].encode('utf-8')
                article_keywords.append(article_kw)            

            giphy_urls = get_giphy_data(article_keywords)

        else:
            print('Error in keyword extaction call: ', response['statusInfo'])

        # timestamp retrieval
        RESULTS["time_updated"] = localtime

        RESULTS["children"].append({
            "title": article["title"],
            "abstract": article["abstract"],
            "url": article["url"],
            "tag" : giphy_urls[0],
            "img_url" : giphy_urls[1],
            "gif_url" : giphy_urls[2]
            })

        with open('article_meta.json', 'w') as file:
                file.write(json.dumps(RESULTS, indent=4))

    # print(RESULTS)
    # return RESULTS

def get_giphy_data(tags):
    giphy_urls=[]

    for tag in tags:
        query = tag.replace(" ","+")
        
        #search giphy api for gifs with the query tags
        giphy_res = requests.get(giphy_API + query + gipy_API_key) 
        giphy_data = giphy_res.json()

        if giphy_data['data']:
            img_url = giphy_data["data"]["images"]["original_still"]["url"]
            gif_url = giphy_data["data"]["images"]["original"]["url"]

            spaced = query.replace("+"," ")
            giphy_urls.append(spaced)
            break

    giphy_urls.extend([img_url,gif_url])

    return giphy_urls       

def main():
    get_article_data()


if __name__ == "__main__":
    main()