.PHONY: install run debug clean lint lint-strict

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

FLAKE8 := $(shell if [ -f venv/bin/flake8 ]; then echo venv/bin/flake8; else echo flake8; fi)
MYPY := $(shell if [ -f venv/bin/mypy ]; then echo venv/bin/mypy; else echo mypy; fi)

lint:
	$(FLAKE8) mazegen a_maze_ing.py
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs mazegen a_maze_ing.py

lint-strict:
	$(FLAKE8) mazegen a_maze_ing.py
	$(MYPY) --strict mazegen a_maze_ing.py
