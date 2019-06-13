#!/usr/bin/python3

# -*- coding: utf -8 -*-

from bs4 import BeautifulSoup
from shutil import rmtree
from os import sep, path, mkdir
import requests


class Link:
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def describe(self, output=True):
        msg = "Hola! Soy un Link de url: '{}' y nombre: '{}'...".format(self.url, self.name)
        if output:
            print(msg)
        return msg


def perform_request(url="https://www.planetadelibros.com/libro-ruso-para-dummies/242847#soporte/242847", output=False):
    res = requests.get(url)
    if res.status_code != 200:
        print("Se ha piñado la petición...")
        exit(1)
    data = res.text
    if output:
        print(data)
    return data


def get_audio_links(data, output=False, audio_format="mp3"):
    soup = BeautifulSoup(data, 'html.parser')
    download_links = soup.findAll("a", {"class": "btn-download"})
    if output:
        for link in download_links:
            print(link)
    objects = []
    for link in download_links:
        url = link.get('href')
        name = link.get('data-tagging').split(':')[1].replace(" ", "_").lower()
        try:
            name.index(".")
        except:
            name = name + "." + audio_format
        parsed_link = Link(url, name)
        if output:
            parsed_link.describe(True)
        objects.append(parsed_link)
    return objects


def download_audio_link(link, folder, output=False):
    url = link.url
    filename = "{}{}{}".format(folder, sep, link.name)
    if output:
        print("Descargando el fichero: '{}'...".format(filename))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def prepare_path(pathname, output=True, destroyer=True):
    if not path.isdir(pathname):
        if output:
            print("El directorio {} no existe. Lo creo...".format(pathname))
        mkdir(pathname)
    else:
        if output:
            print("El directorio {} ya existe...".format(pathname))
        if destroyer:
            if output:
                print("Lo reviento....")
            rmtree(pathname, ignore_errors=True)
            if output:
                print("Y lo vuelvo a crear...")
            mkdir(pathname)


def main(folder="audio_data"):
    data = perform_request()
    links = get_audio_links(data)
    prepare_path(folder)
    for link in links:
        download_audio_link(link, folder, True)


if __name__ == "__main__":
    main()
