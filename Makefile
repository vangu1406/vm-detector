install:
	#install commands
	pip install --upgrade pip &&\
	    pip install -r requirements.txt
format:
	#format code
lint:
	#flake8 or pylint
test:
	#test code
all: install lint test
