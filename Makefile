CWD="`pwd`"

clean:
	@find . -name "*.pyc" -delete

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

test: clean pep8 pep8_tests
	@echo "Running all tests..."
	@nosetests -s  --with-coverage --cover-inclusive --cover-package=tornado_virtuoso_client --tests=$(CWD)/tests/ --with-xunit

pep8:
	@echo "Checking source-code PEP8 compliance"
	@-pep8 $(CWD)/tornado_virtuoso_client/ --ignore=E501,E126,E127,E128

pep8_tests:
	@echo "Checking tests code PEP8 compliance"
	@-pep8 $(CWD)/tests/ --ignore=E501,E126,E127,E128
