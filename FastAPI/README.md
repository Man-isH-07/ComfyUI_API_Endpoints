# FastAPI Backend

This backend handles:
- News fetching
- Prompt generation
- API endpoints for the application

## Setup

```bash
pip install -r requirements.txt
```

## If above gives error then do this : 

```bash
pip install uvicorn fastapi requests
```

```bash
pip install dateparser>=0.7.6
```

```bash
pip install beautifulsoup4>=4.9.1
```

```bash
pip install feedparser==6.0.10
```

```bash
pip install pygooglenews==0.1.2 --no-deps
```

## Running the application

```bash
uvicorn app.main:app --reload
```








