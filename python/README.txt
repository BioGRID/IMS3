* ims22ims3
There are likely bugs in this code.

** /etc/ims.json
The is the default location, another location can be specified with
the --config option.

*** dbs

This is the only section used by ims22ims3, the others may be used by
the actual web site.  Edit this to specify which databases, user
names, and passwords you wish to access MySQL with.  Please edit this
away from the 'sven' database.

** Usage
ims22ims3 --help for summary.

*** IMS2 to IMS3
Once ims.json in configured there are three stages to importing IMS2
to IMS3 schema:

$ ims22ims3 --stage=1
$ ims22ims3 --stage=2
$ ims22ims3 --stage=3

(when all stages are done from one process, it died before being
finished.)  This entire procedure takes about two hours on the test
server.  Once a stage as started, it needs to be cleaned before it can
be restarted.

*** Cleaning
Due to database relations, cleaning must be done in the reverse order:

$ ims22ims3 --stage=3 --clean
$ ims22ims3 --stage=2 --clean
$ ims22ims3 --stage=1 --clean
