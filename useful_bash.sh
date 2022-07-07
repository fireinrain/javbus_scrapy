#!/usr/bin/env sh

# shellcheck disable=SC2028
echo "\n\r"
echo "----------------actresses----------------"

wc -l ./data_store/actresses/censored_star_2022-07-08.csv
wc -l ./data_store/actresses/uncensored_star_2022-07-08.csv

echo "----------------starinfo----------------"
wc -l ./data_store/starinfo/censored_starinfo_2022-07-08.csv
wc -l ./data_store/starinfo/uncensored_starinfo_2022-07-08.csv

echo "---------------stariteminfo-----------------"
wc -l ./data_store/stariteminfo/censored_staritem_2022-07-08.csv
wc -l ./data_store/stariteminfo/uncensored_staritem_2022-07-08.csv
