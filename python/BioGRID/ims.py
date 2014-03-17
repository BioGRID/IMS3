import json
import sys
import MySQLdb
import MySQLdb.cursors
import warnings
from copy import copy
 
class Config:
    """Loads stuff from JSON configure file and provides access."""

    def __init__(self,path='ims.json'):
        print path
        self.json=json.loads(open(path).read())
        self.dbs={}
    def _db(self,section):
        try:
            return self.dbs[section]
        except KeyError:
            db=self.json['dbs'][section]
            self.dbs[section]=MySQLdb.connect(**db)
            warnings.warn('Connecting to DB %s' % section)
        # If it don't work now we want to die
        return self.dbs[section]
    def imsdb(self):
        """Returns a MySQLdb object to the IMS3 database."""
        return self._db('ims')

class _Table(object):
    """The class-wide variable _Table.config must be set with an
    instance of the Config class."""
    _rename={}
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
        it checks the elements too."""
        if (other==None) or (self.id() != other.id()):
            return False
        raise NotImplementedError('__eq__')
    def ims_cursor(self,cur=MySQLdb.cursors.DictCursor):
        """Returns a MySQLdb.cursors.DictCursor to the IMS
        database."""
        return self.config.imsdb().cursor(cur)
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
        
    def id_column(self):
        return '%s_id' % self.__class__.__name__.lower()
    def id(self):
        return self.row[self.id_column()]
    def table(self):
        """Returns the primary SQL table name of this object."""
        return '%ss' % self.__class__.__name__.lower()
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
        cur.execute(self.insert_sql(include_id_column=primary_id),vals)

        #raise NotImplementedError(
        #'insert not implemented for %s' % self.__class__.__name__)
    def store(self):
        """Store stuff if it doesen't exist, or if it's modified."""
        saved=self.saved_self()
        if not saved:
            self.insert()
        elif self==saved:
            pass # don't need no saving
        else:
            # A version of abrt older 2.0.8-21.el6 made this not work
            # correctly
            raise NotImplementedError('No updating parts!')
    def insert_sql(self,include_id_column=True):
        if(include_id_column):
            cols=copy(self._columns)
            cols.append(self.id_column())
        else:
            cols=self._columns
        return 'INSERT INTO %s(%s)VALUES(%s)' % (
            self.table(),','.join(cols),('%s,'*len(cols)).strip(',')
            )

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

class Interaction_source(_Table):
    _columns=['interaction_source_name','interaction_source_url',
              'interaction_source_baseurl','interaction_source_addeddate',
              'interaction_source_status']
