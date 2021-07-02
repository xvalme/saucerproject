import requests

def finding(id):  #TODO #1
    
    '''
    Returns json of the characters found for the anime id that was inputed.
    '''

    try:
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
        response = requests.post(url, json={'query': query, 'variables': variables})

        return response.json()["data"]["Media"]["characters"]['nodes']

    except Exception as e:
        
       return 0