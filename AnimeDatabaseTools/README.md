# Contents
## Database
It has the most popular anime. It is the main database of the project.
The json has this structure:

**Root**
| Field | Type |
| --- | --- |
| data | ```Anime[]``` |

**Anime**
| Field | Type |
| --- | --- |
| sources | ```URL[]``` |
| title | ```String``` |

Using the ```<database_updater.py> <database> <update_database>``` the .json gets also the following keys:

**Anime**
| Field | Type | Explanation |
| --- | --- | --- |
| downloaded | ```Boolean```|  *If was already downloaded and added to the image database* |
| has_characters | ```Boolean```|  *If characters were found* |
| characters | ```String[]```|  *Name of characters in the show* |

To clean the database from anime entried without characters and delete useless keys, run ```<database_updater.py> <database> <clean_database>```.

