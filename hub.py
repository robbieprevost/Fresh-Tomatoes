import get_movies
import SimpleHTTPServer
import SocketServer
from urlparse import urlparse
import json
import os



# tuple containing url endings for wikipedia pages with film lists
pages = (
        ["_numbers",(),()],["_A",(),()],
        ["_B",(),()],["_C",(),()],
        ["_D",(),()],["_E",(),()],
        ["_F",(),()],["_G",(),()],
        ["_H",(),()],["_I",(),()],
        ["_J-K",(),()],["_L",(),()],
        ["_M",(),()],["_N-O",(),()],
        ["_P",(),()],["_Q-R",(),()],
        ["_S",(),()],["_T",(),()],
        ["_U-W",(),()],["_X-Z",(),()]
        )

# set some featured movies for the front page
interstellar = get_movies.Movie(
    "Interstellar",
    "A crew of astronauts in search of a new home for humanity",
    "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",  # noqa
    "https://www.youtube.com/watch?v=2LqzF5WauAw")

batman_vs_superman = get_movies.Movie(
    "Batman v Superman",
    "Two titans collide",
    "https://upload.wikimedia.org/wikipedia/en/2/20/Batman_v_Superman_poster.jpg",  # noqa
    "https://www.youtube.com/watch?v=xe1LrMqURuw")

the_avengers = get_movies.Movie(
    "The Avengers",
    "Earth's mightiest heroes team up to save it",
    "https://upload.wikimedia.org/wikipedia/en/f/f9/TheAvengers2012Poster.jpg",  # noqa
    "https://www.youtube.com/watch?v=eOrNdBpGMv8")

midnight_in_paris = get_movies.Movie(
    "Midnight in Paris",
    "Going back in time to meet authors",
    "http://upload.wikimedia.org/wikipedia/en/9/9f/Midnight_in_Paris_Poster.jpg",  # noqa
    "https://www.youtube.com/watch?v=FAfR8omt-CY")

hunger_games = get_movies.Movie(
    "Hunger Games",
    "A real real reality show",
    "http://upload.wikimedia.org/wikipedia/en/4/42/HungerGamesPoster.jpg",  # noqa
    "https://www.youtube.com/watch?v=PbA63a7H0bo")

# convert featured movies to json
featured = json.dumps({ "featured" : [interstellar.__dict__, batman_vs_superman.__dict__,
                                      the_avengers.__dict__, midnight_in_paris.__dict__,
                                      hunger_games.__dict__]})

# save featured movies json to a file for client to access 
featured_file = open("featured.json", 'w')
featured_file.write(featured)
featured_file.close()

# save page for list item queries
featured_file = open("selected.html", 'w')
featured_file.write('Thanks for the request!!!')
featured_file.close()

# create iterating variable for list item queries 
selected = 0

# get our movies lists from wikipedia
my_movies = get_movies.Movies()
my_movies.get_movie_list(pages)

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/selected":
            global selected

            # clean up some of the selected item files 
            if selected > 5:
                remove_index = 0
                temp = selected - 5
                while remove_index < 5:
                    temp_file = str(temp + remove_index) + '.json'
                    os.remove(temp_file)
                    remove_index += 1
                    selected = 0
            else:
                selected += 1
            self.processMyRequest(url.query, selected)
        else: 
            if self.path == '/':
                self.path = '/new_fresh_tomatoes_static.html'
            if self.path == '/featured':
                self.path = '/featured.json'
            for page in pages:
                if self.path == "/" + page[0]:
                    self.path = '/' + page[0] + '.json'
            
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    # this function starts the process of getting our selected film data
    def processMyRequest(self, query, selected):
        featured_file = open("selected.html", 'w')
        featured_file.write(str(selected))
        featured_file.close()
        self.path = "/selected.html"
        my_movies.process_item_query(query, selected)
        
# set up and start our server
Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)
server.serve_forever()
