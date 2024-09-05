test_core:
	pytest ./tests/core/ -q

test_repo:
	pytest ./tests/repository/ -q

set_test_db:
	cd ./database/py &&	python3 setdb.py test info 2000

set_test_db_empty:
	cd ./database/py &&	python3 setdb.py test
