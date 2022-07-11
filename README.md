## Telegram bot that restricts writers on behalf of the channel for the "Sariqdevchat" group
___
### Create and Activate Environment on Linux
```bash
python3 -m venv env
source env/bin/activate
```
___
### Create and Activate Environment on Windows
```bash
python -m venv env
env\Scripts\activate
```
___
### Installation pip packages
```bash
pip install -r requirements
```
___
### Create a file named ".env" and write the following inside it
```
BOT_TOKEN = "TOKEN"
BOT_USERNAME = 'BOT_USERNAME'
GROUP_USERNAME = "sariqdevchat"
PRIME_CHANNEL = 'sariqdev'
DEVELOPER_CHAT_ID = ...
```
___
### Execute database
```bash
python manage.py makemigrations
python manage.py migrate
```
___
### Run Django Part (run on the server with gunicorn)
```bash
python manage.py runserver
```
___
### Run Telegram Bot
```bash
python manage.py bot
```
___
### python version 3.9.12
___
### Developed by ["leader_0114"](https://t.me/leader_0114)
___