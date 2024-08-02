Goose bot built on telegram


# Quick Start
## Setup
install dependencies, on terminal:
```sh
python3 -m venv venv
pip install poetry
poetry install
```
set up .env
```
TELEGRAM_BOT_TOKEN=<telegrambot token>
OPENAI_API_KEY=<openai key, starts with 'sk'>
```
to start the server:
```py
python3 app.py
```

# Development

quick lint
```sh
sh scripts/lint.sh
```
thorough linting report
```sh
sh scripts/lint.sh --check
```