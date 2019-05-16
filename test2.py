from bson import ObjectId
import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import random
import datetime
from threads import Threads
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import urllib.request

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)



client = MongoClient('mongodb://localhost:27017/')
db = client['maynhac']
songs = db.songs

data = list(range(2, 38))

def func(data, extra):
    base_url = "https://chiasenhac.vn"
    link = "https://chiasenhac.vn/mp3/us-uk.html?tab=album-2019&page=" + str(data)
    fp = urllib.request.urlopen(link)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")  # Html page
    fp.close()
    soup = BeautifulSoup(mystr, 'html.parser')
    print('Find', len(soup.find_all('div', class_='card-header')), 'songs')
    for div in soup.find_all('div', class_='card-header'):
        try:
            song = {"numlike": random.randint(0, 1000000), "numlisten": random.randint(0, 1000000), "type": random.randint(1, 3), "__v": 0, "dateposted": datetime.datetime.utcnow()}
            sub_url = div.find_all('a')[0].get('href')
            full_url = base_url + sub_url
            fsub = urllib.request.urlopen(full_url)
            bs = fsub.read()
            page = bs.decode("utf8")    # Page data
            fsub.close()
            page_soup = BeautifulSoup(page, 'html.parser')
            card = page_soup.find_all('div',  class_='card card-details')[0]
            name = card.find_all('h4')[0].get_text()
            artist = card.find_all('li')[0].find_all('a')[0].get_text()
            avatar = card.find_all('img')[0].get('src')

            download_links = page_soup.find_all('a', class_='download_item')[0].get('href')
            song["name"] = name
            song["artist"] = artist
            song["unsignedname"] = name.lower()
            song["author"] = artist
            
            song["avatar"] = avatar
            song["lyrics"] = page_soup.find_all("div", id="fulllyric")[0].get_text()
            song["comments"] = []
            
            fileName = download_links[download_links.rfind('/') + 1: ]
            print(fileName)
            urllib.request.urlretrieve(download_links, fileName)
            file = drive.CreateFile({'title': fileName})
            file.SetContentFile(fileName)
            file.Upload()
            song["link"] = 'https://docs.google.com/uc?export=download&id=' + file['id']


            print('Inserting: ' + name)
            songs.insert_one(song)
        except Exception as e:
            print("type error: " + str(e))


threads = Threads(3, data)
threads.run(func, None)
threads.join()












    
