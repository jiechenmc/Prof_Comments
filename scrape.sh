# Restarts the scraping process every 20 minutes
while [ true ]
do
    LINE=$(cat data/comments.tsv | wc -l)
    LINE=$(( $LINE + 1 ))

    # Running the Python file
    python scrape_comments.py $LINE
    last_pid="$!"
    sleep 1200
    kill $last_pid

    if [[ $(cat data/comments.tsv | wc -l) -eq $(cat data/routes.tsv | wc -l) ]]
    then
        exit 0
    fi
done