PYTHON := python

.PHONY: all lint test build docs
all:
	@echo "Running cross-platform 'all' target..."
	@echo "On Windows use the PowerShell helper: .\\scripts\\makeall.ps1"
	@if [ -x "$(shell command -v sh 2>/dev/null)" ]; then \
		sh scripts/makeall.sh || true; \
	else \
		echo "No shell detected; on Windows run: powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\makeall.ps1"; \
	fi

lint:
	$(PYTHON) -m ruff check src || true

test:
	$(PYTHON) -m pytest -q || true

build:
	$(PYTHON) -m build || true

docs:
	mkdocs build || true
