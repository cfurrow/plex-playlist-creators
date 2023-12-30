"""
Create a "Saturday Morning Cartoons" playlist from your Plex TV Show collections
named "80s Cartoons" and "90s Cartoons".

Update the values in .env to match your server. Google details on how to find
your X-Plex-Token value and put that in the .env file for PLEX_TOKEN

Then you can run this to create or recreate your playlist:

python cartoon_playlist.py
"""

import os, operator, time, sys, datetime, re
import requests
from no_ssl_verification import no_ssl_verification

from dotenv import load_dotenv
from plexapi.server import PlexServer

load_dotenv(verbose=True)

baseurl = os.environ['PLEX_URL']
token = os.environ['PLEX_TOKEN']

with no_ssl_verification():
  plex = PlexServer(baseurl, token)

  CARTOON_PLAYLIST_TITLE = 'Saturday Morning Cartoons'

  for playlist in plex.playlists():
    if playlist.title == CARTOON_PLAYLIST_TITLE:
      r = requests.delete('{}/playlists/{}?X-Plex-Token={}'.format(baseurl, playlist.key.split('/playlists/')[1], token))
      if r.status_code == 204:
        print('{} already exists. Deleting it and will rebuild.'.format(CARTOON_PLAYLIST_TITLE))
      else:
        print('Failed to remove old Playlist ')
        print(r)


  tv_shows_section = plex.library.section('TV Shows')
  episode_list = []

  for collection in tv_shows_section.collections():
    regexp = re.compile(r'(80s|90s) Cartoons')
    if not regexp.search(collection.title):
      break
    print(collection)
    for tv_show in collection.items():
      print(tv_show)
      for episode in tv_show.episodes():
        if not episode.isPlayed:
          print(episode.title)
          episode_list += episode
          break

  print('Adding {} cartoons to playlist.'.format(len(episode_list)))
  plex.createPlaylist(CARTOON_PLAYLIST_TITLE, items=episode_list)
