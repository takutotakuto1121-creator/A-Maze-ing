VENV = .venv
BIN = $(VENV)/bin
FLAKE8 = flake8
MYPY = mypy

.PHONY: install run debug clean fclean lint lint-strict

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(BIN)/pip install -r requirements.txt

run: $(VENV) install
	$(BIN)/python3 a_maze_ing.py config.txt

debug: $(VENV) install
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

lint: $(VENV) install
	$(BIN)/$(FLAKE8) mazegen a_maze_ing.py
	$(BIN)/$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs mazegen a_maze_ing.py

lint-strict: $(VENV) install
	$(BIN)/$(FLAKE8) mazegen a_maze_ing.py
	$(BIN)/$(MYPY) --strict mazegen a_maze_ing.py
