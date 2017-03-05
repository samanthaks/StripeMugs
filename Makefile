up:
	. venv/bin/activate; python services/accounts.py &
	. venv/bin/activate; python services/catalog.py &
	. venv/bin/activate; python client.py &

down:
	ps -ef | grep "services/accounts.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/catalog.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "client.py" | grep -v grep | awk '{print $$2}' | xargs kill
