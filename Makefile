VENV := venv
HTTP_PORT := 8000


setup:
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

build: $(VENV)/bin/activate

run: build
	$(VENV)/bin/uvicorn app:app --host 0.0.0.0 --port $(HTTP_PORT)

test: build
	$(VENV)/bin/uvicorn app:app --host 0.0.0.0 --port $(HTTP_PORT) &
	$(VENV)/bin/uvicorn app:demo_endpoint_app --host 0.0.0.0 --port 5000 &
	PYTHONPATH=. $(VENV)/bin/python3 app/test.py &
	$(VENV)/bin/python3 app/integration_test.py &


clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete


.PHONY: setup build run test clean
