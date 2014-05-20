IMS_CONFIG=./ims.json
SQL_DIR=./sql

PYTHONPATH=python
IMS22IMS3=PYTHONPATH=$(PYTHONPATH) $(PYTHONPATH)/ims22ims3 --config=$(IMS_CONFIG) --sql-dir=$(SQL_DIR)

CLEANING=ims3clean mostlyclean clean distclean
.PHONY:ims3 ims3clean distclean rpms $(CLEANING)

ims3:
	$(IMS22IMS3)

$(PYTHONPATH)/sql: sql
	mkdir $@
	cp $</*.sql $@

python-rpms: $(PYTHONPATH)/sql
	(cd $(PYTHONPATH); python setup.py bdist_rpm)
	mv $(PYTHONPATH)/dist/*.rpm .

rpms: python-rpms


# This should wipe out the IMS3 database, so use wisely
ims3clean:
	$(IMS22IMS3) --clean

mostlyclean:
	$(RM) -r $(PYTHONPATH)/sql
	(cd $(PYTHONPATH); python setup.py clean)

clean: mostlyclean
	$(RM) -r $(PYTHONPATH)/build $(PYTHONPATH)/dist 
	$(RM) *.rpm $(PYTHONPATH)/MANIFEST

distclean: clean
	find $(PYTHONPATH)/BioGRID -name \*.pyc | xargs $(RM)
