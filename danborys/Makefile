PYTHON = python3
PIP = pip
ENV = uv
MAIN = a_maze_ing.py
ENV_NAME = venv
MAIN = srcs.maze_generator.a_maze_ing
CONFIG = srcs/maze_generator/config.txt
WORK_DIR = srcs
ALL_CACHE = $(shell find . -path "./.venv" -prune -o -name "__pycache__" -print -o -name ".mypy_cache" -print)
VENV_PATH = $(shell find . -type d -name ".$(ENV_NAME)" -print)

install:
	@if [ -d ".$(ENV_NAME)" ]; then \
		echo "venv already exists"; \
	else \
		echo "Creating virtual environment..."; \
		$(ENV) $(ENV_NAME); \
		if [ -f "$(pyproject.toml)"]; then \
			echo "Installing dependencies..."; \
			$(ENV) $(PIP) install -r pyproject.toml; \
		else \
			echo "pyproject.toml file missing"; \
			echo "skipping package installation"; \
		fi; \
	fi
	

run:
	@if [ ! -d ".$(ENV_NAME)" ]; then \
		$(MAKE) install; \
	else \
		echo $(ENV) run $(PYTHON) -m  $(MAIN) $(CONFIG); \
		$(ENV) run $(PYTHON) -m  $(MAIN) $(CONFIG); \
	fi


clean:
	@if [ -n "$(ALL_CACHE)" ]; then \
		echo "Cleaning workspace..."; \
		for cache in $(ALL_CACHE); do \
			echo "Removing $$cache"; \
			rm -rf "$$cache"; \
		done; \
		echo "Workspace cleaned"; \
	else \
		echo "Nothing to clean."; \
	fi

fclean: clean
	@if [ -n "$(VENV_PATH)" ]; then \
		echo "Removing virtual environment..."; \
		rm -rf "$(VENV_PATH)";\
		echo "Virtual environment removed"; \
	else \
		echo "There is no virtual environment";\
	fi

lint:
	flake8 $(WORK_DIR)
	mypy $(WORK_DIR) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 $(WORK_DIR)
	mypy $(WORK_DIR) --strict

.PHONY: install run debug clean fclean lint lint-strict