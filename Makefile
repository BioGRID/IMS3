
# Version Numbers, generally to be passed to RPMBUILD
VERSION:=0.2
RELEASE:=1

# Organize phoney Targets
CLEANING_T:=ims3clean mostlyclean clean distclean
PYTHON_T:=python-rpms
DB_T:=ims3 ims3clean
.PHONY: distclean rpms dist $(CLEANING_T) $(PYTHON_T) $(DB_T)

# Paths to this or that
PYTHONPATH:=python
IMS_CONFIG:=./ims.json
SQL_DIR:=./sql
RPMDIR:=rpmbuild

# Commands
IMS22IMS3=PYTHONPATH=$(PYTHONPATH) $(PYTHONPATH)/ims22ims3 --config=$(IMS_CONFIG) --sql-dir=$(SQL_DIR)
RPMBUILD=rpmbuild --define '_topdir $(CURDIR)/$(RPMDIR)' \
	--define '%version $(VERSION)' \
	--define '%release $(RELEASE)' \
	--define 'ims_wwwdir /var/www/html/ims' \
	--define 'ims_phpdir /usr/share/php/ims'
# /var/www and /usr/share/php gotta be defined is some RPM macro
# someplace!

# To generate an IMS3 RPM file
DIST_NAME:=BioGRID-IMS3
DIR_NAME=${DIST_NAME}-${VERSION}
TAR_FILE=${DIR_NAME}.tar.gz
RPM_FILE=${DIR_NAME}-${RELEASE}.noarch.rpm
SPEC=$(DIST_NAME).spec
MANIFEST=README Makefile ims.json-template $(SPEC) www
DIST_FILES=$(foreach MAN,$(MANIFEST),$(DIR_NAME)/$(MAN))

VERSION_PHP=www/ims/version.php

$(VERSION_PHP): Makefile
	echo -e '<?php\ndefine("IMS3_VERSION","${VERSION}-${RELEASE}");' > $@


# Creates python and IMS3 rpms.
rpms: python-rpms rpm

rpm: $(RPM_FILE)

# Create IMS3 RPM file
$(RPM_FILE): $(TAR_FILE)
	$(RPMBUILD) --target=noarch -tb $<
	mv $(RPMDIR)/RPMS/noarch/$@ $@

# Pass making python RPM file to python
python-rpms: $(PYTHONPATH)/sql
	(cd $(PYTHONPATH); python setup.py bdist_rpm)
	mv $(PYTHONPATH)/dist/*.rpm .

# Port the IMS2 database to the IMS3 database
ims3:
	$(IMS22IMS3)

# This should wipe out the IMS3 database, so use wisely
ims3clean:
	$(IMS22IMS3) --clean

# Copy the sql directory into the python directory so it can be
# included in the python RPM
$(PYTHONPATH)/sql: sql
	mkdir $@
	cp $</*.sql $@

# Well, doesn't include SQL or python stuff
dist: $(TAR_FILE)

# Create a tar file with with RPM spec file it it to easily create
# ims3 rpm.
$(TAR_FILE): ${DIR_NAME} ${SPEC} ${VERSION_PHP}
	tar -zcvf $@ --exclude=*~ $(DIST_FILES)


# Create a link to ourself with the name we want the tar file to be.
${DIR_NAME}:
	ln -s . ${DIR_NAME}



mostlyclean:
	$(RM) $(TAR_FILE)
	$(RM) -r $(PYTHONPATH)/sql
	(cd $(PYTHONPATH); python setup.py clean)

clean: mostlyclean
	$(RM) -r $(PYTHONPATH)/build $(PYTHONPATH)/dist ${RPMDIR}
	$(RM) *.rpm $(PYTHONPATH)/MANIFEST $(DIR_NAME) $(VERSION_PHP)

distclean: clean
	find $(PYTHONPATH)/BioGRID -name \*.pyc | xargs $(RM)
