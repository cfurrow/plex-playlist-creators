
Inspired by https://gist.github.com/blacktwin/397f07724abebd1223ba6ea644ea1669

## How to use
Be sure you have Pyton 3.9+ installed, then run:

```
pip install -r requirements.txt
```

Then get the URL of your plex server and your X-Plex-Token from the URL bar of your browser when you are logged in to your Plex server. [See Plex's help doc on how to do this](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

Then copy the `.env.example` file to a new file called `.env`, and set the following variables:

```
PLEX_URL="https://192.168.0.100:32400"
PLEX_TOKEN=your-token-here
```

Now you should be able to run the script:

```
python cartoon_playlist.py
```

You should see output like this:

```
python3.10 cartoon_playlist.py
Saturday Morning Cartoons already exists. Deleting it and will rebuild.
Saturday Morning Cartoons already exists. Deleting it and will rebuild.
<Collection:5043:80s-Cartoons>
...snipped...
Adding 30 cartoons to playlist.
```

Now go checkout your Plex server, and there will be a new playlist called "Saturday Morning Cartoons".
