import json
import sys
import MySQLdb
import MySQLdb.cursors
import warnings
from copy import copy
from pprint import pprint

def fetch_one(cur,get): # and only one
    row=cur.fetchone()
    if row:
        out=row[get]
        if cur.fetchone():
            raise StandardError('Expecting 1 row got more then 1')
    else:
        return None
    return out

 
class Config:
    """Loads stuff from JSON configure file and provides access."""

    def __init__(self,path='ims.json'):
        self.json=json.loads(open(path).read())
        self.dbs={}
    def _db(self,section):
        try:
            return self.dbs[section]
        except KeyError:
            db=self.json['dbs'][section]
            self.dbs[section]=MySQLdb.connect(
                user=db['user'],
                passwd=db['passwd'],
                db=db['schema'])

            warnings.warn('Connecting to DB %s' % section)
        # If it don't work now we want to die
        return self.dbs[section]
    def imsdb(self):
        """Returns a MySQLdb object to the IMS3 database."""
        return self._db('ims')
    def imsdb_name(self):
        """Returns the name if the IMS3 database."""
        # need to str(...) here so we don't convert strings into
        # unicode.
        return str(self.json['dbs']['ims']['schema'])
    def imsdb_cursor(self,cur=MySQLdb.cursors.DictCursor):
        return self.imsdb().cursor(cur)
    def _sql2kv(self,sql):
        c=self.imsdb_cursor()
        c.execute(sql)
        out=self.cursor2kv(c)
        warnings.warn(str(out))
        return out
        
    def cursor2kv(self,c,k='k',v='v'):
        """Convert an MySQL curser to a key/value pair."""
        out={}
        row=c.fetchone()
        while row:
            out[row[k]]=row[v]
            row=c.fetchone()
        return out


class _Table(object):
    """The class-wide variable _Table.config must be set with an
    instance of the Config class."""
    _rename={}
    _user_ids=[]
    def __init__(self,row):
        self.row=row
#    def __repr__(self):
#        return '%s:%s' % (self.id_column(),self.id())
    def __getitem__(self,name):
        # Rename items as needed, mainly for IMS2 conversion, bit I
        # thought it might come in handy for other things too.
        try:
            name=self._rename[name]
        except KeyError:
            pass

        try:
            return self.row[name]
        except KeyError:
            return None
    def __eq__(self,other):
        """This is a deep equals, it does more then just just the id,
        it checks the elements too. (err, not implemented)"""
        if (other==None) or (self.id() != other.id()):
            return False
        raise NotImplementedError('__eq__')

    FACTORY={}
    @classmethod
    def factory(cls,name):
        try:
            return cls.FACTORY[name]
        except KeyError:
            table=cls.table()
            col_name='%s_name' % cls.__name__
            sql="SELECT * FROM %s WHERE %s=%%s" % (table,col_name)
            c=cls.ims_cursor()
            c.execute(sql,(name,))
            o=cls(c.fetchone())
            warnings.warn('%s: %s -> %d' % (table,name,o.id()))
            cls.FACTORY[name]=o
        return cls.FACTORY[name]
    @classmethod
    def cursor2kv(self,c,k='k',v='v'):
        return self.config.cursor2kv(c,k,v)
    @classmethod
    def ims_cursor(self,cur=MySQLdb.cursors.DictCursor):
        """Returns a MySQLdb.cursors.DictCursor to the IMS
        database."""
        return self.config.imsdb_cursor(cur)
    def validate_user_id(self,user_id=None):
        if None==user_id:
            user_id=self.row['user_id']
        if 0==len(self._user_ids):
            c=self.ims_cursor()
            c.execute('SELECT user_id FROM users')
            for u in c.fetchall():
                self._user_ids.append(u['user_id'])
            warnings.warn('Loading user_ids')
        try:
            self._user_ids.index(user_id)
        except ValueError:
            return None
        return user_id
    def saved_self(self):
        """Returns a version of the same object, but as saved in the
        database."""
        sql='SELECT * FROM %s WHERE %s=%%s' % (self.table(),self.id_column())
        c=self.ims_cursor()
        c.execute(sql,(self.id(),))
        in_db=c.fetchone()
        if in_db:
            return self.__class__(in_db)
        return None

    @classmethod
    def table(cls):
        """Returns the primary SQL table name of this object."""
        return '%ss' % cls.__name__.lower()
    @classmethod
    def id_column(cls):
        return '%s_id' % cls.__name__.lower()

    def id(self):
        try:
            #print self.row
            return self.row[self.id_column()]
        except KeyError:
            # If we don't have the id we assume it's not in the database.
            return None
    def warn(self,msg):
        warnings.warn('%s=%s %s' % (self.id_column(),str(self.id()),msg))
    def insert(self):
        """Blindly insert a new row, no checking do dup primary key or
        anything."""
        cur=self.ims_cursor()
        vals=[]
        for column in self._columns:
            vals.append(self[column])
        primary_id=self.id()
        if primary_id:
            vals.append(self.id())
        sql=self.insert_sql(include_id_column=primary_id)
        cur.execute(sql,vals)
        if primary_id:
            return primary_id

        # fetche the primary key we just got
        cur.execute('SELECT LAST_INSERT_ID() AS id')
        self.row[self.id_column()]=cur.fetchone()['id']
    def store(self):
        """Store stuff if it doesen't exist, or if it's modified."""
        saved=self.saved_self()
        if not saved:
            self.insert()
        elif self==saved:
            pass # don't need no saving
        else:
            # A version of abrt older then 2.0.8-21.el6 made this not
            # work correctly
            raise NotImplementedError('No updating parts!')
        return self.id()
    def load(self):
        """Set the id if already in database, or stores it."""

        if hasattr(self,'_unique'):
            # If we know the unique items, only check those
            cols=self._unique
        else:
            cols=self.row.keys()

        where=[]
        vals=[]
        for col in cols:
            where.append('%s=%%s' % col)
            vals.append(self[col])
            
        sql='SELECT %s AS id FROM %s WHERE %s' % (self.id_column(),self.table(),' AND '.join(where));
        cur=self.ims_cursor()
        cur.execute(sql,vals)
        got=cur.fetchone()
        if got:
            self.row[self.id_column()]=got['id']
        else:
            self.store()
        return got

    def insert_sql(self,include_id_column=True):
        if(include_id_column):
            cols=copy(self._columns)
            cols.append(self.id_column())
        else:
            cols=self._columns
        return 'INSERT INTO %s(%s)VALUES(%s)' % (
            self.table(),','.join(cols),('%s,'*len(cols)).strip(',')
            )

    def get_participant_id(self,value,p_type):
        c=self.ims_cursor()
        c.execute('''SELECT participant_id FROM participants
WHERE participant_value=%s AND participant_type_id=%s
''',(value,p_type))
        return fetch_one(c,'participant_id')
    def pgid(self,v,p):
        # v usually points to a value in the quick database
        out=self.get_participant_id(v,p)
        if None==out:
            p=Participant(
                {'participant_value':v,
                 'participant_type':t}
                )
            p.store()
            return p.id()
        return out


class Project(_Table):
    """Stores a row from the PROJECT table."""
    _columns=['project_name','project_description','project_addeddate'
              ,'organism_id','project_status']

class User(_Table):
    """Stores a row from the USERS table."""
    _columns=['user_name','user_password','user_cookie','user_firstname',
              'user_lastname','user_email','user_addeddate','user_lastaccess',
              'user_role','project_id']
    
class Project_user(_Table):
    """Stores a row from the PROJECT_USERS table."""
    _columns=['project_id','user_id','project_user_status',
              'project_user_addeddate']

class Interaction(_Table):
    _columns=['participant_hash','publication_id','interaction_type_id',
              'interaction_status','interaction_source_id']

class Interaction_history(_Table):
    @classmethod
    def table(cls):
        return 'interaction_history'
    _columns=['modification_type','interaction_id','user_id',
              'interaction_history_comment','interaction_history_date']

class Interaction_source(_Table):
    """List of interaction sources."""
    _columns=['interaction_source_name','interaction_source_url',
              'interaction_source_baseurl','interaction_source_addeddate',
              'interaction_source_status']

class Interaction_quantitation(_Table):
    _columns=['interaction_quantitation_value',           
              'interaction_quantitation_type_id','user_id',
              'interaction_quantitation_addeddate',
              'interaction_quantitation_status','interaction_id']

class Interaction_quantitation_type(_Table):
    _columns=['interaction_quantitation_type_name',
              'interaction_quantitation_type_desc',
              'interaction_quantitation_type_addeddate',
              'interaction_quantitation_type_status']

class Interaction_note(_Table):
    _columns=['interaction_note_text','user_id','interaction_note_addeddate',
              'interaction_note_status','interaction_id']

class Interaction_participant(_Table):
    _columns=['interaction_id','participant_id','participant_role_id',
              'interaction_participant_addeddate',
              'interaction_participant_status']

class Iplex_project(_Table):
    pass
#    _columns=['iplex_project_name','iplex_project_fullname',
#              'iplex_project_description','iplex_project_added`date',
#              'iplex_project_status']

class Publication(_Table):
    _columns=[
        'publication_pubmed_id','publication_article_title',
        'publication_abstract','publication_author_short',
        'publication_author_full','publication_volume',
        'publication_issue','publication_date',
        'publication_journal','publication_pagination',
        'publication_affiliation','publication_meshterms',
        'publication_status','publication_addeddate',
        'publication_lastupdated']


class Publication_query(_Table):
    @classmethod
    def table(cls):
        """Please don't use plurels when naming your SQL tables."""
        return 'publication_queries'
    _columns=['project_id','publication_query_value',
              'publication_query_addeddate','publication_query_lastrun',
              'publication_query_type','publication_query_status']

class Pubmed_mapping(_Table):
    _columns=['external_database_id','external_database_url',
              'external_database_name','publication_pubmed_id']

class Project_publication(_Table):
    _columns=['project_id','publication_id',
              'project_publication_addeddate',
              'project_publication_status','publication_query_id']

class PTM(_Table):
    _columns=['participant_id','ptm_residue_location','ptm_residue',
              'ptm_modification_id','publication_id','ptm_source_id',
              'ptm_status']

class PTM_source(_Table):
    _columns=['ptm_source_name','ptm_source_desc','ptm_source_addeddate',
              'ptm_source_status']

class PTM_modification(_Table):
    _columns=['ptm_modification_name','ptm_modification_desc',
              'ptm_modification_addeddate','ptm_modification_status']

class PTM_relationship(_Table):
    _columns=['ptm_id','participant_id','ptm_relationship_type',
              'publication_id','user_id','ptm_relationship_identity',
              'ptm_relationship_addeddate','ptm_relationship_status']	 

class PTM_history(_Table):
    @classmethod
    def table(cls):
        return 'ptm_history'
    _columns=['modification_type','ptm_id','user_id',
              'ptm_history_comment','ptm_history_date']

class PTM_note(_Table):
    _columns=['ptm_note_text','user_id','ptm_note_addeddate',
              'ptm_note_status','ptm_id']

class Participant(_Table):
    _unique=['participant_value','participant_type_id']
    _columns=['participant_id','participant_value','participant_type_id',
              'participant_addeddate','participant_status']

class Participant_type(_Table):
    _colums=['participant_type_name','participant_type_status',
             'participant_type_addeddate']

class Unknown_participant(_Table):
    _columns=['unknown_participant_identifier','participant_type_id',
              'organism_id','publication_id',
              'unknown_participant_addeddate','unknown_participant_status']

class Ontology(_Table):
    _columns=['ontology_name','ontology_url','ontology_rootid',
              'ontology_addeddate','ontology_lastparsed','ontology_status']
    @classmethod
    def table(cls):
        return 'ontologies'

class Ontology_term(_Table):
    _columns=['ontology_term_official_id','ontology_term_name',
              'ontology_term_desc','ontology_term_synonymns',
              'ontology_term_replacement','ontology_term_subsets',
              'ontology_term_preferred_name','ontology_id',
              'ontology_term_addeddate','ontology_term_status',
              'ontology_term_childcount','ontology_term_parent']

class Ontology_organism(_Table):
    # leave the other columns out for now so the IMS2 import uses the
    # default values.
    _columns=['ontology_id','organism_id']

class Ontology_relationship(_Table):
    _columns=['ontology_term_id','ontology_parent_id',
              'ontology_relationship_type',
              'ontology_relationship_addeddate',
              'ontology_relationship_status']

class Interaction_ontology(_Table):
    _columns=['interaction_id','ontology_term_id',
              #'user_id',
              'interaction_ontology_type_id']
    @classmethod
    def table(cls):
        return 'interaction_ontologies'

class Interaction_ontology_qualifier(_Table):
    _columns=['interaction_ontology_id','ontology_term_id',
              #'user_id',
              'interaction_ontology_qualifier_addeddate',
              'interaction_ontology_qualifier_status']
    @classmethod
    def table(cls):
        return 'interaction_ontologies_qualifiers'

class Dataset_queue(_Table):
    _columns=['dataset_queue_filename','dataset_queue_data','dataset_queue_filesize',
              'user_id','project_id','dataset_queue_interaction_count',
              'dataset_queue_forced','dataset_queue_addeddate','dataset_queue_status']
    @classmethod
    def table(cls):
        return 'dataset_queue'
