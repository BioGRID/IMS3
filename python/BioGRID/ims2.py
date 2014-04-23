"""Stuff to convert IMS2 database schema to IMS3.  Hopefully this will
be the only files with IMS2 information in it."""
import json
import BioGRID.ims
from time import strftime
import MySQLdb.cursors

global PARTICIPANT_TYPE
PARTICIPANT_TYPE=1
global DEFAULT_USER_ID
DEFAULT_USER_ID=1
#global IGNORE_ID
#IGNORE_ID=None
global SOURCE_IDS
SOURCE_IDS={}

class Config(BioGRID.ims.Config):
    def ims2db(self):
        """Returns a MySQLdb pointer to the IMS2 database."""
        return self._db('ims2')

class _Table(object):
    @classmethod
    def ims2_cursor(self,cur=MySQLdb.cursors.DictCursor):
        return self.config.ims2db().cursor(cur)
    @classmethod
    def ims2_table(cls):
        # IMS2 table is not plural
        return cls.table()
    @classmethod
    def slurp_sql(cls):
        # there doesn't really seem to be secure way to have dynamic
        # table names
        return 'SELECT * FROM %s' % cls.ims2_table()
    @classmethod
    def slurp(cls):
        c=cls.ims2_cursor()
        c.execute(cls.slurp_sql())
        cls.puke(c)
    @classmethod
    def puke(cls,c):
        raw=c.fetchone()
        while raw:
            cooked=cls(raw)
            cooked.store()
            raw=c.fetchone()
    def pubmed_id(self):
        """Returns the PubMed ID as reported from the IMS2 database.
        Otherwise returns None if current object has no
        'publication_id' item."""
        pub_id=self['publication_id']
        if None!=pub_id:
            c=self.ims2_cursor()
            c.execute('''SELECT publication_pubmed_id FROM publications
WHERE publication_id=%s''',(pub_id,))
            return BioGRID.ims.fetch_one(c,'publication_pubmed_id')
        return None

class Project(BioGRID.ims.Project,_Table):
    _rename={'project_addeddate':'project_timestamp'}

    def __getitem__(self,name):
        if 'project_status'==name:
            status=self.row[name]
            if('open'==status):
                return 'public'
            else:
                return 'private'
        return super(Project,self).__getitem__(name)

class User(BioGRID.ims.User,_Table):
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

class Project_user(BioGRID.ims.Project_user,_Table):
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
                self.warn('user_id %s not in users' % self['user_id'])

class Interaction(BioGRID.ims.Interaction,_Table):
    IGNORE_ID=None
    def __init__(self,passthru):
        out=super(Interaction,self).__init__(passthru)

        if None==Interaction.IGNORE_ID:
            c=self.ims2_cursor()
            c.execute('SELECT tag_category_id AS id FROM tag_categories WHERE tag_category_name=%s',
                      ('Ignore Interactions',));
            Interaction.IGNORE_ID=BioGRID.ims.fetch_one(c,'id');
            self.warn('Fetched IGNORE_ID==%d' % Interaction.IGNORE_ID)

        if 0==len(SOURCE_IDS):
            c=self.ims_cursor()
            c.execute('''SELECT
interaction_source_id,interaction_source_name FROM interaction_sources''')
            row=c.fetchone()
            while row:
                SOURCE_IDS[row['interaction_source_name']
                           ]=row['interaction_source_id']
                row=c.fetchone()
            self.warn('Source index: %s' % str(SOURCE_IDS))
        return out
    def __getitem__(self,name):
        if 'interaction_status'==name:
            c=self.ims2_cursor()
            c.execute('''SELECT tag_id FROM interaction_tag_mappings 
WHERE interaction_id=%s AND tag_id IN
(SELECT tag_id FROM tags WHERE tag_category_id=%s)
''',(self.id(),Interaction.IGNORE_ID))
            tag_id=BioGRID.ims.fetch_one(c,'tag_id')
            if tag_id:
                return 'temporary'
            return 'normal'
        elif 'interaction_source_id'==name:
            c=self.ims2_cursor()
            c.execute('''SELECT
REPLACE(tag_name,'-Ignore','') AS is_name
FROM tag_categories
JOIN tags USING(tag_category_id)
JOIN interaction_tag_mappings USING(tag_id)
WHERE tag_category_name IN('Source','Ignore Interactions')
AND interaction_id=%s
''',(self.id(),))
            name=BioGRID.ims.fetch_one(c,'is_name')
            if None==name:
                return SOURCE_IDS['BioGRID']
            return SOURCE_IDS[name]

        return super(Interaction,self).__getitem__(name)
    def store(self):
        try:
            return super(Interaction,self).store()
        except _mysql_exceptions.IntegrityError:
            pmid=self.pubmed_id()
            c=self.ims2_cursor()
            c.execute('''SELECT modification_type FROM interaction_matrix
WHERE interaction_id=%s''',(self.id(),))
            mod_type=BioGRID.ims.fetch_one(c,'modification_type')
            self.warn('skipping %s where PubMed ID is %s' % (mod_type,pmid))

class Interaction_source(BioGRID.ims.Interaction_source,_Table):
    @classmethod
    def slurp_sql(cls):
        return '''SELECT
REPLACE(tag_name,'-Ignore','') AS interaction_source_name,
tag_added_date AS interaction_source_addeddate,
tag_status AS interaction_source_status,
tag_category_name
FROM tag_categories JOIN tags USING(tag_category_id)
WHERE tag_category_name IN('Source','Ignore Interactions')'''

    def id(self):
        return None

class Interaction_quantitation(BioGRID.ims.Interaction_quantitation,_Table):
    @classmethod
    def slurp_sql(cls):
        return '''SELECT iq.*,user_id,interaction_history_date
AS interaction_quantitation_addeddate
FROM interaction_quantitation AS iq
JOIN interaction_matrix USING(interaction_id)'''
    def __getitem__(self,name):
        if 'interaction_quantitation_status'==name:
            return 'active'
        return super(Interaction_quantitation,self).__getitem__(name)

class Interaction_quantitation_type(BioGRID.ims.Interaction_quantitation_type,_Table):
    @classmethod
    def ims2_table(cls):
        return cls.__name__.lower()
    def __getitem__(self,name):
        if 'interaction_quantitation_type_addeddate'==name:
            return '%s %s' % (
                self.row['interaction_quantitation_type_date_added'],
                self.row['interaction_quantitation_type_time_added'])
        elif 'interaction_quantitation_type_status'==name:
            return 'active'
        return super(Interaction_quantitation_type,self).__getitem__(name)

class Interaction_note(BioGRID.ims.Interaction_note,_Table):
    _rename={'interaction_note_text':'interaction_qualification',
             'interaction_note_status':'interaction_qualification_status'}
    _user_ids=[]
    @classmethod
    def ims2_table(cls):
        return 'interaction_qualifications'
    def __getitem__(self,name):
        if 'user_id'==name:
            user_id=self.validate_user_id()
            if user_id:
                return user_id
            self.warn('skipping where user_id=%d' % self.row['user_id'])
            return DEFAULT_USER_ID

        return super(Interaction_note,self).__getitem__(name)
    def id(self):
        return self.row['interaction_qualification_id']
    def store(self):
        try:
            return super(Interaction_note,self).store()
        except _mysql_exceptions.IntegrityError as x:
            if 0!=str(x).count("REFERENCES `interactions` (`interaction_id`)"):
                self.warn('skipping where interaction_id=%s' %
                          self['interaction_id'])
            else:
                raise

class Interaction_participant(BioGRID.ims.Interaction_participant,_Table):
    ROLE_ID={}
    P2P={} # BioGRID Protein ID -> participant_id
    def __init__(self,passthru):
        out=super(Interaction_participant,self).__init__(passthru)
        if 0==len(Interaction_participant.P2P):
            c=self.ims_cursor()
            c.execute('''SELECT DISTINCT participant_id,participant_value FROM participants
WHERE participant_type_id=%s''',(PARTICIPANT_TYPE,))
            raw=c.fetchone()
            while raw:
                Interaction_participant.P2P[raw['participant_value']]=raw['participant_id']
                raw=c.fetchone()
            self.warn('fetched participant ids')
        return out

    @classmethod
    def slurp_sql(cls):
        c=cls.ims_cursor()
        c.execute('''SELECT participant_role_name AS K,
participant_role_id as V FROM participant_roles''')
        row=c.fetchone()
        ROLE_ID={}
        while row:
            ROLE_ID[row['K']]=row['V']
            row=c.fetchone()
        return '''
(SELECT interaction_id,publication_id,interactor_A_id AS interactor_id,%d AS participant_role_id FROM interactions)
UNION
(SELECT interaction_id,publication_id,interactor_B_id AS interactor_id,%d AS participant_role_id FROM interactions)
''' % (ROLE_ID['bait'],ROLE_ID['prey'])
    def __getitem__(self,name):
        if 'participant_id'==name:
            return Interaction_participant.P2P[self['interactor_id']]
        elif 'interaction_participant_status'==name:
            return 'active'
        return super(Interaction_participant,self).__getitem__(name)
    def store(self):
        try:
            return super(Interaction_participant,self).store()
        except _mysql_exceptions.IntegrityError:
            self.warn('Skipping where PubMed ID is %s' % self.pubmed_id())

# class Iplex_project(BioGRID.ims.Iplex_project):
#     _rename={'iplex_project_name':'iplex_name',
#              'iplex_project_description':'iplex_description',
#              'iplex_project_addeddate':'iplex_createddate',
#              'iplex_project_status':'iplex_status'}

class Publication(BioGRID.ims.Publication,_Table):
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
            self.warn('skipping since PubMed ID is %s' %
                      self['publication_pubmed_id'])
            return
        if 0==pmid:
            self.warn('skipped since PubMed ID is %d' % pmid)
        else:
            try:
                super(Publication,self).store()
            except _mysql_exceptions.IntegrityError:
                self.warn('skipping dup entry where PubMed ID is %d' % pmid)

class Publication_query(BioGRID.ims.Publication_query,_Table):
    _rename={'publication_query_value':'pubmed_query_value',
             'publication_query_addeddate':'pubmed_query_added_date',
             'publication_query_lastrun':'pubmed_query_last_run',
             'publication_query_type':'pubmed_query_type',
             'publication_query_status':'pubmed_query_status'}
    @classmethod
    def ims2_table(cls):
        return 'pubmed_queries'
    def id(self):
        """Overloaded because the table name is different between IMS2
        and IMS3."""
        return self.row['pubmed_query_id']

class Project_publication(BioGRID.ims.Project_publication,_Table):
    """Make sure the Publicatin table is loaded before this!"""
    _rename={'project_publication_addeddate':'project_pubmed_timestamp',
             'project_publication_status':'project_pubmed_status',
             'publication_query_id':'pubmed_query_id'}
    @classmethod
    def ims2_table(cls):
        return 'project_pubmeds'
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
                self.warn('inserting PubMed ID %d into publications' % pmid)
                return pub.id()
            return pub_id

        out=super(Project_publication,self).__getitem__(name)
        if ('publication_query_id'==name)and(0==out):
            return None
        return out

class PTM(BioGRID.ims.PTM,_Table):
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


class PTM_source(BioGRID.ims.PTM_source,_Table):
    def __getitem__(self,name):
        if name==('ptm_source_status'):
            return 'active'
        return super(PTM_source,self).__getitem__(name)

class PTM_modification(BioGRID.ims.PTM_modification,_Table):
    _rename={'ptm_modification_name':'modification_name',
             'ptm_modification_id':'modification_id'}
    @classmethod
    def ims2_table(cls):
        return 'modification'
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

class PTM_relationship(BioGRID.ims.PTM_relationship,_Table):
    _rename={'ptm_relationship_type':'relationship_type',
             'ptm_relationship_identity':'relationship_identity'}
    def __getitem__(self,name):
        if 'user_id'==name:
            return DEFAULT_USER_ID
        if 'participant_id'==name:
            return self.get_participant_id(self.row['gene_id'],
                                           PARTICIPANT_TYPE)
        return super(PTM_relationship,self).__getitem__(name)

class PTM_history(BioGRID.ims.PTM_history,_Table):
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
    @classmethod
    def ims2_table(cls):
        return 'ptms'
    def store(self):
        try:
            return super(BioGRID.ims.PTM_history,self).store()
        except _mysql_exceptions.OperationalError:
            print row
            raise

class PTM_note(BioGRID.ims.PTM_note,_Table):
    _rename={'ptm_note_addeddate':'ptm_addeddate',
             'ptm_note_status':'ptm_status'}
    @classmethod
    def ims2_table(cls):
        return 'ptms'
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

class Participant(BioGRID.ims.Participant,_Table):
    def id(self):
        return None
    @classmethod
    def slurp_sql(cls):
        return '''
(SELECT DISTINCT interactor_A_id AS participant_value FROM interactions)
UNION DISTINCT
(SELECT DISTINCT interactor_B_id AS participant_value FROM interactions)
'''
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
    import warnings

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
            Table=eval(job)
            Table.slurp()
            ims3.commit()
