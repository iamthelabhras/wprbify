import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import argparse
import re
import inflection
import shutil
import os
import requests
from termcolor import colored
from tqdm import tqdm
from tabulate import tabulate
from prettytable import PrettyTable

# Set your Spotify credentials here
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'

# Set the output file path for text file containing tracks not found on Spotify.
OUTPUT_FILE_PATH = "YOUR_OUTPUT_FILE_PATH"


# Set up Spotify API authorization
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

# Function to extract track info from WPRB playlist URL
def extract_track_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    spin_texts = soup.find_all('td', class_='spin-text')
    track_list = []
    for spin_text in spin_texts:
        artist = spin_text.find('span', class_='artist')
        song = spin_text.find('span', class_='song')
        album = spin_text.find('span', class_='release')
        if artist and song:
            artist = artist.text.strip()
            song = song.text.strip()
            album = album.text.strip() if album else None  # Make album data optional
            track_list.append((artist, song, album))
    return track_list

# Helper function to calculate similarity
def calculate_similarity(wprb_artist, wprb_song, wprb_album, spotify_artist, spotify_song, spotify_album):
    """
    Calculate the similarity score between WPRB track data and Spotify track data.

    Parameters:
        wprb_artist (str): The artist name from WPRB track data.
        wprb_song (str): The song name from WPRB track data.
        wprb_album (str): The album name from WPRB track data.
        spotify_artist (str): The artist name from Spotify track data.
        spotify_song (str): The song name from Spotify track data.
        spotify_album (str): The album name from Spotify track data.

    Returns:
        int: The similarity score between 0 and 100.
    """
    # Normalize and clean the data for comparison
    wprb_artist_normalized = re.sub(r'[^\w\s]', '', wprb_artist).lower()
    wprb_song_normalized = re.sub(r'[^\w\s]', '', wprb_song).lower()
    
    if wprb_album is not None:  # Check if album data is available
        wprb_album_normalized = re.sub(r'[^\w\s]', '', wprb_album).lower()
    else:
        wprb_album_normalized = None
    
    spotify_artist_normalized = re.sub(r'[^\w\s]', '', spotify_artist).lower()
    spotify_song_normalized = re.sub(r'[^\w\s]', '', spotify_song).lower()
    spotify_album_normalized = re.sub(r'[^\w\s]', '', spotify_album).lower()

    # Compare artist, song, and album data for similarity
    artist_match = SequenceMatcher(None, wprb_artist_normalized, spotify_artist_normalized).ratio()
    song_match = SequenceMatcher(None, wprb_song_normalized, spotify_song_normalized).ratio()
    album_match = SequenceMatcher(None, wprb_album_normalized, spotify_album_normalized).ratio() if wprb_album_normalized else 0

    # Calculate the weighted similarity and cap at 100
    similarity = int(min((artist_match + song_match + album_match * 2) / 3 * 100, 100))
    return similarity

# New function for song-only search in Spotify
def spotify_song_search(sp, song_name):
    """
    Performs a song-only search in Spotify.

    Parameters:
        sp (Spotipy.Spotify): The Spotify client instance.
        song_name (str): The song name to search for.

    Returns:
        list: A list of search results (tracks) from Spotify.
    """
    search_results = sp.search(q=song_name, type='track', limit=5)
    return search_results['tracks']['items']

# Updated wprb_search_results function
def wprb_search_results(wprb_artist, wprb_song, wprb_album):
    """
    Searches for tracks in Spotify and calculates similarity.

    Parameters:
        wprb_artist (str): Artist name from WPRB.
        wprb_song (str): Song name from WPRB.
        wprb_album (str): Album name from WPRB.

    Returns:
        list: A list of search results (tracks) from Spotify with similarity scores.
    """
    # Original search using artist, song, and album
    search_query = f"{wprb_song} {wprb_artist} {wprb_album}"
    search_results = sp.search(q=search_query, type='track', limit=5)

    results = []
    for track in search_results['tracks']['items']:
        spotify_artist = track['artists'][0]['name']
        spotify_song = track['name']
        spotify_album = track['album']['name']
        similarity = calculate_similarity(wprb_artist, wprb_song, wprb_album, spotify_artist, spotify_song, spotify_album)
        results.append((spotify_artist, spotify_song, spotify_album, similarity))

    # Sort search results by similarity (from most to least similar)
    results.sort(key=lambda x: x[3], reverse=True)

    # If no exact match, perform a song-only search in Spotify
    if not any(s[0].lower() == wprb_artist.lower() and s[1].lower() == wprb_song.lower() for s in results):
        song_results = spotify_song_search(sp, wprb_song)
        for track in song_results:
            spotify_artist = track['artists'][0]['name']
            spotify_song = track['name']
            spotify_album = track['album']['name']
            similarity = calculate_similarity(wprb_artist, wprb_song, wprb_album, spotify_artist, spotify_song, spotify_album)
            results.append((spotify_artist, spotify_song, spotify_album, similarity))

    # If still no results, perform an artist and song-only search in Spotify
    if not any(s[0].lower() == wprb_artist.lower() and s[1].lower() == wprb_song.lower() for s in results):
        artist_and_song_results = search_with_search_q(wprb_artist, wprb_song)
        for track in artist_and_song_results:
            spotify_artist = track['artists'][0]['name']
            spotify_song = track['name']
            spotify_album = track['album']['name']
            similarity = calculate_similarity(wprb_artist, wprb_song, wprb_album, spotify_artist, spotify_song, spotify_album)
            results.append((spotify_artist, spotify_song, spotify_album, similarity))

    return results

# Function for safe integer input
def safe_input_int(prompt):
    while True:
        try:
            choice = int(input(prompt))
            return choice
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to create a Spotify playlist & add tracks to it.
def create_spotify_playlist(sp, playlist_name, track_list):
    """
    Create a Spotify playlist and add tracks to it.

    Parameters:
        sp (spotipy.Spotify): Spotify API instance.
        playlist_name (str): Name of the playlist to be created.
        track_list (list): List of track data from WPRB URL.

    Returns:
        None
    """
    playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True)
    playlist_id = playlist['id']

    not_found_tracks = []
    skipped_tracks = []

    terminal_width = shutil.get_terminal_size().columns

    # Determine the column widths for table display
    col_widths = [5, (terminal_width - 33) // 3, (terminal_width - 33) // 3, (terminal_width - 33) // 3]

    for track in tqdm(track_list, desc="Processing tracks", unit="track"):
        artist, song, album = track  # Unpack the track tuple

        results = wprb_search_results(artist, song, album)

        # Indicate searching for WPRB playlist tracks
        separator = "♪" * 20
        print(colored(f"\n{separator} SCANNING SPOTIFY FOR WPRB PLAYLIST TRACKS {separator}", "yellow"))

        print("\n")
        print("Currently we're searching Spotify for ...")
        print(f"The song {colored(song, 'yellow')} by {colored(artist, 'yellow')} off of their album {colored(album, 'yellow')}.")
        print("\n")

        # Sort search results by similarity (from most to least similar) across different search approaches
        results.sort(key=lambda x: x[3], reverse=True)

        # Use a list to keep track of search results for this track
        chosen_results = []

        if results and results[0][3] == 100:
            track_uri = get_track_uri(sp, results[0][0], results[0][1])
            if track_uri:
                sp.playlist_add_items(playlist_id, [track_uri])
                print(f"PERFECT MATCH 🎯:  '{song}' by '{artist}'.  Adding this track to the playlist...")
            else:
                print(f"Sorry!  {song} by {artist} does not appear to be in Spotify's music library.")
                not_found_tracks.append(track)
        elif results:
            table_data = []
            counter = 1

            for res in results:
                # Truncate long names for better table display
                artist_truncated = res[0][:col_widths[2] - 3] + "..." if len(res[0]) > col_widths[2] else res[0]
                song_truncated = res[1][:col_widths[1] - 3] + "..." if len(res[1]) > col_widths[1] else res[1]
                album_truncated = res[2][:col_widths[3] - 3] + "..." if len(res[2]) > col_widths[3] else res[2]

                table_data.append([counter, song_truncated, artist_truncated, album_truncated, f"{res[3]}%"])
                counter += 1

            print(tabulate(table_data, headers=["No.", "Song", "Artist", "Album", "Similarity"], tablefmt="pretty"))

            choice = input("Input a value in the No. column to add a track to your playlist (or 's' to skip): ").strip()
            if choice == 's':
                print(f"Skipped '{song} - {artist}'.")
                skipped_tracks.append(track)
            elif choice.isdigit() and 1 <= int(choice) <= len(results):
                # Get the index of the chosen track in the original results list
                chosen_index = int(choice) - 1

                # Get the chosen result and directly add it to the playlist
                chosen_result = results[chosen_index]
                track_uri = get_track_uri(sp, chosen_result[0], chosen_result[1])
                if track_uri:
                    sp.playlist_add_items(playlist_id, [track_uri])
                    print(f"Added '{chosen_result[1]} - {chosen_result[0]}' to the playlist.")
                else:
                    print(f"No track found for '{chosen_result[1]} - {chosen_result[0]}'.")
                    not_found_tracks.append(track)
            else:
                print("Invalid choice. Skipped the track.")
                skipped_tracks.append(track)

        else:
            print(f"No search results found for '{song} - {artist}'. Skipped the track.")
            not_found_tracks.append(track)

    # Save not found and skipped tracks to a text file
    if not_found_tracks or skipped_tracks:
        playlist_name_snake_case = inflection.parameterize(playlist_name, separator='_')
        save_not_found_tracks(playlist_name_snake_case, not_found_tracks + skipped_tracks)

    print("\nFinished creating a Spotify playlist!")
    print(f"The playlist '{colored(playlist_name, 'yellow')}' is now ready on your Spotify account.")

# Function to search for track URI in Spotify
def get_track_uri(sp, artist, song):
    search_query = f"{song} {artist}"
    search_results = sp.search(q=search_query, type='track', limit=1)

    if search_results['tracks']['items']:
        return search_results['tracks']['items'][0]['uri']
    return None

def search_with_search_q(artist, song):
    """
    Perform a search using Spotipy's search_q method to find tracks with an exact match of artist and song.

    Parameters:
        artist (str): The artist name.
        song (str): The song name.

    Returns:
        list: A list of search results.
    """
    search_query = f'artist:"{artist}" track:"{song}"'
    search_results = sp.search(q=search_query, type='track', limit=5)
    return search_results['tracks']['items']

# Function to save the list of tracks not found in Spotify to a file
def save_not_found_tracks(playlist_name, not_found_tracks):
    """
    Saves the list of tracks not found in Spotify to a file.

    Parameters:
        playlist_name (str): The name of the Spotify playlist.
        not_found_tracks (list): A list of tuples containing track data (song, artist).
    """
    file_path = f"{OUTPUT_FILE_PATH}{playlist_name}-not_found_in_spotify.txt"
    with open(file_path, 'w') as file:
        for track in not_found_tracks:
            file.write(f"{track[0]} - {track[1]}\n")

# New function to fetch HTML content from URL or file
def fetch_html_content(input_source):
    if input_source.startswith('http://') or input_source.startswith('https://'):
        response = requests.get(input_source)
        if response.status_code == 200:
            return response.text
        else:
            print("Error fetching the HTML content from the URL.")
            return None
    else:
        try:
            with open(input_source, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("Error: File not found.")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Spotify playlist based on a WPRB playlist.")
    parser.add_argument("input_source", type=str, help="The WPRB playlist URL or path to the local HTML file.")
    parser.add_argument("playlist_name", type=str, help="The name for the Spotify playlist.")
    args = parser.parse_args()

    # Extract HTML content from URL or local file
    html_content = fetch_html_content(args.input_source)
    if html_content is None:
        exit()

    # Extract track info from the HTML content
    track_list = extract_track_info(html_content)

    # Create Spotify playlist and add tracks
    create_spotify_playlist(sp, args.playlist_name, track_list)
