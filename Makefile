.PHONY: test lint

VENV := .venv/bin/python

test:
	$(VENV) -m unittest discover -s tests -v

lint:
	$(VENV) -m black --check pipeline.py scripts/ tests/
	$(VENV) -m py_compile pipeline.py
	@for f in scripts/*.py scripts/ocr/*.py; do $(VENV) -m py_compile "$$f"; done
	@echo "All files compile clean."

fmt:
	$(VENV) -m black pipeline.py scripts/ tests/
