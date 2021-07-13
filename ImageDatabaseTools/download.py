from image_downloader import image_downloader
import os
import json
import cv2
import os
import sys
from glob import glob

'''
Downloading, for each anime in the database, and for each character, 
the images and saving them in data folder.
'''

def download(database_module):

    data = database_module

    iterations = 0

    while iterations < len(data["data"]):

        if data["data"][iterations]["downloaded"] == False:    #It was not already downloaded

            for url in data["data"][iterations]["sources"]: #Getting the ID of anime to create the directory with it + name

                if 'anilist.co' in url:     #Found anilist url to get the data.

                    id = str(url.rsplit('/', 1)[-1])

            for character in data["data"][iterations]["characters"]:   #Getting the characters

                dest = image_downloader().create_dic(str(id) + '+' + character['name']['full'])  #Creating directory
                image_downloader().download_from_links(data['data'][iterations]['title']+ ' anime '+ character['name']['full'], dic=dest)

                #bulk_convert(dst=dest)

            data["data"][iterations]["downloaded"] = True #So we don´t download the same anime again

            anime_database.seek(0)  # rewind
            json.dump(data, anime_database)
            anime_database.truncate()

        print(str(iterations) + "/" + str(len(data["data"]))) 
        iterations += 1
