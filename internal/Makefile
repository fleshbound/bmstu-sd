test_core:
	pytest ./tests/core/ -v

test_repo:
	pytest ./tests/repository/ -v

set_test_db:
	cd ./database/py &&	python3 setdb.py test info 2000

set_test_db_empty:
	cd ./database/py &&	python3 setdb.py test

main:
	cd ./database/py &&	python3 setdb.py main

tmp_10:
	cd ./database/py && python3 setdb.py 10
	sudo cp ./database/data/*.csv /tmp
	cd ./database/py && python3 setdb.py copy

all:
	cd ./database/py &&	python3 setdb.py all

test_user_data:
	cd ./database/py &&	python3 setdb.py
