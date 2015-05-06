Daniel Clarke
CS 6613 - Artificial Intelligence
Spring 2015
Project: Mini Camelot

Installation

Install the following dependencies:
python 3.4 (https://www.python.org/downloads/)
Flask 0.10 (http://flask.pocoo.org/)
Once installed, open your terminal can go to the app directory in the source code
Run the following command ‘$ python mini-camelot.py’
You should see output similar to this:
		‘* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)’
Open your browser and go to the given URL
Play your game! (To reset/restart, simply refresh the page).

Design
	
At first, I built the program to run in the console. You can see this by running the camelot.py file in the depreciated folder. The AI model uses the Minimax algorithm with Alpha-Beta Pruning. In addition to that, I build the graph search with an iterative depending approach. Initially the maximum depth the search will go to is a depth of 4. If the alpha-beta search is able to complete at this level in under 5 seconds, the max depth is incremented and the search is restarted. Since the game is infinite in depth (one could move his/her piece back and forth indefinitely), this seemed to be the best approach.
It was specified that we should implement a cutoff once such that the search never exceeds 10 seconds, hence the cutoff test look first to see if a given node is a leaf node, then if the current run-time of the search is close to 10s, it uses the evaluation function I designed to provide an accurate depiction of the game in the given state.

My evaluation function is as follows:
100 * ((0.2 * ((#white_pieces - #black_pieces)/5)) + (0.4 * (-1/min_distance_to_black_castle)) + (0.4 * (1/min_distance_to_white_castle)))

This gives us a number between -100 and 100, and takes into account both strategies of either attempting to win via capturing all enemy pieces and attempting to win by reaching the castle. I have weighted it in such a way that reaching the castle is more important (decided through experience).