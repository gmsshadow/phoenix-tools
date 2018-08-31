read -p 'Search Term: ' searchvar
read -p 'Day: ' dayvar

grep -i $searchvar -R /home/barry/phoenix-tools/data/positions/$dayvar/ > $dayvar-$searchvar.txt
