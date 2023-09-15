.PHONY: install backend frontend
install:
	pip install -e backend/.
	cd frontend && npm install

backend:
	uvicorn main:app --reload --port 3000 --host 0.0.0.0 --workers 1 --app-dir=./backend
frontend:
	cd frontend && gatsby develop --host 0.0.0.0

