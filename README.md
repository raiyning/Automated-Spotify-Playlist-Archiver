# Discover Weekly Archiver

**Discover Weekly Archiver** is a tool that automates the archiving of your Discover Weekly playlists on Spotify. It offers:

- **Consolidated Archive**: Your Discover Weekly is appended to a single playlist containing all your archived Discover Weekly playlists.

This project harnesses the Spotify API for playlist management and utilizes GitHub Actions to automate the archiving workflow.

## Motivation

While there are similar projects available on GitHub for archiving Discover Weekly playlists, this project was created with specific goals in mind:

- **Personal Learning**: The project provided an opportunity to delve into the Spotify API and the intricacies of playlist management.

- **Unique Archiving **: It allows archiving to a consolidated, all-time playlist.


## Getting Started

To set up the Discover Weekly Archiver, follow these steps:

1. Clone the repository and install Python dependencies using Poetry:

   ```bash
   git clone git@github.com:raiyning/spotify-api.git && cd discovered-weekly
   poetry install
   ```

2. Create a `.env` file to store environment variables for local execution. Refer to `sample.env` for guidance on defining the necessary variables.

## Spotify Developer Account

To access and manage your Spotify playlists, you'll need to provide authorization through your Spotify Developer Account:

1. Visit https://developer.spotify.com/dashboard/ and log in to your Spotify account.

2. Create a new Spotify application.

3. Record the `CLIENT_ID` and `CLIENT_SECRET` from your app's main page in the `.env` file.

4. In your app's settings, add a redirect URI. If you're unfamiliar with OAuth, use a URI like `http://localhost:$PORT`, where `$PORT` is an available port on your machine.

5. Add the `REDIRECT_URI` to your `.env` file.

## Refresh Token

Authorize your Spotify app to read and write private playlists to your account:

1. Record your Spotify `USERNAME` in the `.env` file.

2. Run `python get_refresh_token.py` and follow the terminal instructions to complete the authentication flow.

3. Copy the `REFRESH_TOKEN` from the terminal and place it in your `.env` file to avoid repeating the authentication flow in the future.

## Playlist IDs

Obtain the unique IDs for your Discover Weekly playlist and the playlist used to store all your archived Discover Weeklies:

1. Right-click on the playlist in Spotify, select "Share," and then choose "Copy link to playlist." The link will be in the format: `http://open.spotify.com/playlist/$PLAYLIST_ID?x=abc`.

2. Record both your `DISCOVER_WEEKLY_PLAYLIST_ID` and `ALL_DISCOVERED_PLAYLIST_ID` in your `.env` file.

## Local Usage

Run the Discover Weekly Archiver locally with the following command:

```bash
python discovered_weekly.py
```

## Automated Usage

To automate the archiving process, fork this repository and configure GitHub Secrets with your environment variables. The workflow will execute every Tuesday. You can also manually trigger a run by navigating to Actions, selecting the "discovered-weekly" workflow, and clicking "Run workflow."

---
