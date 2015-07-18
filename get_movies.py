import urllib
import os
import json

class Movies():
    """ This class provides a way to store movie list information."""

    def __init__(self):
        print("Movies class assigned.")

    # get the list of movies and their wikipedia page url  
    def get_movie_list(self, pages):
        # use this index to assign to self.list 
        index = 0
        # set self.list to pages tuple with nested tuples for urls and titles
        self.list = pages
        # iterate through pages tuple 
        for page in pages:

            # open each wikipedia page containing a movie list 
            connection = urllib.urlopen("https://en.wikipedia.org/wiki/List_of_films:"+ page[0])
            output = connection.read()
            connection.close()
            link_beg_index = 0
            link_beg = '<li><i><a href="'
            link_end = '"'
            title_beg_index = 0
            title_beg = 'title="'
            title_end = '"'
            i = 0

            while link_beg_index < len(output):

                # parse the html to get links and titles for each movie
                if(output.find(link_beg, link_beg_index) > 0):
                    link_beg_index = output.find(link_beg, link_beg_index) + 16
                    link_end_index = output.find(link_end, link_beg_index)
                    title_beg_index = output.find(title_beg, link_end_index) + 7
                    title_end_index = output.find(title_end, title_beg_index)
                    url = (output[link_beg_index:link_end_index],)
                    title = (output[title_beg_index:title_end_index],)

                    # add new url and title to self.list item for each page
                    self.list[index][1] = self.list[index][1] + url
                    self.list[index][2] = self.list[index][2] + title
                    i = i + 1
                else:
                    break

            # save a list file
            object_to_save = json.dumps(self.list[index])
            output_string = self.list[index][0] + '.json'
            output_file = open(output_string, 'w')
            output_file.write(object_to_save)
            output_file.close()
            index = index + 1

    def process_item_query(self, query, selected):
        query_parts = ['list=', 'index=', 'url=', 'title=']
        queries = ['', '', '', '']
        i = 0
        for item in query_parts:
            item_beg = item
            item_beg_index = query.find(item_beg, 0) + len(item)
            item_end = "QQQ"
            item_end_index = query.find(item_end, item_beg_index)
            if item_end_index != -1:
                queries[i] = query[item_beg_index:item_end_index]
            else:
                queries[i] = query[item_beg_index:]
            i += 1

        # get poster image from wikipedia page
        wiki_page = urllib.urlopen("https://en.wikipedia.org"+ queries[2])
        wiki_page_output = wiki_page.read()
        wiki_page.close()
        img_tag_beg = '<img'
        img_tag_beg_index = wiki_page_output.find(img_tag_beg, 0)
        img_src_beg = 'src="'
        img_src_index_beg = wiki_page_output.find(img_src_beg, img_tag_beg_index) + 5
        img_src_end = '"'
        img_src_index_end = wiki_page_output.find(img_src_end, img_src_index_beg)
        img_src = wiki_page_output[img_src_index_beg:img_src_index_end]

        # get youtube url for embedded trailer
        search = urllib.urlopen('http://www.bing.com/search?q=youtube' + queries[3])
        search_output = search.read()
        search.close()
        video_link_beg = 'http://www.youtube.com/watch?v='
        video_link_beg_index = search_output.find(video_link_beg, 0) + 31
        video_link_end = '"'
        video_link_end_index = search_output.find(video_link_end, video_link_beg_index)
        video_link = search_output[video_link_beg_index:video_link_end_index]

        # save selected file for client to access
        selected_string_file = str(selected) + '.json'
        selected_json = json.dumps({'image': img_src, 'videoLink': video_link})
        selected_json_file = open(selected_string_file, 'w')
        selected_json_file.write(selected_json)
        selected_json_file.close()

class Movie():
    """ This class provides a way to store information for a single movie"""
        
    def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
