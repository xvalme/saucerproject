from bs4 import BeautifulSoup
from requests_html import HTMLSession
import hashlib
import os
from datetime import datetime
import multiprocessing
import math
import requests
import time
import json

class image_downloader:

    def __init__(self):
        pass

    def google_download_page(self, keywords):
         #Goes to google and makes a query with the keywords
         #return a list of links to download

        #Preparing url from keywords

        url = "https://www.google.com/search?q=" + (
            keywords.replace(' ','+')) + (
                "&sxsrf=ALeKk012aKzq5ZtEAObHa7bjYa-O7rAIZg:1624446613217&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj88diaz63xAhWszoUKHehvAjQQ_AUoAXoECAEQAw&biw=1280&bih=605")
        
        try:
            session = HTMLSession()

            r = session.get(url)   #starting session and get html

            soup = BeautifulSoup(r.content, 'html5lib') #prettify html

            link_list = []

            for img in soup.find_all('img'):   #finding images from 1st load of the page

                if img.get('data-src') is not None:   #Cleaning nones

                    link_list.append(img.get('data-src'))    #getting #data-src from each image

            #Error handling

            if len(link_list) == 0:

                raise Exception('Google did not find any images with that specification.')

            return link_list 

        except Exception as e:

            return [] 

    def bing_download_page(self, keywords, limit=20):

        try:   

            link_list = []

            base_url = "https://www.bing.com/images/search?q=" + (
                keywords.replace(' ','+'))
            current_position = "&first=1"

            url = base_url + current_position

            while len(link_list) < limit: #Will run until it passes the limit for the 1st time

                link_list_verifier = (len(link_list))

                session = HTMLSession()
                head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

                r = session.get(url, headers=head)   #starting session and get html

                soup = BeautifulSoup(r.content, 'html5lib') #prettify html

                for img in soup.find_all('img'):   #finding images from 1st load of the page

                    if (img.get('src') is not None) and ('OIP' in img.get('src')):   #Cleaning nones and nonimage stuff

                            link_list.append(img.get('src'))    
    
                    if img.get('data-src') is not None and 'OIP' in img.get('data-src'):

                            link_list.append(img.get('data-src'))

                    if (img.get('src') is not None) and ('OIF' in img.get('src')):   #Cleaning nones and nonimage stuff

                            link_list.append(img.get('src'))    
    
                    if img.get('data-src') is not None and 'OIF' in img.get('data-src'):

                            link_list.append(img.get('data-src'))

                url = base_url + "&first=" + str(len(link_list))  #Preparing link for next loop

                if len(link_list) - link_list_verifier < 10:  #There is almost no new stuff
                    break
                 
            #Error handling

            if len(link_list) == 0:

                raise Exception('Bing did not find any images with that specification.')

            return link_list 

        except Exception as e:

            return []

    def download_from_links(self, keywords, dic="data/"):

        dic = self.create_dic(dic=dic, keywords=keywords)

        urls = self.google_download_page(keywords)
        bing_links = self.bing_download_page(keywords)

        urls = bing_links + urls

        downloaded_items = 0
        
        if not os.path.isdir(dic):
                    
            raise Exception("No directory found.")

        if len(urls) == 0:

            raise Exception("No images returned for that query.")

        session = requests.Session()

        for url in urls:

            downloaded_items += 1

            img_data = session.get(url).content   #Save with random hash

            with open(dic + str(hashlib.md5(url.encode('utf-8')).hexdigest()+".png"), 'wb') as handler:
                handler.write(img_data)

    def create_dic(self, dic, keywords):
        name = (dic + keywords)
        name = name.replace('?', ' ')
        name = name.replace(':', ' ')
        name = name.replace('*', ' ')
        name = name.replace('"', ' ')
        name = name.replace('|', ' ')

        os.makedirs(name)
        
        return (name + '/')

def main(database='AnimeDatabaseTools/anime-offline-database.json', workers = 2):

    with open(database, 'r+',encoding='utf8') as anime_database:

        data = json.load(anime_database)    #Importing databse

        jobs = []

        number_of_anime = math.modf(len(data['data'])/int(workers))[1]
        rest = len(data["data"])-int(workers)*number_of_anime
 
        for job in range(workers):

            p1 = multiprocessing.Process(target=json_to_character, args=(data["data"][int(job*number_of_anime):int(job+1*number_of_anime)],))
            jobs.append(p1)

            p1.start()

def json_to_character(data):
    '''Given a json database it returns the characters for each anime'''

    for anime in data:

        for character in anime['characters']:

            image_downloader().download_from_links(anime['title'] + ' ' + str(character['name']['full']))

if __name__ == '__main__':
    main()