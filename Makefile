up:
	. venv/bin/activate; python services/accounts.py &
	. venv/bin/activate; python services/catalog.py &
	. venv/bin/activate; python services/payments.py &
	. venv/bin/activate; python services/customers.py &
	. venv/bin/activate; python services/orchestrator.py &
	. venv/bin/activate; python client.py &


down:
	ps -ef | grep "services/accounts.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/catalog.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/payments.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/customers.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/orchestrator.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "client.py" | grep -v grep | awk '{print $$2}' | xargs kill
