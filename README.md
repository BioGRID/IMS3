# Inactive Repository
This project has been replaced by https://github.com/BioGRID/IMS and is maintained for legacy purposes only.

-----------------------------------

# Introduction
Source Code for future versions of BioGRID IMS, see:
       http://wiki.thebiogrid.org/doku.php/interaction_management_system
For now mainly concerned in porting the IMS2 database schema to the
IMS3 schema.

Get latest source from:
    https://github.com/BioGRID/IMS3

# Non RPM requirements
Currently jQUery, bootstrap, and select2 are required but not included
in the RPM and not available from default CentOS RPMs.  You will need
to specify where they are using the /etc/ims.json file.

I think jsTree is going to be required in the future too.

# /etc/ims.json
The main configuration file.  It can also be located ../ims.json
relative to the location if the ims.php file, but that is mainly for
developement.

Note, no comments are allowed in JSON files.

## title
Whet to display on the top of the IMS3 page

## dbs
Accessing databases.

### ims
The main database to read and write to.

### quick
Access database with constant information.

### ims2
Not needed after we sucefully update to the latest database.

## css
List of CSS files to be included. See non-RPM rqueires above.

## js
List of JavaScript files to be incuded.  See non-RPM rqueires above.

## pubmed_update
An ISO 8601 date. Publications that have been updated before this date
will be refreshed by queries to PubMed.

## expries
How long to let somebody be logged on.

## ontology_types
ontologies.ontology_name to array of
interaction_ontology_types.interaction_ontology_type_shortcode
entries.  If none specified defaults to ["P"].
