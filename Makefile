reverse = $(if $(1),$(call reverse,$(wordlist 2,$(words $(1)),$(1)))) $(firstword $(1))

PYTHON_PREFIX=./python
SQL_DIR=./sql
PYTHON=PYTHONPATH=$(PYTHON_PREFIX) python
IMS_CONFIG=ims.json

.PHONY:python ims3

IMS2=$(PYTHON) -m BioGRID.ims2 --conf=$(IMS_CONFIG) --sql=$(SQL_DIR)

INTERACTION_TABLES=Interaction_source Interaction_quantitation_type
PART_TABLES=Participant
#IPLEX_TABLES=Iplex_project
USER_TABLES=Project User Project_user
PTM_TABLES=PTM_source PTM_modification
PUB_TABLES=Publication_query Publication Project_publication


TABLE_DEPENDS=$(USER_TABLES) $(INTERACTION_TABLES) $(PUB_TABLES) \
	$(PTM_TABLES) $(PART_TABLES)
TABLE_RDEPENDS=$(call reverse,$(TABLE_DEPENDS))

ims3:
	$(IMS2) $(TABLE_DEPENDS)

clean:
	$(IMS2) --clean $(TABLE_RDEPENDS)

distclean:
	find $(PYTHON_PREFIX) -name \*.pyc | xargs $(RM)

python:
	$(PYTHON)
