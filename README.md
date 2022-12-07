# PoroLobby

PoroLobby creates 5v5 Practice Tool with bots in League of Legends. This tool accesses League Client API.

## How to use

### Easy way

Video guide (deprecated):

[![Video guide](https://img.youtube.com/vi/EHd3vRVECLg/0.jpg)](https://www.youtube.com/watch?v=EHd3vRVECLg)

1. Download `PoroLobby.zip` file from Releases section.
2. Extract the archive and go to the extracted `PoroLobby` folder
2. Start League of Legends and log in
4. (Optional) Edit the configuration file `config.json`
3. Run the `porolobby.exe` - the lobby will be created and filled with medium bots or the ones from config
4. Start the game and ENJOY!

### Configuration

The configuration is stored in `config.json`. You can specify different config file using command line interface. For example: `porolobby.exe -c alternativeConfig.json`

## Installation (advanced)

### Prerequisities
- Python >= 3.10.0 (it might work with older versions)
- pipenv (`pip install pipenv`)

### Step by step
1. Clone this repo - `git clone https://github.com/LeagueOfPoro/PoroLobby.git`
2. Move to the directory -  `cd PoroLobby`
3. Install the Python virtual environment - `pipenv install`
4. (Optional) Edit the configuration file
5. Run the tool - `pipenv run python ./porolobby.py`

### Create EXE
1.  `pipenv install --dev`
2.  `pipenv run pyinstaller -F --icon=poro.ico ./main.py`

## Support my work
<a href='https://www.youtube.com/channel/UCwgpdTScSd788qILhLnyyyw/join' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://share.leagueofporo.com/yt_member.png' border='0' alt='Become a channel member on YouTube' />

## Disclaimer

This tool uses the official League Client API, and therfore the use of this tool should not be bannable by Riot Games. That said, League of Poro provides no guarantee whatsoever. Use at your own risk!

## License 

This tool is distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

## Endorsement

PoroLobby isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
