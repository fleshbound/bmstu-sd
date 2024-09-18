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

all:
	cd ./database/py &&	python3 setdb.py all

test_user_data:
	cd ./database/py &&	python3 setdb.py
