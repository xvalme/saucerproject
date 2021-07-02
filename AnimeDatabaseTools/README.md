# Contents
## anime-offline-database.json 
It has the most popular anime. The json has this structure:

**Root**
| Field | Type |
| --- | --- |
| data | ```Anime[]``` |

**Anime**
| Field | Type |
| --- | --- |
| sources | ```URL[]``` |
| title | ```String``` |
| type | ```Enum of [TV, MOVIE, OVA, ONA, SPECIAL, UNKNOWN]``` |
| episodes | ```Integer``` |
| status | ```Enum of [FINISHED, ONGOING, UPCOMING, UNKNOWN]``` |
| animeSeason | ```AnimeSeason``` |
| picture | ```URL``` |
| thumbnail | ```URL``` |
| synonyms | ```String[]``` |
| relations | ```URL[]``` |
| tags | ```String[]``` |
| downloaded | ```Boolean```|  *If was already downloaded and added to the image database*
| has_characters | ```Boolean```|  *If characters were found*
| characters | ```String[]```|  *Name of characters in the show*

## anilist_recognition.py 
Queries Anilist API using graphql. Simply call ```finding(id)``` to get the corresponding characters of that anime ID.

## charachter_finder.py 
Given a .json database of anime, picks the corresponding Anilist page and adds new keys with charachters (that were picked up via the anilist_recognition.py) information.