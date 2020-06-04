pytest -vv --cov=src --cov-report=html:tests/reports --junit-xml=tests/results/results.xml
flake8 src tests
mypy src