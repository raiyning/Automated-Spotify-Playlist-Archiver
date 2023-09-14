import os
from os.path import join, dirname
from subprocess import Popen
import warnings

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Override sample with non-sample file-based env variables,
# and override both with actual env variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

# Authenticate
scopes = ["playlist-read-private", "playlist-modify-private","playlist-modify-public",]
auth_manager = SpotifyOAuth(
    scope=scopes,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
)

url = auth_manager.get_authorize_url()

redirect_server = None
# Start up a server at the redirct uri so that the browser has somewhere to go.
if "localhost" in REDIRECT_URI:
    port = REDIRECT_URI.rstrip("/").split(":")[-1]
    redirect_server = Popen(["python", "-m", "http.server", port])


print(f"1. Open the following link in your browser:\n\n{url}\n")
print("2. Accept the Spotify authorization.")

redirect_url = input(
    "3. Enter the URL that you got redirected to after accepting the authorization\n"
)
response_code = auth_manager.parse_response_code(redirect_url)
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    access_token = auth_manager.get_access_token(response_code)

print(f"Your refresh token is:\n\n{access_token['refresh_token']}\n")
print(f"Store this as the REFRESH_TOKEN in your environment variables")

if redirect_server is not None:
    redirect_server.terminate()