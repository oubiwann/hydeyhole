VENV=.venv
ACT=./$(VENV)/bin/activate
REQS=requirements.txt

$(VENV):
	virtualenv $(VENV)

deps: $(VENV)
	@. $(ACT) && pip install -r $(REQS)

hy-shell: deps
	@. $(ACT) && hy

keys: deps
	@. $(ACT) && twistd hydeyhole keygen

start: clean
	@. $(ACT) && twistd hydeyhole

start-dev: deps clean
	@. $(ACT) && twistd -n hydeyhole

stop:
	@. $(ACT) && twistd hydeyhole stop

shell: deps
	make start &
	@sleep 3
	@. $(ACT) && twistd hydeyhole shell
	make stop

clean-venv:
	rm -rf $(VENV)

clean:
	@find . -name "*.pyc" -exec rm {} \;

clean-all: clean clean-venv
