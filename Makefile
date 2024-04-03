.PHONY: all clean venv deps runserver

VENV := venv
ACTIVATE_VENV := . $(VENV)/bin/activate

all: clean venv deps loadenv migrate

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@echo "Removed virtual environment."

venv:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV)
	@echo "Virtual environment created."

deps:
	@echo "Installing dependencies..."
	@$(ACTIVATE_VENV) && pip install --upgrade poetry
	@$(ACTIVATE_VENV) && poetry install --no-cache
	@echo "Dependencies installed."

loadenv:
	@echo "[+] Loading Environment Variables from .env"
	@while IFS= read -r line; do \
		if [[ ! "$$line" =~ ^\# && -n "$$line" ]]; then \
			export $$line; \
		fi; \
	done < ".env"

runserver:
	@$(ACTIVATE_VENV) && python main/manage.py runserver

makemigrations:
	@$(ACTIVATE_VENV) && python main/manage.py makemigrations

migrate:
	@$(ACTIVATE_VENV) && python main/manage.py migrate
