# Restarts the scraping process every 30 minutes
# watch -n 1800 ./scrape.sh
LINE=$(cat data/comments.tsv | wc -l)
LINE=$(( $LINE + 1 ))

# Running the Python file
python scrape_comments.py $LINE