LINE=$(cat ./_comments.tsv | wc -l)
LINE=$(( $LINE + 1 ))

# Running the Python file
now=$(date "+%H:%M")
expire=$(date -d "$now 30 minutes" +'%H:%M' )
echo "Duo OAuth expires in about 30 minutes!"
echo "Session started at:\t\t $now\nDuo Token Expires in 30 minutes: $expire\n"
python scrape_comments.py $LINE