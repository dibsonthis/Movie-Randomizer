import requests
from bs4 import BeautifulSoup
import json
import random

# genres = ['action-and-adventure', 'animation', 'anime', 'biography', 'children', 'comedy', 'crime', 'cult', 'documentary', 'drama', 'family', 'fantasy', 'history', 'horror', 'mystery', 'romance', 'science-fiction', 'thriller', 'all']

genres = ['fantasy', 'history', 'horror', 'mystery', 'romance', 'science-fiction', 'thriller', 'all']


def get_titles(genre, amount=100):

    all_titles = []

    for offset in range(amount)[::50]:

        if genre == "all":
            url = "https://reelgood.com/movies/source/netflix?offset=" + str(offset)
        else:
            url = "https://reelgood.com/movies/genre/" + genre + "/on-netflix?offset=" + str(offset)

        raw_html = requests.get(url).content

        html = BeautifulSoup(raw_html, 'html.parser')

        all_title_blocks = html.select('tr')

        for title_block in all_title_blocks:
            if title_block.select('td'):
                title = title_block.select('td')[1].get_text()
                all_titles.append(title)
                print(title + ' - Title Added')

    return all_titles

def get_images(genre, amount=100):

    all_images = []

    for offset in range(amount)[::50]:

        if genre == "all":
            url = "https://reelgood.com/movies/source/netflix?offset=" + str(offset)
        else:
            url = "https://reelgood.com/movies/genre/" + genre + "/on-netflix?offset=" + str(offset)

        raw_html = requests.get(url).content

        html = BeautifulSoup(raw_html, 'html.parser')

        all_title_blocks = html.select('tr')

        for title_block in all_title_blocks:
            if title_block.select('td'):
                title = title_block.select('td')
                all_images.append(title)

        image_links = []

        for index, image in enumerate(all_images):
            try:
                link = image[0].select('img')[0]['src']
            except IndexError:
                link = "static/images/no-image.png"
            image_links.append(link)
            print('Image Added - ({}/{})'.format(index+1,len(all_images)))

    return image_links

def get_description(title):

    search_url = "https://www.google.com/search?q=" + title + " movie summary"

    raw_html = requests.get(search_url).content

    html = BeautifulSoup(raw_html, 'html.parser')

    all_divs = html.select('div')

    result = []

    for i in all_divs:
        if i.get('class') == ['BNeawe', 's3v9rd', 'AP7Wnd']:
            result.append(i)

    try:
        result = result[2].get_text()
    except IndexError:
        result = 'No Description Available'

    return result


def get_descriptions(titles):

    descriptions = []

    search_url = "https://www.google.com/search?q="

    for index, title in enumerate(titles):
        description = get_description(title)
        descriptions.append(description)
        print(title + ' - Description Added ({}/{})'.format(index+1, len(titles)))

    return descriptions

def get_genre(genre, amount):

    titles = get_titles(genre, amount)
    images = get_images(genre, amount)
    descriptions = get_descriptions(titles)

    result = []

    for index, title in enumerate(titles):
        result.append( {'title': title, 'description': descriptions[index], 'img': images[index]} )

    with open('genres/' + genre + '.txt', 'w') as file:
        json.dump(result, file)

def get_all(genres, amount=100):
    for index, genre in enumerate(genres):
        get_genre(genre, amount)
        print(genre + ' - Added ({}/{})'.format(index+1, len(genres)))

def randomize(genre):
    result = []
    with open('genres/' + genre + '.txt') as file:
        result = json.load(file)

    random_number = random.randint(0,len(result)-1)

    random_result = result[random_number]

    return random_result
