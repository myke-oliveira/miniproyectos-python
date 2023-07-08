#! /usr/bin/python3

import requests
from dotenv import load_dotenv
from os import getenv, get_terminal_size
from time import sleep


def main():
    load_dotenv()
    api_consumer = APIConsumer()
    formater = Formater()

    title = input("Enter the title: ")
    data = api_consumer.search(title)
    movies = data['results']

    # Saving API requests count
    for movie in movies[:5]:
        print(formater.format_movie(movie))
        # Avoid TOO MANY REQUESTS ERROR
        sleep(12)
        details = api_consumer.get_movie_details(movie['imdbid'])
        print(formater.format_movie_details(details))


class APIConsumer():
    def __init__(self):
        self.url = getenv('MOVIE_RATING_URL')
        self.api_key = getenv('MOVIE_RATING_API_KEY')
        self.api_host = getenv('MOVIE_RATING_API_HOST')

    def search(self, title, page=1):
        url = f'{self.url}/search'
        payload = {'title': title, 'page': str(page)}
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()

    def advanced_search(self, params):
        url = f'{self.url}/advancedsearch'
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_params(self, param_name):
        url = f'{self.url}/getParams'
        payload = {'param': param_name}
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()

    def get_movie_details(self, imdbid):
        url = f'{self.url}/gettitleDetails'
        payload = {'imdbid': imdbid}
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()

    def __str__(self):
        return f'Object<APIConsumer> ({self.api_host=}, {self.api_key=}, {self.api_host=})'


class Formater():
    def format_movie(self, movie):
        columns, _ = get_terminal_size()
        text = '-' * columns + '\n'
        text += movie.get('title').center(columns) + '\n'
        text += '-' * columns + '\n'
        text += f"Genre: {', '.join(movie.get('genre'))}\n"
        text += f"Released: {movie.get('released')}\n\n"
        text += f"Synopsis: {movie.get('synopsis')}"
        return text

    def format_movie_details(self, details):
        text = f'Languages: {", ".join(details.get("language"))}\n'
        text += f'Runtime: {details.get("runtime")}\n'
        text += f'Rating: {details.get("imdbrating")}\n'
        return text


if __name__ == '__main__':
    main()
