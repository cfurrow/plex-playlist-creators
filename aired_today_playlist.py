"""
Create a Plex Playlist with what was aired on this today's month-day, sort by oldest first.
If Playlist from yesterday exists delete and create today's.
If today's Playlist exists exit.

Make sure PLEX_URL is set in your ENV (e.g. http://192.168.1.72:32400)
Make sure PLEX_TOKEN is set in your ENV (get from app.plex.tv and open your dev console while playing a video)

To build a playlist for a given date:
python aired_today_playlist.py '2019-02-10'

To build a playlist for today's date:
python aired_today_playlist.py
"""

import os, operator, time, sys, datetime
import requests
from dotenv import load_dotenv
from plexapi.server import PlexServer
from no_ssl_verification import no_ssl_verification

load_dotenv(verbose=True)

if 'PLEX_URL' not in os.environ:
  print('PLEX_URL not found in ENV')
  exit(1)

if 'PLEX_TOKEN' not in os.environ:
  print('PLEX_TOKEN not found in ENV')
  exit(1)

baseurl = os.environ['PLEX_URL']
token = os.environ['PLEX_TOKEN']


with no_ssl_verification():
  plex = None
  try:
    plex = PlexServer(baseurl, token)
  except Exception as e:
    print('Plex Server not found at {}'.format(baseurl))
    print(e)
    exit(1)

  if plex is None:
    print('Plex Server not found at {}'.format(baseurl))
    exit(1)

  library_name = ['Movies', 'TV Shows'] # You library names

  child_lst = []
  aired_lst = []

  if len(sys.argv) > 1:
    date_arg = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
    date_in_seconds = time.mktime(date_arg.timetuple())
    today = time.gmtime(date_in_seconds)
  else:
    today = time.gmtime(time.time())


  TODAY_PLAY_TITLE = 'Aired Today {}-{}'.format(today.tm_mon, today.tm_mday)
  print('Building a playlist: {}'.format(TODAY_PLAY_TITLE))

  # Remove old Aired Today Playlists
  for playlist in plex.playlists():
    if playlist.title.startswith('Aired Today') and not playlist.title == TODAY_PLAY_TITLE:
      r = requests.delete('{}/playlists/{}?X-Plex-Token={}'.format(baseurl, playlist.key.split('/playlists/')[1], token))
      if r.status_code == 204:
        print('Removing old Aired Today Playlists ')
      else:
        print('Failed to remove old Aired Today Playlist ')
        print(r)
    elif playlist.title == TODAY_PLAY_TITLE:
      print('{} already exists. No need to make again.'.format(TODAY_PLAY_TITLE))
      exit(0)


  # Get all movies or episodes from LIBRARY_NAME
  for library in library_name:
    for child in plex.library.section(library).all():
      if child.type == 'movie':
        child_lst += [child]
      elif child.type == 'show':
        child_lst += child.episodes()
      else:
        pass


  # Find what aired with today's month-day
  # print('Looking for videos that aired in month {} and day {}'.format(str(today.tm_mon), str(today.tm_mday))

  for video in child_lst:
    try:
      if str(video.originallyAvailableAt.month) == str(today.tm_mon) \
        and str(video.originallyAvailableAt.day) == str(today.tm_mday):
        aired_lst += [[video] + [str(video.originallyAvailableAt)]]
    except Exception as e:
      pass
    # Sort by original air date, oldest first
    aired_lst = sorted(aired_lst, key=operator.itemgetter(1))

  # Remove date used for sorting
  play_lst = [x[0] for x in aired_lst]

  if len(aired_lst) > 0:
    # Create Playlist
    print('Adding {} videos to playlist.'.format(len(aired_lst)))
    plex.createPlaylist(TODAY_PLAY_TITLE, items=play_lst)
  else:
    print('Nothing to add!')
