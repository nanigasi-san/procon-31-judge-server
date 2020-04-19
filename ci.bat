pytest -vv --cov=src --cov-report=html:tests/reports --junit-xml=tests/results/results.xml > nul
flake8 src tests > nul
mypy src > nul