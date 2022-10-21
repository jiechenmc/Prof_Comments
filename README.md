# Prof Comments and Grades

## Will not work anymore after Heroku retires free tier :(

RESTful API for comments and grade distribution data from SBUClassieEval

## Easily spin up a dev session with

#### Docker
```bash
docker compose up
```
#### Python
```bash
pip install -r requirements.txt
uvicorn app:app
```

## Scraping data locally 
- To scrape, create a .env file that looks like the example.env with fields filled in.
- Visit the scripts/scrape folder for more info
- Altough the file is called scrape_comments, it scrapes grade distribution data as well!
```bash
python scrape_routes.py ...
python scrape_comments.py ...
```

##### For documentations please visit: https://prof-comments.herokuapp.com/docs
