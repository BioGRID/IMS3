"""Stuff to convert IMS2 database schema to IMS3.  Hopefully this will
be the only files with IMS2 information in it."""
import BioGRID.ims
from time import strftime
import warnings

class Config(BioGRID.ims.Config):
    def ims2db(self):
        """Returns a MySQLdb pointer to the IMS2 database."""
        return self._db('ims2')

class Project(BioGRID.ims.Project):
    _rename={'project_addeddate':'project_timestamp'}

    def __getitem__(self,name):
        if 'project_status'==name:
            status=self.row[name]
            if('open'==status):
                return 'public'
            else:
                return 'private'
        return super(Project,self).__getitem__(name)

class User(BioGRID.ims.User):
    _rename={
        'user_password':'password',
        'user_cookie':'cookie',
        'user_email':'email',
        'user_lastaccess':'access_timestamp',
        'user_firstname':'first_name',
        'user_lastname':'last_name',
        'project_id':'current_project',
        }

    def __getitem__(self,name):
        """Overloaded to convert IMS3 names to IMS2 names."""
        if 'user_addeddate'==name:
            adddate=self.row['access_timestamp']
            if not(adddate):
                adddate=strftime("%Y-%m-%d %H:%M:%S")
            return adddate
        return super(User,self).__getitem__(name)

class Project_user(BioGRID.ims.Project_user):
    _rename={'project_user_addeddate':'project_users_timestamp'}
    def __getitem__(self,name):
        if 'project_user_status'==name:
            return 'inactive'
        return super(Project_user,self).__getitem__(name)
    def id(self):
        return None
    def store(self):
        try:
            return super(Project_user,self).store()
        except _mysql_exceptions.IntegrityError as x:
            if 0==str(x).count("REFERENCES `users` (`user_id`)"):
                raise
            else:
                warnings.warn('user_id %s not in users' % self['user_id'])

class Interaction_source(BioGRID.ims.Interaction_source):
    def id(self):
        return None

class Interaction_quantitation_type(BioGRID.ims.Interaction_quantitation_type):
    def __getitem__(self,name):
        if 'interaction_quantitation_type_addeddate'==name:
            return '%s %s' % (
                self.row['interaction_quantitation_type_date_added'],
                self.row['interaction_quantitation_type_time_added'])
        elif 'interaction_quantitation_type_status'==name:
            return 'active'
        return super(Interaction_quantitation_type,self).__getitem__(name)

# class Iplex_project(BioGRID.ims.Iplex_project):
#     _rename={'iplex_project_name':'iplex_name',
#              'iplex_project_description':'iplex_description',
#              'iplex_project_addeddate':'iplex_createddate',
#              'iplex_project_status':'iplex_status'}

class Publication(BioGRID.ims.Publication):
    _rename={'publication_addeddate':'publication_modified'}
    _use=['publication_pubmed_id','publication_addeddate']
    def __getitem(self,name):
        try:
            self._use.index(name)
            return super(Publication,self).__getitem__(name)
        except ValueError:
            # for most things we wast to populate this with NULLs,
            # will fill directly from PubMed.
            return None

class Publication_query(BioGRID.ims.Publication_query):
    _rename={'publication_query_value':'pubmed_query_value',
             'publication_query_addeddate':'pubmed_query_added_date',
             'publication_query_lastrun':'pubmed_query_last_run',
             'publication_query_type':'pubmed_query_type',
             'publication_query_status':'pubmed_query_status'}
    def id(self):
        """Overloaded because the table name is different between IMS2
        and IMS3."""
        return self.row['pubmed_query_id']
    

if __name__ == '__main__':
    import sys
    from optparse import OptionParser
    import MySQLdb.cursors
    import _mysql_exceptions
    p=OptionParser()
    p.add_option('-c','--config',metavar='JSON')
    p.add_option('-s','--sql-dir',metavar='PATH')
    p.add_option('--clean',action='store_true')
    (opts,jobs)=p.parse_args()
    
    cfg=Config(opts.config)
    BioGRID.ims._Table.config=cfg
    if not(opts.clean):
        ims2=cfg.ims2db() # not needed in --clean
    ims3=cfg.imsdb()

    for job in jobs:
        print 'starting %s' % job

        # First check for SQL files containing IMS3 schema
        file=open('%s/%s.sql' % (opts.sql_dir,job))
        if opts.clean:
            line=file.readline()
            while line:
                if line.startswith('CREATE TABLE'):
                    table=line.split(' ')[-1].strip("(\n")
                    try:
                        ims3.query('DROP TABLE %s' % table)
                    except _mysql_exceptions.OperationalError as(errno,msg):
                        if 1051==errno: # Unknown table
                            pass
                        else:
                            raise
                line=file.readline()
            file.close()


        else:
            sqls=file.read()
            file.close()
            # WARNING! Don't use ; is you comments in the SQL files!
            for sql in sqls.split(';'):
                try:
                    ims3.query(sql)
                except _mysql_exceptions.OperationalError as(errno,msg):
                    # We can skip this error
                    if 1065==errno: # Query was empty
                        pass
                    else:
                        raise

            c=ims2.cursor(MySQLdb.cursors.DictCursor)

            if 'Interaction_source'==job:
                c.execute('''SELECT tag_name AS interaction_source_name,
tag_added_date AS interaction_source_addeddate,
tag_status AS interaction_source_status
FROM tag_categories JOIN tags USING(tag_category_id)
WHERE tag_category_name='Source'
''')
            else:
                # there doesn't really seem to be secure way to have dynamic
                # table names
                if 'Interaction_quantitation_type'==job:
                    table_name=job.lower()
                elif 'Publication_query'==job:
                    table_name='pubmed_queries'
                else:
                    table_name='%ss' % job.lower()
                c.execute('SELECT * FROM %s' % table_name)


            raw=c.fetchone()
            Table=eval(job)
            while raw:
                cooked=Table(raw)
                cooked.store()
                raw=c.fetchone()
                ims3.commit()
