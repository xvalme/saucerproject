# Saucer AI Project
Basicaly, this is a facial image recognition (it even finds the corresponding characters and anime!), but for anime characters.
Given an input image, it searches for faces in it, then uses artificial intelligence to get the character as output.
The project aims to create an API using django so that anyone can use it without much of a mess.  

## How to use it  
-

## Folders and what each thing does  
**AnimeDatabase/** has a .json list of anime (almost 16k), with the characters each one has. The characters list does not come by default, so `charachter_finder.py` updates the database with them. `anilist_recognition` is called to pick this data from the Anilist API. 

## Want to contribute?  
Anyone interested just send a message so that we can discuss how to help, or just go to the current issues.

## Special Thanks
This project would be 10x harder if these resources were not available:  
Thanks to `anime-offline-database` for the default database that we use in this project.
Thanks to `Anilist` and their API to get the character´s data.

## Main colaborators
**xVal**, **milannzz** and **ae** are the current devs of the project.

