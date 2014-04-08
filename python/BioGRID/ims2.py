
"""Stuff to convert IMS2 database schema to IMS3.  Hopefully this will
be the only files with IMS2 information in it."""
import json
import BioGRID.ims
from time import strftime
import warnings



PARTICIPANT_TYPE=1
DEFAULT_USER_ID=1

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

class Interaction(BioGRID.ims.Interaction):
    ignore_id=None
    
    def ims2_cursor(self):
        return self.config.ims2db().cursor(MySQLdb.cursors.DictCursor)
    def __init__(self,path='ims.json'):
        if None==self.ignore_id:
            c=self.ims2_cursor()
            c.execute('SELECT tag_category_id AS id FROM tag_categories WHERE tag_category_name=%s',
                      ('Ignore Interactions',));
            self.ignore_id=BioGRID.ims.fetch_one(c,'id');
            warnings.warn('Fetched ignore_id==%d' % self.ignore_id)
        return super(Interaction,self).__init__(path)
    def __getitem__(self,name):
        if 'interaction_status'==name:
            return 'normal'
        elif 'interaction_source_id'==name:
            return 1
        return super(Interaction,self).__getitem__(name)
    def store(self):
        try:
            return super(Interaction,self).store()
        except _mysql_exceptions.IntegrityError:
            c=self.ims2_cursor();
            c.execute('''SELECT publication_pubmed_id AS id FROM publications
WHERE publication_id=%s''',(self['publication_id'],))
            pmid=BioGRID.ims.fetch_one(c,'id');
            c.execute('''SELECT modification_type FROM interaction_matrix
WHERE interaction_id=%s''',(self.id(),))
            mod_type=BioGRID.ims.fetch_one(c,'modification_type')
            warnings.warn(
                'Skipping %s interaction_id=%d where pubmed_id=%s' %
                (mod_type,self.id(),pmid));

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
    _use=['publication_pubmed_id','publication_addeddate',
          'publication_status']
    def __getitem__(self,name):
        try:
            self._use.index(name)
            return super(Publication,self).__getitem__(name)
        except ValueError:
            # for most things we wast to populate this with NULLs,
            # will fill directly from PubMed.
            return None
    def store(self):
        try:
            pmid=int(self['publication_pubmed_id'])
        except ValueError:
            warnings.warn(
                'publication_id=%s skipped since PubmedID is %s' %
                (self.id(),self['publication_pubmed_id']))
            return
        if 0==pmid:
            warnings.warn(
                'publication_id=%s skipped since PubmedID is %d' %
                (self.id(),pmid))
        else:
            try:
                super(Publication,self).store()
            except _mysql_exceptions.IntegrityError:
                warnings.warn(
                    'Skipping dup entry where publication_pubmed_id=%d' % pmid)

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

class Project_publication(BioGRID.ims.Project_publication):
    """Make sure the Publicatin table is loaded before this!"""
    _rename={'project_publication_addeddate':'project_pubmed_timestamp',
             'project_publication_status':'project_pubmed_status',
             'publication_query_id':'pubmed_query_id'}
    def id(self):
        return self.row['project_pubmed_id']
    def __getitem__(self,name):
        if 'publication_id'==name:
            c=self.ims_cursor()
            pmid=self.row['pubmed_id']
            c.execute('SELECT publication_id FROM publications WHERE publication_pubmed_id=%s', (pmid,))
            pub_id=BioGRID.ims.fetch_one(c,'publication_id')
            if pub_id==None:
                # Insert a new pub into the publication table
                pub=Publication({'publication_pubmed_id':pmid,
                                 'publication_status':'active'})
                pub.store() # should publication id
                warnings.warn(
                    "Inserting PubMed ID %d into publications" % pmid)
                return pub.id()
            return pub_id

        out=super(Project_publication,self).__getitem__(name)
        if ('publication_query_id'==name)and(0==out):
            return None
        return out

class PTM(BioGRID.ims.PTM):
    _rename={'ptm_modification_id':'modification_id'}
    def __getitem__(self,name):
        if 'ptm_status'==name:
            return 'experimental' # not stored in IMS2
        if 'participant_id'==name:
            return self.get_participant_id(self['gene_id'],PARTICIPANT_TYPE)
        return super(BioGRID.ims.PTM,self).__getitem__(name)
    def store(self):
        try:
            return super(BioGRID.ims.PTM,self).store()
        except _mysql_exceptions.OperationalError:
            p=Participant({'participant_value':self['gene_id'],
                           'participant_type_id':PARTICIPANT_TYPE,
                           'participant_status':'active'})
            p.store()
            warnings.warn(
                "Inserting participant_value=%d into participants" %
                self['gene_id'])
            return super(BioGRID.ims.PTM,self).store()


class PTM_source(BioGRID.ims.PTM_source):
    def __getitem__(self,name):
        if name==('ptm_source_status'):
            return 'active'
        return super(PTM_source,self).__getitem__(name)

class PTM_modification(BioGRID.ims.PTM_modification):
    _rename={'ptm_modification_name':'modification_name',
             'ptm_modification_id':'modification_id'}
    def id(self):
        try:
            return self.row['modification_id']
        except:
            print self
            print self.row
            raise
    def __getitem__(self,name):
        if name==('ptm_modification_status'):
            return 'active'
        return super(PTM_modification,self).__getitem__(name)

class PTM_relationship(BioGRID.ims.PTM_relationship):
    _rename={'ptm_relationship_type':'relationship_type',
             'ptm_relationship_identity':'relationship_identity'}
    def __getitem__(self,name):
        if 'user_id'==name:
            return DEFAULT_USER_ID
        if 'participant_id'==name:
            return self.get_participant_id(self.row['gene_id'],
                                           PARTICIPANT_TYPE)
        return super(PTM_relationship,self).__getitem__(name)

class PTM_history(BioGRID.ims.PTM_history):
    _rename={'ptm_history_date':'ptm_addeddate'}
    def __getitem__(self,name):
        if 'modification_type'==name:
            if 'active'==self['ptm_status']:
                return 'ACTIVITATED'
            else:
                # hopefully produce a warning message
                return self['ptm_status']
        elif 'user_id'==name:
            return DEFAULT_USER_ID
        elif 'ptm_history_comment'==name:
            if 'TRUE'==self['ptm_status']:
                return "Warning: TRUE"
            else:
                return None
        return super(PTM_history,self).__getitem__(name)
    def store(self):
        try:
            return super(BioGRID.ims.PTM_history,self).store()
        except _mysql_exceptions.OperationalError:
            print row
            raise

class PTM_note(BioGRID.ims.PTM_note):
    _rename={'ptm_note_addeddate':'ptm_addeddate',
             'ptm_note_status':'ptm_status'}
    def __getitem__(self,name):
        if 'user_id'==name:
            return DEFAULT_USER_ID
        elif 'ptm_note_text'==name:
            #notes=eval(self['ptm_notes'])
            notes=json.loads(self['ptm_notes'])
            if len(notes)==0:
                return None
            elif len(notes)==1:
                return notes[0]
            else:
                raise StandardError('Found multiple notes')
        return super(PTM_note,self).__getitem__(name)
    def store(self):
        if '[]'==self.row['ptm_notes']:
            return None
        return super(PTM_note,self).store()

class Participant(BioGRID.ims.Participant):
    def id(self):
        return None
    def __getitem__(self,name):
        if 'participant_status'==name:
            return 'active'
        if 'participant_type_id'==name:
            return PARTICIPANT_TYPE # for now assume protein
        return super(Participant,self).__getitem__(name)

if __name__ == '__main__':
    import sys
    from optparse import OptionParser
    import MySQLdb.cursors
    import _mysql_exceptions


    def warn_fmt(message,category,filename,lineno,line=None):
        return "%s\n" % message
    warnings.formatwarning=warn_fmt

    p=OptionParser()
    p.add_option('-c','--config',metavar='JSON')
    p.add_option('-s','--sql-dir',metavar='PATH')
    p.add_option('--clean',action='store_true')
    (opts,jobs)=p.parse_args()
    
    cfg=Config(opts.config)
    BioGRID.ims._Table.config=cfg
    if opts.clean:
        msg_fmt='removing %s'
    else:
        ims2=cfg.ims2db() # not needed in --clean
        msg_fmt='starting %s'
    ims3=cfg.imsdb()

    for job in jobs:
        warnings.warn(msg_fmt % job)

        # First check for SQL files containing IMS3 schema
        file=open('%s/%s.sql' % (opts.sql_dir,job))
        if opts.clean:
            line=file.readline()
            tables=[]
            while line:
                if line.startswith('CREATE TABLE'):
                    table=line.split(' ')[-1].strip("(\n")
                    tables.insert(0,table)
                line=file.readline()
            file.close()

            for table in tables:
                try:
                    ims3.query('DROP TABLE %s' % table)
                except _mysql_exceptions.OperationalError as(errno,msg):
                    if 1051==errno: # Unknown table
                        pass
                    else:
                        raise


        else:
            sqls=file.read()
            file.close()
            # WARNING! Don't use ; is you comments in the SQL files!
            for sql in sqls.split(';'):
                try:
                    #print sql
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
            elif 'Participant'==job:
                c.execute('''
(SELECT DISTINCT interactor_A_id AS participant_value FROM interactions)
UNION DISTINCT
(SELECT DISTINCT interactor_B_id AS participant_value FROM interactions)
''')
            else:
                # there doesn't really seem to be secure way to have dynamic
                # table names

                if 'Interaction_quantitation_type'==job:
                    # IMS2 table is not plural
                    table_name=job.lower()
                elif 'Publication_query'==job:
                    table_name='pubmed_queries'
                elif 'Project_publication'==job:
                    table_name='project_pubmeds'
                elif 'PTM_modification'==job:
                    table_name='modification'
                elif 'PTM_history'==job or 'PTM_note'==job:
                    table_name='ptms'
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
