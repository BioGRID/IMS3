PYTHON_PREFIX=./python
SQL_DIR=./sql
PYTHON=PYTHONPATH=$(PYTHON_PREFIX) python
IMS_CONFIG=ims.json

.PHONY:python ims3

IMS2=$(PYTHON) -m BioGRID.ims2 --conf=$(IMS_CONFIG) --sql=$(SQL_DIR)
TABLE_DEPENDS=Project

ims3:
	$(IMS2) $(TABLE_DEPENDS)

clean:
	$(IMS2) --clean $(TABLE_DEPENDS)

#User

python:
	$(PYTHON)
