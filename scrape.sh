# Restarts the scraping process every 30 minutes
# watch -n 1800 ./scrape.sh
LINE=$(cat data/comments.tsv | wc -l)
LINE=$(( $LINE + 1 ))

# Running the Python file
now=$(date "+%H:%M")
expire=$(date -d "$now 30 minutes" +'%H:%M' )
echo "Duo OAuth expires in about 30 minutes!"
echo "Now:\t $now\nExpires: $expire\n"
python scrape_comments.py $LINE