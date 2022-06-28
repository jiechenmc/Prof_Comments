# Gather latest routes ...
echo -n "Term (Spring_2022): "; read term
echo -n "URL (https://classie-evals.stonybrook.edu/\?currentTerm\=1224\&page\=): "; read url 
echo -n  "LAST PAGE # (73): "; read last_page_number

echo -n "\nGathering latest routes...\n"
python scripts/scrape/scrape_routes.py $term $url $last_page_number

echo -n "\nGathering Comments...\n"
python scripts/scrape/scrape_comments.py ./routes.tsv ./data.tsv 1

echo -n "\nCreating data.json...\n"
python scripts/files/to_json.py ./data.tsv ./data.json

echo -n "\nCleanign up...\n"
rm -rf ./routes.tsv && rm -rf ./data.tsv

echo -n "\nInspect \`data.json\` before continuing..."

echo -n "\n Run \'python migrate.py\' to migrate..."