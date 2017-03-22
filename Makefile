up:
	. venv/bin/activate; python services/accounts/accounts.py &
	. venv/bin/activate; python services/catalog/catalog.py &
	. venv/bin/activate; python services/payments/payments.py &
	. venv/bin/activate; python services/customers/customers.py &
	. venv/bin/activate; python services/orchestrator/orchestrator.py &
	. venv/bin/activate; python client.py &

down:
	ps -ef | grep "services/accounts/accounts.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/catalog/catalog.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/payments/payments.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/customer/customers.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/orchestrator/orchestrator.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "client.py" | grep -v grep | awk '{print $$2}' | xargs kill
