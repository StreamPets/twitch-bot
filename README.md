# StreamPets Twitch Bot

## Installation

### Clone the repository
```bash
git clone git@github.com:StreamPets/twitch-bot.git
cd twitch-bot
```

### Create virtual environment
On Windows and MacOS:
```bash
python -m venv venv
```
On Linux:
```bash
python3 -m venv venv
```

### Activate the virtual environment
On Linux and MacOS:
```bash
source venv/bin/activate
```
On Windows:
```bash
./venv/Scripts/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Create .env file
```
BOT_TOKEN=<your bot oauth token>
API_URL=http://localhost:<port>
```

#### Bot Token
An OAuth token from your bot's account.

#### API URL
The URL of the StreamPets Backend instance.
You can clone and run it from [here](https://github.com/StreamPets/backend).

## Usage

To run the bot:
```bash
python main.py
```
