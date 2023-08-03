# WPRBIFY
![wprb](https://github.com/iamthelabhras/wprbify/assets/17169600/4dc1b1b1-13da-402a-bf52-c458849a5326)

WPRBify is a Python script (`wprbify.py`) that allows users to quickly & easily convert a WPRB playlist into a Spotify playlist.  

And when I say quickly, I mean _quickly_: in my experience, this script can process a 3-hour, 40+ song playlist in about 1 minute!

Once properly configured on your computer, this script can be executed on the command line via:

```bash
python wprbify.py <input_source> "<playlist_name>"
```

| Argument           | Description                                                                                              |
|--------------------|----------------------------------------------------------------------------------------------------------|
| `<input_source>`   | A WPRB playlist URL<sup>*</sup> or a file path to WPRB playlist saved as an HTML file.                   |
| `<playlist_name>`  | The name of the Spotify playlist you'd like to create.                                                  |

Don't forget the quotation marks (`""`) around `<playlist_name>`.  They're easy to miss, but the script won't run without them!

<sup>*</sup> <sup><sub>Technically, this script will work with _any_ playlist URL found on [Spinitron's website](https://spinitron.com/).</sub></sup>


## Table of Contents

- [Overview](#overview)
- [About WPRB](#about-wprb)
- [Step-by-Step Instructions On How To Set Up WPRBify](#step-by-step-instructions-on-how-to-set-up-wprbify)
- [Nerd Stuff For Nerds](#nerd-stuff-for-nerds)
- [Similarity Score](#similarity-score)
- [Bug Reports & Pull Requests](#bug-reports--pull-requests)


## Overview

How does this WPRBify work?  

Well, in the broad strokes, it:

- Extracts data from a WPRB playlist.
- Creates a new Spotify playlist.
- Searches Spotify's music library using the extracted WPRB playlist data.
- Adds matching tracks to the new playlist.
- Outputs a list of tracks it was unable to add to the new playlist.

It's probably easier for me to _show_ you how this works rather than tell you.  

Here's a screen recording of me using WPRBify to process a recent (2023-07-30) [Princeton Blue Ribbon](https://playlists.wprb.com/WPRB/show/208579/Princeton-Blue-Ribbon) playlist:




https://github.com/iamthelabhras/wprbify/assets/17169600/8f75cd17-17d8-4388-be1b-ef5f08bc4f0c




Pretty cool, right?  (And yes, Smog's _Supper_ is an amazing album!)

As you may have noticed, many of the playlist tracks processed by this script were _automatically_ added to the Spotify playlist.  
  
That's because this script only asks for user input when it can't find an exact match for a WPRB playlist track in Spotify's music library.  

When this happens, the script generates a table of Spotify search results (visible at 00:20 & 00:38 in the screen recording), rank-ordered by a [similiarity score](#similarity-score), & asks the user to select which track they'd like added to the playlist.  

Sometimes WPRB tracks simply aren't available on Spotify, in which case none of the tabulated search results will match up with a WPRB playlist track.  Here, the user has the option to simply skip the track & the script will continue processing the playlist.  

In the highly unlikely event a search of Spotify's music library returns _no_ results, the script will automatically skip the WPRB playlist track & continue processing a playlist without any input from the user.

The script also keeps tabs on any WPRB playlist tracks it hasn't added to a Spotify playlist.  If any such tracks exist, the script outputs a text file when it finishes running containing these tracks' data (i.e. song, artist, album).  

You're free to do anything you like with this text file -  including deleting it - but I recommend using it to manually search Spotify's music library & confirm the missing tracks are, indeed, unavailable on Spotify.  No computer program is perfect!

Again, this is a high level overview of the script's basic functionality.  You can find more detailed information about WPRBify's inner workings in the [Nerd Stuff For Nerds](#nerd-stuff-for-nerds) section.


## About WPRB

I wrote this script for current WPRB listeners, but I'd be thrilled if it managed to bring even just one first-time listener into the WPRB fold.  If you've never heard of WPRB, please read on! 

[WPRB 103.3FM](https://wprb.com/) is a community radio station located at Princeton University in Princeton, New Jersey.  It has a long & rich history in the world of college radio, dating back to its founding in 1940.  The station is known for its diverse & eclectic programming, as well as its devoted listener fanbase.  (Indeed, some of us are such devoted listeners that we do crazy things in our spare time like write Python scripts to process WPRB playlists...).

### Links

- [WPRB Website](https://wprb.com/): Visit WPRB's official website of to explore its history, schedule, DJ profiles, & more.
- [WPRB's Spinitron Account](https://spinitron.com/WPRB/): Check out WPRB's Spinitron account to view playlists & track information for recent broadcasts.
- [WPRB Livestream](https://listen.wprb.com): Listen to WPRB's current broadcast live on the interwebs!


## Step-by-Step Instructions On How To Set Up WPRBify

I didn't just create WPRBify for myself; I hoped it would be something _all_ WPRB listeners might find useful.  

That said, I realize downloading, configuring, & running a script can be a daunting undertaking for people with little-to-no programming experience.

That's why I created this section for WPRB listeners with limited computer skills.

If this sounds like you, follow the step-by-step instructions below to get WPRBify up-and-running on your computer.

### I. Set Up Spotify API Credentials:

Spotify's API ("Application Programming Interface") acts as a bridge between WPRBify & Spotify's vast music library & services. It allows the script to communicate with Spotify's servers, enabling functions like searching for tracks, creating playlists, & accessing other music-related information from your Spotify account. Think of an API as a set of rules & protocols that allow different software applications to communicate with each other.  Sort of like Esperanto, but useful.

Before we tackle downloading & configuring the Python script itself, we'll need to set up your Spotify API credentials.

#### 1. Sign Up For A Spotify For Developers Account

> Head over to the [Spotify for Developers](https://developer.spotify.com/) website & sign up for a (free) Spotify for Developers Account.  
> 
> If you already have a Spotify account, you can use the same credentials you use to log into Spotify to log into Spotify for Developers.  

#### 2. Navigate To The Spotify Developer Dashboard

> Once you're logged in:
> 
> - Click on the rounded-teal pill with your Spotify user profile picture & name (upper-right-hand corner of your browser window).
> - Select "Dashboard" to navigate to the Spotify for Developers Dashboard. 
> 
> This is where you'll create & manage the Spotify API credentials your script needs to run properly.

#### 3. Create A New Application

> Once you've accessed the Spotify for Developers Dashboard:
>
> - Click on the rounded-blue pill labelled "Create app" (upper-right-hand corner of your browser window).
>
>This will bring you to a "Create app" screen with four text inputs labelled "App name", "App description", "Website", & "Redirect URI".  
>
> - Copy & paste the text in the "Text Input Value" column below into the corresponding text input.
>
> | **Text Input Field** | **Text Input Value (Copy & Paste)**                            |
> |----------------------|----------------------------------------------------------------|
> | App name             | WPRBify                             |
> | App Description      | An app that uses WPRB playlists to generate Spotify playlists. |
> | Redirect URI         | https://localhost:8888/callback                                |
>
> - Check the box next to "I understand and agree with Spotify's Developer Terms of Service and Design Guidlines" (bottom of your browser window). 
> - Click the rounded-blue pill labelled "Save" (bottom of your browser window).

#### 4. Obtain Your Client ID & Client Secret

> Once you've successfully created your app, you'll be taken to the app's "Home" screen.  
>
> We now need to locate the "Client ID" & "Client secret" keys that were auto-generated when you created your app:
>
> - Click on the white-rounded pill labelled "Settings" (upper-right-hand corner of your browser window).  
> 
> This will take you to your app's "Basic Information" screen.
> 
> You should see "Client ID"  - a long series of letters & numbers - prominently displayed in your browser.  
> 
> - Click on the "copy" icon (two square icons placed one-above-the-other) to the right of the Client ID.
> 
> This will copy your Client ID into your system clipboard. 
> 
> - Open a new document on your computer.
> 
> This new document can be anything you want: a text file, a Word doc, a Google doc, an e-mail to yourself, etc.  It doesn't matter. 
> 
> - Paste your Client ID into your new document.
> - Click on the blue "View client secret" text positioned beneath your Client ID to reveal your Client secret.
> 
> Your Client secret is another long series of letters & numbers.  
> 
> - Click on the "copy" icon to the right of the Client secret.
> 
> This will copy your Client secret into your system clipboard. 
>
> - Paste your Client secret into your new document.  
> - Save your new document.  Be sure you know where to find this document, because we'll need to reference it later!


### II. Install Python & Required Python Libraries

WPRBify is written in Python, a popular & versatile programming language known for its simplicity & readability.  In order to run this script, Python must be installed on your computer.

We'll also need to install some Python _libraries_ on your computer.  These libraries enhance WPRBify's functionality & handle tasks like web scraping, data processing, & interfacing with Spotify's API.  Even if you already have Python installed on your computer, WPRBify will _not run_ without these libraries.

We'll be doing all this via your computer's command line.  

The command line, also known as the terminal or the shell, is a text-based interface that allows you to interact with your computer using text commands.  If you have limited computer skills, you've probably never worked with the command line before.  Don't panic!  Although it may look intimidating, the command line is actually very easy to use once you get the hang of it.

#### 1: Access The Command Line

> Different operating systems access the command line in different ways.  
> 
> **Windows**:
> 
> - Press `Win` (or `Win` + `R`) to open the "Run" dialog bar.
> - Type `cmd` & press `Enter/Return` to open the Command Prompt.
> 
> **Mac**:
> 
> - Press `Command` + `Spacebar` to open the Finder.
> - Type `Terminal` into the Finder.
> - Select the Terminal application from the list of search results.

#### 2: Check To See If Python Is Already Installed On Your Computer 

> To perform this check:
> 
> - Type `python --version` - into the command line.
> - Press `Enter/Return`.
> 
> If Python is installed on your computer, you'll see a version number displayed on your screen. (On my Macbook, this command currently outputs `Python 3.11.4`.)  
> 
> If Python isn't installed on your computer, you'll see an error message.

#### 3: Install Python

> If Python isn't installed on your computer, we can easily install it. 
> 
> **Windows**:
> 
> - Type `python` into the command line.
> - Click the "Get" icon after Windows opens the Python in the Microsoft Store.
> - Wait for Python to finish installing on your computer.
> - Repeat Step 2 to confirm Python was successfully installed.
> 
> **Mac**:
> 
> - Go to the Python website: https://www.python.org/downloads/.
> - Download "the latest version for macOS" by clicking on the "Download Python #.##.#" button.  (Currently "Download Python 3.11.4".)
> - Navigate to your `Downloads` folder.
> - Double-click on the downloaded package.
> - Follow the on-screen instructions to install Python.
> - Repeat Step 2 to confirm Python was successfully installed.

#### 4: Install Python Libraries

> Almost done setting up Python!  
> 
> Now we need to install the aforementioned Python libraries. 
> 
> - Copy & paste the code snippet below into the command line:
> 
> ```bash
> pip install spotipy beautifulsoup4 argparse inflection termcolor tqdm tabulate prettytable requests
> ```
>
> - Press `Enter/Return`.
>
> Don't panic if your computer starts printing a whole bunch of text on your screen.  You're not being hacked!  This is exactly how your computer should behave when installing new Python libraries. 


### III.  Download, Extract, & Move The `wprbify.py` Script 

As you probably noticed, WPRBify "lives" here on GitHub.  In order to properly configure & run WPRBify, thought, we need to download a copy of it onto your computer.

#### 1. Download The Script As A Zip file 

> Starting from WPRBify's GitHub repo (i.e. this webpage):
>
> - Scroll to the top of the script's GitHub repo/webpage.
> - Click on the green "<> Code" button (right-hand side of your browser window).
> - Select "Download ZIP". 
> 
> This will download the script's GitHub repo to your computer as a Zip file.

#### 2. Navigate To The Downloaded Zip File

> **Windows**:
>
> - Open Window's File Explorer.
> - Navigate to the downloaded Zip file.
>
> **Mac**:
>
> - Open Finder.
> - Navigate to the downloaded Zip file.
>
> The exact location your browser downloaded the Zip file to may vary, depending on your browser, browser settings, & operating system.  
>
> If you've customized your browser to download files to a specific folder, the downloaded Zip file will be there; otherwise, the downloaded Zip file can likely be found in your computer's `Downloads` folder. 
>
> If you're _really_ having trouble locating the downloaded Zip file, try searching your computer for: `wprbify-main.zip`.

#### 3. Extract The Zip File

>We now need to extract the WPRBify script from the downloaded Zip file.
> 
> **Windows**:
>
> - Right-click on `wprbify-main.zip`.
> - Select "Extract All".
> 
> **Mac**:
>
> - Double-click on `wprbify-main.zip`.
> 
> Once the downloaded Zip file has been "unzipped", you should see a new folder - `wprbify-main` - in your Finder / File Explorer window. 

#### 4. Move `wprbify.py` Into Your Documents Folder 

> To make it as easy as possible for us to configure & run WPRBify, we're going to move it into the `Documents` folder of your computer.
>
> **Windows**:
>
> - Double-click on the `wprbify-main` folder to access its contents. 
> - Right-click on the `wprbify` Python file.
> - Hover over "Send To".
> - Select "Documents".
>
> **Mac**:
>
> - Double-click on the `wprbify` folder to access its contents. 
> - Click on the `wprbify.py` Python file.
> - Select "Edit" from the Finder menu bar (top of your Finder window).
> - Select "Copy 'wprbify.py'". 
> - Click on the "Documents" folder under "Favorites" (left-hand side of your Finder window) to open the `Documents` folder.
> - Select "Edit" from the Finder menu bar (top of your Finder window).
> - Select "Paste".
 

### IV.  Configuring The WPRB Playlist Script

Now that we've downloaded WPRBify to computer & moved it into your `Documents` folder, we need to configure it so it will run properly.

#### 1. Open The Script In A Text Editor

> To configure the script, we first need to open it in a text editor.  To keep things simple, we're going to use whichever basic text editor came pre-installed on your computer.
>
> **Windows**:
> 
> - Navigate to the `Documents` folder in File Explorer.
> - Right-click on the `wprbify` Python file.
> - Select "Open With".
> - Select "Notepad".
> 
> **Mac**:
> 
> - Navigate to the `Documents` folder in Finder.
> - Click on `wprbify.py`.
> - Select "File" from the Finder menu bar (top of your Finder window).
> - Click on "Open With".
> - Select "TextEdit".
 
#### 2. Add Your Spotify API Credentials To The Script

> To access Spotify's API & interact with your Spotify account, we need to add your unique Spotify API credentials (i.e. your Client ID & Client Secret) to WPRBify. 
> 
> - Find these lines of code in the script:
> 
> ```python
> # Spotify API credentials
> CLIENT_ID = "YOUR_CLIENT_ID"
> CLIENT_SECRET = "YOUR_CLIENT_SECRET"
> ```
> 
> - Replace `YOUR_CLIENT_ID` with the Client ID we copied-and-pasted into a new document in Step I.4.
> - Replace `YOUR_CLIENT_SECRET` with the Client secret we copied-and-pasted into an new document in Step I.4.
> - Confirm you didn't delete the quotation marks (`""`) while updating the script.
> - Confirm there are no spaces separating the quotation marks (`""`) from your Client ID & Client secret.

#### 3. Add An Output File Path To The Script

> After it successfully runs, WPRBify outputs a text file containing any WPRB playlists tracks not included in the generated Spotify playlist.  
> 
>  Now we're going to configure the script so that this text file is output to the `Documents` folder on your computer.
> 
> - Find these lines of code in the script: 
> 
> ```python
> # Set the output file path for text file containing tracks not found on Spotify.
> OUTPUT_FILE_PATH = "YOUR_OUTPUT_FILE_PATH"
> ```
> 
> **Windows**:
> 
> - Replace `YOUR_OUTPUT_FILE_PATH` with `\\Users\\username\\Documents\\` where `username` is your Windows user name.  
>
> **Mac**:
>
> - Replace `YOUR_OUTPUT_FILE_PATH` with `/Users/username/Documents/` where `username` is your Mac user name.
>
> If you're unsure what your Windows or Mac user name is, it's very easy to look it up:
> 
> - Open the Command Prompt / Terminal.
> - Type `whoami` into the command line.  
> 
> Your Windows or Mac user name will appear on the screen.  

#### 4. Save The Updated Script 

> Now that we've updated the script, we need to save our updates.
> 
> **Windows & Mac**:
> 
> - Click on "File".
> - Select "Save".


### V.  Run WPRBify 

_Maith thú!_  Now it's (finally) time to fire up WPRBify & create our first Spotify playlist! 

####    1.  Open Spotify.

> It's _very important_ Spotify is open & running on your computer the first time you run WPRBify.  
> 
> - If Spotify isn't already open on your computer, go ahead & open it now.  

####  2.  Navigate To A WPRB Playlist & Copy Its URL

> To generate a Spotify playlist from a WPRB playlist, we need a WPRB playlist's URL.  
>
> - Open your browser & navigate to the [WPRB broadcast calendar](https://playlists.wprb.com/WPRB/calendar). 
> - Click on any past broadcast to open its playlist.  
> - Navigate to the URL address bar (the _very_ top of your browser window, where you type in web addresses).
> - Double-click on the playlist's URL (i.e. the string of text beginning `https://playlists.wprb.com`) to select/highlight it.
> - Right click on the highlighted URL & select "Copy".

####  3.  Navigate To Your Updated Script On The Command Line

> **Windows**:
>
> - Open the Command Prompt.
> - Type `cd \Users\username\Documents` into the command line, replacing `username` with your Windows user name. 
> - Press `Enter`.  
>
> **Mac**:
>
> - Open the Terminal.
> - Type `cd ~/Documents` into the command line.

####  4.  Run The Updated Script From The Command Line 

> - **Confirm Spotify is open on your computer.**
> - **Confirm that you've successfully logged into your Spotify account**.
> - Type `python wprbify.py`, followed by a single `<SPACE>`, into the command line.
> - Click into the Command Prompt (Windows) or Terminal (Mac) using your mouse.
>
> **Windows**:
> - Right click in the Command Prompt.
> - Select "Paste".  
>
> **Mac**:
> - Select "Edit" from the Terminal menu bar. 
> - Click "Paste". 
> 
> This should paste the WPRB playlist URL we selected & copied in Step IV.2 into the command line. 
>
> - Press `<SPACE>`.
> - Type `"PLAYLIST_NAME"` into the command line, replacing `PLAYLIST_NAME` with the name of your playlist.  Don't forget to confirm that your playlist name is enclosed in quotation marks (`""`)! 
> - Hit `Enter/Return`.
> 
> To illustrate:
> 
> If your selected & copied WPRB playlist URL is: 
>
> `https://playlists.wprb.com/WPRB/pl/17691402/Intergalactic-Pool-Party`
> 
>
> And the name you've chosen for your Spotify playlist is: 
>
> Help I'm Trapped In The Mall!
> 
>
> Then what you should type into the command line is: 
> 
> ```bash
> python wprbify.py https://playlists.wprb.com/WPRB/pl/17691402/Intergalactic-Pool-Party "Help I'm Trapped In The Mall"
> ```

####  5.  Authorize The Updated Script 

> When you run WPRBify for the first time, it will prompt you to log in to Spotify & grant it permission to modify your Spotify account. 
>
> - Follow the on-screen instructions to complete the authorization process.

#### 6.  Generate Your First Spotify Playlist

> Once you've authorized WPRBify to access your Spotify account, it should immediately begin running on your command line!  
> 
> All you need to do now is sit back, watch the script generate your Spotify playlist, & provide your user input as needed. (See the [Overview](#overview) section above for more details about user input.) 
>
> Once WPRBify has finished running, your new Spotify playlist should be visible in your Spotify account.  
> 
> Additionally, if the script was unable to add any WPRB playlist tracks to your new Spotify playlist, a list of those tracks will be saved within your computer's `Documents` folder as `YOUR_PLAYLIST_NAME-not_in_spotify.txt`. 

_Comhghairdeas_!  🎉🎉🎉

You just downloaded, configured, & ran WPRBify!  

See?  I told you you didn't need a Computer Science degree to get this working on your computer.  Happy playlist creation & **LONG LIVE FREE-FORM COMMUNITY RADIO**!


## Nerd Stuff For Nerds

This section delves into the inner workings of the `wprbify.py` script. If you are familiar with programming concepts, Python, & APIs, I hope you'll find this section interesting!

Here, you'll find a detailed breakdown of:

- The Python libraries & modules WPRBify depends on to run properly.
- A detailed breakdown of the WPRBify's functions. 
- How WPRBify calculates the "similarity scores" which correlated WPRB playlist track data with Spotify search result data

### Dependencies 

#### Libraries 

This script utilizes the following Python libraries:

- `spotipy` [(docs)](https://spotipy.readthedocs.io): Provides a convenient interface to interact with Spotify's Web API. It allows the script to search for tracks, create playlists, & access other music-related information from your Spotify account.

- `beautifulsoup4` [(docs)](https://tedboy.github.io/bs4_doc/): A powerful library used for web scraping. It allows the script to extract track information from the HTML content of the WPRB playlist page or a locally saved HTML file.

- `inflection` [(docs)](https://inflection.readthedocs.io/en/latest/): A library that provides utilities for English word inflection. It is used to correctly format track names & artist names when searching for tracks on Spotify.

- `termcolor` [(docs)](https://pypi.org/project/termcolor/): Adds color to text output in the terminal, making it easier to distinguish different elements of the script's output.

- `tqdm` [(docs)](https://tqdm.github.io/): A fast & extensible library for progress bars. It is used to display progress bars during the track search process, making it more interactive & visually appealing.

- `tabulate` [(docs)](https://pypi.org/project/tabulate/): A library that helps to create ASCII tables. It is used to format the tabulated list of search results, making it easier for the user to review & select tracks from the command line.

- `prettytable` [(docs)](https://pypi.org/project/prettytable/): Another library for creating ASCII tables. It is used to generate a neatly formatted table of tracks that were not found in Spotify or were skipped during the search process.

- `requests` [(docs)](https://pypi.org/project/requests/): Used to send HTTP requests & handle responses. It is used in the web scraping process to fetch the HTML content of the WPRB playlist page.

These libraries must be installed on your machine in order for WPRBify to run properly.  You can install them in one go from the command line via:

```bash
pip install spotipy beautifulsoup4 argparse inflection termcolor tqdm tabulate prettytable requests
````

#### Modules

This script utilizies the following Python standard library modules:

- `argparse` [(docs)](https://docs.python.org/3/library/argparse.html): Makes it easy to write user-friendly command-line interfaces. Allows the script to accept input arguments, such as the WPRB playlist URL & the name of the new Spotify playlist, when running the script from the command line.

- `re` [(docs)](https://docs.python.org/3/library/re.html): Provides support for regular expressions, enabling efficiently pattern matching & text manipulation in strings.

- `shutil` [(docs)](https://docs.python.org/3/library/shutil.html): A collection of high-level file operations & file system utility functions, simplifying tasks like copying, moving, & deleting files & directories.

- `os` [(docs)](https://docs.python.org/3/library/os.html): Supplies a wide range of operating system-dependent functionalities, including file and directory management, process control, & environment variables access.


### Functions

In this section, we provide a comprehensive overview of the functions used in the WPRBify script. These functions serve as the building blocks of the script's functionality & work together to fetch track information, search for matching tracks on Spotify, calculate similarity scores, & create personalized Spotify playlists.

#### `extract_track_info(html_content)`

Extracts track information from the HTML content of the WPRB playlist.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `html_content`  | str        | The HTML content of the WPRB playlist.                |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `track_list`    | list       | A list of tuples containing track information.         |

#### `calculate_similarity(wprb_artist, wprb_song, wprb_album, spotify_artist, spotify_song, spotify_album)`

Calculates the similarity score between WPRB track data and Spotify track data.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `wprb_artist`   | str        | The artist name from WPRB track data.                  |
| `wprb_song`     | str        | The song name from WPRB track data.                    |
| `wprb_album`    | str        | The album name from WPRB track data.                   |
| `spotify_artist`| str        | The artist name from Spotify track data.               |
| `spotify_song`  | str        | The song name from Spotify track data.                 |
| `spotify_album` | str        | The album name from Spotify track data.                |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `similarity`    | int        | The similarity score between 0 and 100.                |

#### `spotify_song_search(sp, song_name)`

Performs a song-only search in Spotify.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `sp`            | spotipy.Spotify | The Spotify API object.                            |
| `song_name`     | str        | The song name to search for.                           |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `search_results`| list       | A list of search results (tracks) from Spotify.        |

#### `wprb_search_results(wprb_artist, wprb_song, wprb_album)`

Searches for tracks in Spotify and calculates similarity.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `wprb_artist`   | str        | Artist name from WPRB.                                 |
| `wprb_song`     | str        | Song name from WPRB.                                   |
| `wprb_album`    | str        | Album name from WPRB.                                  |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `results`       | list       | A list of search results (tracks) from Spotify with similarity scores. |

#### `safe_input_int(prompt)`

Prompts for integer input, ensuring it is a valid number.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `prompt`        | str        | The prompt to display to the user.                     |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `choice`        | int        | The user's valid integer input.                        |

#### `create_spotify_playlist(sp, playlist_name, track_list)`

Creates a Spotify playlist and adds tracks to it.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `sp`            | spotipy.Spotify | The Spotify API object.                            |
| `playlist_name` | str        | The name of the playlist to be created.                |
| `track_list`    | list       | List of track data from the WPRB URL.                  |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| None            |            | This function does not return anything.                |

#### `get_track_uri(sp, artist, song)`

Searches for the track URI in Spotify based on artist and song.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `sp`            | spotipy.Spotify | The Spotify API object.                            |
| `artist`        | str        | The artist name.                                       |
| `song`          | str        | The song name.                                         |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `track_uri`     | str        | The Spotify track URI, or None if not found.           |

`search_with_search_q(artist, song)`

Performs a search using Spotipy's `search_q` method to find tracks with an exact match of artist and song.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `artist`        | str        | The artist name.                                       |
| `song`          | str        | The song name.                                         |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `search_results`| list       | A list of search results.                              |

`save_not_found_tracks(playlist_name, not_found_tracks)`

Saves the list of tracks not found in Spotify to a file.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `playlist_name` | str        | The name of the Spotify playlist.                      |
| `not_found_tracks`| list      | A list of tuples containing track data (song, artist). |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| None            |            | This function does not return anything.                |

`fetch_html_content(input_source)`

Fetches HTML content from a URL or file path.

| Parameters      | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `input_source`  | str        | The URL or file path of the HTML content.              |

| Returns         | Data Type  | Description                                            |
|-----------------|------------|--------------------------------------------------------|
| `html_content`  | str        | The HTML content fetched from the URL or file.         |


### Similarity Score

The similarity score is a numerical value between 0 & 100 that indicates how closely the track data from the WPRB playlist matches the corresponding track data found on Spotify. The higher the similarity score, the closer the match between the two sets of track data.

The calculation of the similarity score involves the following steps: normalization, comparison, weight average calculation & final score generation.  The sub-sections below explain each step in greater & document the code associated with each step. 

#### Normalization

Both sets of track data are normalized by converting all text to lowercase & removing any special characters & punctuation. This step ensures that the comparison between the track data is case-insensitive & focuses solely on the alphanumeric content.

```python
   wprb_artist_normalized = re.sub(r'[^\w\s]', '', wprb_artist).lower()
   wprb_song_normalized = re.sub(r'[^\w\s]', '', wprb_song).lower()

   if wprb_album is not None:  # Check if album data is available
       wprb_album_normalized = re.sub(r'[^\w\s]', '', wprb_album).lower()
   else:
       wprb_album_normalized = None

   spotify_artist_normalized = re.sub(r'[^\w\s]', '', spotify_artist).lower()
   spotify_song_normalized = re.sub(r'[^\w\s]', '', spotify_song).lower()
   spotify_album_normalized = re.sub(r'[^\w\s]', '', spotify_album).lower()
```

#### Comparison 

The normalized artist name, song name, & album name (if available) from the WPRB playlist are compared with the corresponding data from Spotify using the SequenceMatcher algorithm from the difflib library. SequenceMatcher computes a similarity ratio between two strings, indicating how similar they are. The higher the ratio, the more similar the strings.

```python
artist_match = SequenceMatcher(None, wprb_artist_normalized, spotify_artist_normalized).ratio()
song_match = SequenceMatcher(None, wprb_song_normalized, spotify_song_normalized).ratio()
album_match = SequenceMatcher(None, wprb_album_normalized, spotify_album_normalized).ratio() if wprb_album_normalized else 0
```

#### Weighted Average

The similarity scores for the artist, song, & album data are combined into a weighted average to compute the final similarity score. The weights used are 1 for artist & song & 2 for the album. This is done to give more importance to the album match if available. For example, if the album name is available, a perfect match on the album name will have a larger impact on the final score compared to a perfect match on the artist or song name alone.

```python
similarity = int(min((artist_match + song_match + album_match * 2) / 3 * 100, 100))
```

#### Final Score

The final similarity score is capped at a maximum of 100 to ensure that it falls within the desired range. A similarity score of 100 indicates a perfect match between the WPRB track data & the corresponding track data on Spotify.

```python
return similarity
```
### Bug Reports & Pull Requests

If you encounter any issues with the script or would like to contribute improvements, please open a GitHub issue or submit a pull request.

