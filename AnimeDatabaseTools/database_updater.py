import json
import time
import os, sys
import requests

'''
Given a .json database of anime, picks the corresponding Anilist page and
adds a new a new key with charachters (that were picked up via the 
Anilist.co API).
'''

def update_database(database='anime-offline-database.json'):
    '''
    Searches in the entire database for anilist.co links, gets the ID of them
    and calls anilist_recognition.finding to get the data from their API.
    Adds then the data to the database.
    '''
    with open(database, 'r+',encoding='utf8') as anime_database:

        data = json.load(anime_database)    #Importing databse

        iterations = 0
        internet_fails = 0
        start_time =  time.time()
        time.sleep(0.0000000000001)  #Avoiding division by 0
        
        while iterations < len(data["data"]):    #Checking every source that exists

            sources = data["data"][iterations]["sources"]   

            for url in sources:

                if 'anilist.co' in url:     #Found anilist url to get the data.

                    id = url.rsplit('/', 1)[-1]   #Last part of url has ID

                    characters = finding(id)     #Get character list.
                    
                    if characters == 'Connection Error':
                        time.sleep(10)   #Wait a bit and retry
                        internet_fails += 1
                        characters = finding(id)

                    if characters == 'Not found' or characters == [] or characters == 'Connection Error': #no data = no characters
                        data['data'][iterations]['has_characters'] = False
                        data["data"][iterations]['downloaded'] = False
                        data["data"][iterations]['characters'] = []

                    else:
                        if characters != 0: #Sucessfully completed request
                        #Updating json database 
                
                            data["data"][iterations]['downloaded'] = False
                            data["data"][iterations]['characters'] = characters
                            data['data'][iterations]['has_characters'] = True

            if 'downloaded' not in data["data"][iterations]:  #IF it was not found, there is no data from anilist
                data['data'][iterations]['has_characters'] = False
                data["data"][iterations]['characters'] = []
                data["data"][iterations]['downloaded'] = False
                    
            
            print('''Completed update of %s/%s | Internet fails up now: %s | Velocity: %s characters/second'''
            % (str(iterations),
                str(len(data["data"])),
                    internet_fails, 
                        round(float(iterations)/float(time.time() - start_time), 3)
                            ),
            end='\r')
                                
            iterations += 1

        anime_database.seek(0)  # rewind
        anime_database.write(json.dumps(data, indent=True))
        anime_database.truncate()

def clean_database(database='anime-offline-database.json'):
    '''
    Removes all content that does not have has_charachters == True, or don´t
    even have this key (i.e.problems in getting the data).
    '''

    with open(database, 'r',encoding='utf8') as anime_database:

        data = json.load(anime_database)    #Importing databse
        iterations = 0
        print('Database Loaded...')

    while iterations < len(data["data"]) :    #Checking every source that exists
        print(str(iterations) + '/' + str(len(data["data"])) + ' entried cleaned.', end='\r')

        #Start by deleting the keys we don´t want:
        data["data"][iterations].pop('type', None)
        data["data"][iterations].pop('episodes', None)
        data["data"][iterations].pop('status', None)
        data["data"][iterations].pop('animeSeason', None)
        data["data"][iterations].pop('picture', None)
        data["data"][iterations].pop('thumbnail', None)
        data["data"][iterations].pop('relations', None)
        data["data"][iterations].pop('tags', None)
        data["data"][iterations].pop('synonyms', None)

        if 'has_characters' not in data["data"][iterations]:   #Did not get anything fron anilist, because there was no anilist.co link.

            del data["data"][iterations]

        else:
            if (
                data["data"][iterations]["has_characters"] == False) or (
                    data["data"][iterations]["characters"] == []
                    ): #Cleaning if there are no  charachters

                del data["data"][iterations]

            else:
                iterations += 1
               
    with open(database, 'w',encoding='utf8') as anime_database:
        anime_database.seek(0)  # rewind
        anime_database.write(json.dumps(data, indent=True))
        anime_database.truncate()

def finding(id): 
    
    '''
    Returns json of the characters found for the anime id that was inputed.
    '''

    query = '''
    query ($id: Int) { 
    Media (id: $id, type: ANIME) { 
        characters(sort: ID){
            nodes {
                name {
                    full
                }
            }
        }
    }
    }
    '''

    #Id of the anime
    variables = {
        'id': id
    }

    url = 'https://graphql.anilist.co'

    # Make the Api request
    session = requests.Session()

    try:
        response = session.post(url, json={'query': query, 'variables': variables})
        
    except Exception:
        return 'Connection Error'

    try:
        return response.json()["data"]["Media"]["characters"]['nodes']

    except:   #Not found
        return 'Not found'

def main():
    
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: database_updater.py <database-dir> <update_database or clean_database>\n")
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        raise RuntimeError("%s: not found" % database)

    elif sys.argv[2] == 'update_database':
        update_database(sys.argv[1])
    
    elif sys.argv[2] == 'clean_database':
        clean_database(sys.argv[1])

    else:
        sys.stderr.write("Operation could not be perfomed. Usage: database_updater.py <database-dir> <update_database or clean_database>\n")
        sys.exit(-1)
    

if __name__ == '__main__':
    main()