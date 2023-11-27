
Inspired by https://gist.github.com/blacktwin/397f07724abebd1223ba6ea644ea1669
(my original gist https://gist.github.com/cfurrow/13a062359bd83ac17a38f8c4fcd3bab2)

## How to use
Be sure you have Pyton 3.9+ installed, then run:

```
pip install -r requirements.txt
```

Then get the URL of your plex server and your X-Plex-Token from the URL bar of your browser when you are logged in to your Plex server. [See Plex's help doc on how to do this](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

Then copy the `.env.example` file to a new file called `.env`, and set the following variables. Be sure to use the correct URL or IP address for your Plex server. In the example below, the Plex server is at IP address 192.168.0.110 and the port is 32400 (the default Plex port).

```sh
PLEX_URL="https://192.168.0.100:32400"
PLEX_TOKEN=your-token-here
```

Now you should be able to run either script:

```sh
python cartoon_playlist.py
# or this one:
python aired_today_playlist.py
# or this one:
python aired_today_playlist.py '2019-02-10'
```

You should see output like this depending on the script you ran:

```
python3.10 cartoon_playlist.py
Saturday Morning Cartoons already exists. Deleting it and will rebuild.
Saturday Morning Cartoons already exists. Deleting it and will rebuild.
<Collection:5043:80s-Cartoons>
...snipped...
Adding 30 cartoons to playlist.
```

Now go checkout your Plex server, and there will be a new playlist called "Saturday Morning Cartoons".

## Troubleshooting

If you see an error like this:

```
(401) unauthorized; https://192.168.0.100:32400/ <html><head><script>window.location = window.location.href.match(/(^.+\/)[^\/]*$/)[1] + 'web/index.html';</script><title>Unauthorized</title></head><body><h1>401 Unauthorized</h1></body></html>
```

That means the token you are using is not valid. Make sure you are using the correct token for the correct server.
