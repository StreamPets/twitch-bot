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

## Run in Docker

### Clone the repository
```bash
git clone https://github.com/StreamPets/twitch-bot.git
cd twitch-bot
```
You can choose to build and run the file manually, or to use Docker Compose (recommended)

### Build and run manually
Build the image from the Dockerfile within the repository.
```
docker build -t twitch-bot .
```
then start the container
```
docker run -d -e BOT_TOKEN=<Twitch Bot OAuth Token> -e API_URL=<Streampets Backend URL> twitch-bot
```

### Docker Compose
Edit the environment variables in the docker compose file to contain the correct Bot Token and API URL, then start the container.
```
docker compose up -d
```