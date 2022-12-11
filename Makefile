install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py

test:
	python -m unittest test_csv_combiner.py

all: install lint test