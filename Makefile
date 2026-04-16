setup:
	python -m pip install -U pytest

check:
	python -m pytest

show-tree:
	@find . -maxdepth 3 -type f | sort
