from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from pymongo import MongoClient

# locale.getlocale()
# Put locale in French for the date conversions
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

format_date = '%A %d %B %Y %H:%M'
# We get the unique url of each post, since sometime the contenu of the post is not complete on the listing page
list_urls = list()
results = list()
i = 1 
# while len() <= 200:
while  len(results) < 200:
    # Inspecting the page show that the feed of VDM is like: https://www.viedemerde.fr/?page=i, where i is the page
    # number
    url = 'http://www.viedemerde.fr/?page={}'.format(i)
    req = Request(url.format(i), headers={'User-Agent': 'Mozilla/5.0'})
    # Get the articles of the first page
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    # We only take the articles tag in the div jscroll-inner, since in the next div, we found the results of the 
    # page 2.
    list_articles =  soup.find_all(class_='jscroll-inner')[0].find_all('article', recursive=False)

    for article in list_articles:
        if len(results) < 200:
            # We inspect the html code in we see that the contenu is only in h2 and p tag
            # Sometimes we have text with h2 tag
            contenu_h2 = article.h2
            contenu_p = article.p

            if contenu_h2 and contenu_p:
                contenu = contenu_h2.text.strip() + '\n' + article.p.text.strip()
            elif contenu_h2:
                contenu = contenu_h2.text.strip()
            elif contenu_p:
                contenu = contenu_p.text.strip()

            article_info = article.find_all(class_='text-center')
            for info in article_info:
                info = info.text.strip()
                if info:
                    date_hour = info.split('\n')[1].replace('/', '').strip()
                    # date = ' '.join(date_hour.split(' ')[:-1])
                    date = datetime.strptime(date_hour, format_date)
                    # hour = date_hour.split(' ')[-1]
                    if len(info.split('\n')[0].replace('/', '').strip().split(' ')) > 1:
                        autor = info.split('\n')[0].replace('/', '').strip().split(' ')[1]
                    else:
                        autor = 'Inconnu'
            
            results.append({
                'id': i,
                'content': contenu,
                'date': date,
                # 'hour': hour,
                'autor': autor
            })
            i += 1
                    
        else:
            # We break the for loop when we reach 200 articles
            break



# Put the data in the db
_user = 'root'
_pwd = 'Ceci3st1pwd}'
_client = MongoClient(host='iadvize-db-svc', port=27017)
_db_ = _client.iAdvize
_db_.authenticate(str(_user), str(_pwd), source='admin')
name = 'vdm'

_db_[name].insert_many(results)

print('db_update')

# curl -i -X POST http://localhost/api/posts?author=Soweit"
# curl -i -X GET "http://localhost/api/posts/5"
# curl -i -X POST "http://localhost/api/posts?from=2016-10-25T21:00:00Z&to=2016-10-26T18:00:00Z"

# curl -i -X POST -H "Content-Type: application/json" -d '{"Camp": {"Adv":"test"} }'
# curl -i -X GET -H "Content-Type: application/json"  http://localhost/api/posts/5
