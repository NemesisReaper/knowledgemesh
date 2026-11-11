.PHONY: test api worker dashboard e2e compile check

PYTHON ?= .venv/Scripts/python.exe

test:
	$(PYTHON) -m pytest -v

e2e:
	$(PYTHON) -m pytest apps/api/tests/test_multinode_e2e.py -v

compile:
	$(PYTHON) -m compileall apps packages infrastructure

api:
	$(PYTHON) -m uvicorn knowmesh_api.main:app --host 127.0.0.1 --port 8000 --reload

dashboard:
	cd apps/dashboard && pnpm dev

