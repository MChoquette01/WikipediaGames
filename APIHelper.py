import requests
import sys


def get_trending_articles(date):
    """Retrieve trending articles for a given date, with an index denoting the order"""

    with open("Wikipedia API Credentials.txt", "r") as f:
        credentials = f.readlines()

    USERNAME = credentials[0].split(": ")[1].strip()
    PASSWORD = credentials[1].split(": ")[1].strip()

    if USERNAME == "<YOUR_USERNAME_HERE>":
        print("Update 'Wikipedia API Credentials.txt with your Wikipedia username to continue!")
        sys.exit(-1)
    if PASSWORD == "<YOUR_PASSWORD_HERE>":
        print("Update 'Wikipedia API Credentials.txt with your Wikipedia password to continue!")
        sys.exit(-1)

    S = requests.Session()

    # Retrieve login token first
    login_url = "https://www.mediawiki.org/w/api.php"
    params = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }

    resp = S.get(url=login_url, params=params).json()

    login_token = resp['query']['tokens']['logintoken']

    # Send a post request to login. Using the main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

    params = {
        'action': "login",
        'lgname': USERNAME,
        'lgpassword': PASSWORD,
        'lgtoken': login_token,
        'format': "json"
    }

    resp = S.post(login_url, data=params).json()

    # response should have succeeded
    assert resp['login']['result'] == 'Success'

    # now get the trending articles
    trends_url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/' + date

    headers = {
      'Authorization': login_token,
      'User-Agent': USERNAME
    }

    response = requests.get(trends_url, headers=headers)
    data = response.json()
    articles = []
    for idx, trending_article in enumerate(data['mostread']['articles']):
        title = trending_article['title'].replace('_', ' ')
        articles.append({"id": idx + 1, "title": title})

    return articles[:10]

