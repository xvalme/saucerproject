import json
from anilist_recognition import finding

class charachter_finder:
    '''
    Given a .json database of anime, picks the corresponding Anilist page and
    adds a new a new key with charachters (that were picked up via the 
    Anilist.co API).
    '''

    def __init__(self):
        pass

    def update_database(self, database='anime-offline-database.json'):
        '''
        Searches in the entire database for anilist.co links, gets the ID of them
        and calls anilist_recognition.finding to get the data from their API.
        Adds then the data to the database.
        '''
        with open(database, 'r+',encoding='utf8') as anime_database:

            data = json.load(anime_database)    #Importing databse

            iterations = 0
            
            while iterations < len(data["data"]):    #Checking every source that exists

                sources = data["data"][iterations]["sources"]   

                for url in sources:

                    if 'anilist.co' in url:     #Found anilist url to get the data.

                        id = url.rsplit('/', 1)[-1]

                        characters = finding(id)     #Get character list.

                        if characters == 0: #no data = no characters
                            data['data'][iterations]['has_characters'] = False
                        
                        if characters != 0: #Sucessfully completed request (even if there are none.)
                            #Updating json database 
                    
                            data["data"][iterations]['downloaded'] = False
                            data["data"][iterations]['characters'] = characters

                            if len(characters) == 0:
                                data['data'][iterations]['has_characters'] = False

                            else:
                                data['data'][iterations]['has_characters'] = True

                    if 'downloaded' not in data["data"][iterations]:
                        data['data'][iterations]['has_characters'] = False
                        data["data"][iterations]['characters'] = []
                        data["data"][iterations]['downloaded'] = False
                        

                print ("\033[A                             \033[A")
                print("Completed update of " + str(iterations) + "/" + str(len(data['data'])) )
                                 
                iterations += 1

            anime_database.seek(0)  # rewind
            json.dump(data, anime_database)
            anime_database.truncate()

    def clean_database(self, database='AnimeDatabase/anime-offline-database.json'):  #TODO #3
        '''
        Removes all content that does not have has_charachters == True, or don´t
        even have this key (i.e.problems in getting the data).
        '''
        with open(database, 'r+',encoding='utf8') as anime_database:

            data = json.load(anime_database)    #Importing databse

            iterations = 0
            
            while iterations < len(data["data"]):    #Checking every source that exists

                if 'has_characters' not in data["data"][iterations]:   #Did not get anything fron anilist, because there was no anilist.co link.
                    del data["data"][iterations]

                else:   #Got 0 data from anilist
                    if data["data"][iterations]["has_characters"] == False:
                        del data["data"][iterations]

                iterations += 1

            anime_database.seek(0)  # rewind
            json.dump(data, anime_database)
            anime_database.truncate()

def __init__():
    charachter_finder().update_database()
