# AnimeRecSystem
CPSC558 Final Project
## Author:

Kaiyuan Sun
Beixi Hao 

# Anime Recommendation System
This program is a simple anime recommendation system that provides anime recommendations based on user preferences. It uses a list of anime data and their associated tags to generate recommendations based on the tags and anime that the user has provided.

## Usage

To run the program, simply execute the program file in the terminal with the command `python3 ARS.py`. The program will ask you to input commands to interact with it. The available commands are:

show all tags available - Prints a list of all the available tags in the dataset.
show all animes available - Prints a list of all the available animes in the dataset.
add your preference tag - Adds a tag that you like to your preference list.
add your preference anime - Adds an anime that you like to your preference list.
get recommendation - Generates a list of recommended animes based on your preferences.
clear all tags - Clears all the tags and animes in your preference list.
quit - Exits the program.
How it works
The program works by calculating a score for each anime based on the tags that the anime and the user's preference list share. The program then sorts the list of animes based on their scores and returns the top recommendations.

The "load()" function in the "loader.py" file is responsible for loading the anime data and tags into the program. The "recommend()" function takes in the user's preference list as arguments and generates a list of recommended animes.

# Conclusion
This program is a simple implementation of an anime recommendation system that demonstrates the basic concepts of recommendation systems. However, it is important to note that this program is not optimized for performance and may not provide accurate recommendations for large datasets.