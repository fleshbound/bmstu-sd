#!/bin/bash

reset_db() {
  make main
}

if [ -f ./res_no_index.txt ]; then
    rm ./res_no_index.txt
fi
touch ./res_no_index.txt

for (( i=0; i < 180000; i=i+10000 )); do
    reset_db
    PGPASSWORD=$(cat .env | grep DB_PWD= | cut -f2 -d"=") psql -h $(cat .env | grep DB_HOST= | cut -f2 -d"=") -p $(cat .env | grep DB_PORT= | cut -f2 -d"=") -d $(cat .env | grep DB_NAME= | cut -f2 -d"=") -U $(cat .env | grep DB_USER= | cut -f2 -d"=") --command "COPY \"user\"(email, hashed_password, role, name) from '/home/sheglar/bmstu/petowo/db/internal/database/data/test_data/${i}.csv' delimiter ';' csv header;"
    for (( j=0; j <= 30; j++ )); do
        echo "i=${i}; j=${j}"
        val=$(echo "EXPLAIN ANALYZE select * from postgres.public.\"user\" order by name;" | LANG=C PGPASSWORD=$(cat .env | grep DB_PWD= | cut -f2 -d"=")  psql  -h $(cat .env | grep DB_HOST= | cut -f2 -d"=") -p $(cat .env | grep DB_PORT= | cut -f2 -d"=") -d $(cat .env | grep DB_NAME= | cut -f2 -d"=") -U $(cat .env | grep DB_USER= | cut -f2 -d"="))
        val1=$(echo $val| tr ' ' '\n' | tail -4 | tr '\n' ' ' | cut -f 1 -d ' ')
        val2=$(echo $val| tr ' ' '\n' | tail -10 | tr '\n' ' ' | cut -f 3 -d ' ')
        res=$(echo "$val1+$val2" | bc)
        echo $res > ./res_no_index.txt
    done
done

if [ -f ./res_index.txt ]; then
    rm ./res_index.txt
fi
touch ./res_index.txt

for (( i=0; i < 180000; i=i+10000 )); do
    reset_db
    PGPASSWORD=$(cat .env | grep DB_PWD= | cut -f2 -d"=") psql  -h $(cat .env | grep DB_HOST= | cut -f2 -d"=") -p $(cat .env | grep DB_PORT= | cut -f2 -d"=") -d $(cat .env | grep DB_NAME= | cut -f2 -d"=") -U $(cat .env | grep DB_USER= | cut -f2 -d"=") --command "create index ix_user_name ON postgres.public.\"user\" (name);"
    PGPASSWORD=$(cat .env | grep DB_PWD= | cut -f2 -d"=") psql  -h $(cat .env | grep DB_HOST= | cut -f2 -d"=") -p $(cat .env | grep DB_PORT= | cut -f2 -d"=") -d $(cat .env | grep DB_NAME= | cut -f2 -d"=") -U $(cat .env | grep DB_USER= | cut -f2 -d"=") --command "COPY \"user\"(email, hashed_password, role, name) from '/home/sheglar/bmstu/petowo/db/internal/database/data/test_data/${i}.csv' delimiter ';' csv header;"
    for (( j=0; j <= 30; j++ )); do
        echo "i=${i}; j=${j}"
        val=$(echo "EXPLAIN ANALYZE select * from postgres.public.\"user\" order by name;" | LANG=C PGPASSWORD=$(cat .env | grep DB_PWD= | cut -f2 -d"=")  psql  -h $(cat .env | grep DB_HOST= | cut -f2 -d"=") -p $(cat .env | grep DB_PORT= | cut -f2 -d"=") -d $(cat .env | grep DB_NAME= | cut -f2 -d"=") -U $(cat .env | grep DB_USER= | cut -f2 -d"="))
        val1=$(echo $val| tr ' ' '\n' | tail -4 | tr '\n' ' ' | cut -f 1 -d ' ')
        val2=$(echo $val| tr ' ' '\n' | tail -10 | tr '\n' ' ' | cut -f 3 -d ' ')
        res=$(echo "$val1+$val2" | bc)
        echo $res > ./res_index.txt
    done
done
