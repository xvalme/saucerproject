from bs4 import BeautifulSoup
from requests_html import HTMLSession
import hashlib
import os
import multiprocessing
import math
import requests
import json
import datetime
import cv2

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

            return link_list 

        except Exception as e:

            return [] 

    def bing_download_page(self, keywords, limit=300):

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
                 
            return link_list 

        except Exception as e:

            return []

    def download_from_links(self, keywords, source_id ,dic="data/"):

        urls = self.google_download_page(keywords)
        bing_links = self.bing_download_page(keywords)

        urls = bing_links + urls

        downloaded_items = 0

        if not os.path.isdir(dic):
                    
            raise Exception("No main data directory found.")

        try:
            session = requests.Session()
            
            dic = self.create_dic(dic=dic, keywords=keywords, source_id=source_id)

            for url in urls:

                downloaded_items += 1

                img_data = session.get(url).content   #Save with random hash

                with open(dic + str(hashlib.md5(url.encode('utf-8')).hexdigest()+".png"), 'wb') as handler:
                    handler.write(img_data)

        except Exception as e:
            print(e)
            
        #Running face_identifier right now to save memory
        self.face_identifier(directory=dic)

    def create_dic(self, dic, keywords, source_id):
        keywords = keywords.replace('/', ' ')
        name = (dic + source_id + '-' + keywords)
        name = name.replace('?', ' ')
        name = name.replace(':', ' ')
        name = name.replace('*', ' ')
        name = name.replace('"', ' ')
        name = name.replace('|', ' ')
        name = name.replace(chr(92), ' ')

        os.makedirs(name)
        
        return (name + '/')

    def face_identifier(self, directory, cascade_file='lbpcascade_animeface.xml'):
        '''Uses the cascade file to identify in each character directory the faces, and deletes the 
        initial images.'''
        
        if not os.path.isfile(cascade_file):
            raise RuntimeError("%s: not found" % cascade_file)
        
        cascade = cv2.CascadeClassifier(cascade_file)
        files = []
        
        for (dirpath, dirnames, filenames) in os.walk(directory):
            files.extend(filenames)
            break
        
        try:
            for image_file in files:
                image_file = directory + image_file
                
                image = cv2.imread(image_file)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                
                faces = cascade.detectMultiScale(gray,
                                                # detector options
                                                scaleFactor = 1.1,
                                                minNeighbors = 5,
                                                minSize = (30, 30))
                
                face_num = 0
                
                for (x, y, w, h) in faces:
                    
                    face_num += 1
                    
                    crop_img = image[y:y+h, x:x+w]
                    resized_image = cv2.resize(crop_img, (128, 128), interpolation=cv2.INTER_AREA)
                
                    cv2.imwrite(
                        str(image_file[:-4]) + '-' + str(face_num)+'.png',
                        resized_image
                    )
                    
                os.remove(image_file)
                
        except Exception as e:
            print(e)
        
def main(database='anime-offline-database.json', workers = 1, start_position=0):

    with open(database, 'r+',encoding='utf8') as anime_database:

        data = json.load(anime_database)    #Importing databse

        jobs = []

        number_of_anime = math.modf(len(data['data'])/int(workers))[1]
 
        for job in range(workers):

            p1 = multiprocessing.Process(target=json_to_character, args=(data["data"][int(job*number_of_anime):int((job+1)*number_of_anime)],job,start_position,))
            jobs.append(p1)

            p1.start()

def json_to_character(data, job, current_position=0):
    '''Given a json database it returns the characters for each anime'''

    for anime in data:
        current_position += 1

        print('[%s] Worker %s: %s / %s' % (datetime.datetime.now().strftime("%H:%M:%S"), job+1, current_position, len(data)))
        
        source = 0
        
        for sourc in anime['sources']: #Getting ID of anime
            if 'anilist.co' in sourc:
                source = sourc.rsplit('/', 1)[-1]
            else:
                pass

        for character in anime['characters']:

            image_downloader().download_from_links(anime['title'] + ' ' + str(character['name']['full']), source_id=source)

if __name__ == '__main__':
    main(database='anime-offline-database.json', workers=1, start_position=0)
