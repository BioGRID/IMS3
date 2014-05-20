""""Stuff to convert IMS2 database schema to IMS3.  Hopefully this will
be the only files with IMS2 information in it."""
import json
import BioGRID.ims
from time import strftime
import MySQLdb.cursors
import _mysql_exceptions

global PARTICIPANT_TYPE
PARTICIPANT_TYPE=1
global UNKNOWN_PARTICIPANT_TYPE
UNKNOWN_PARTICIPANT_TYPE=2
global DEFAULT_USER_ID
DEFAULT_USER_ID=1

class Config(BioGRID.ims.Config):
    def ims2db(self):
        """Returns a MySQLdb pointer to the IMS2 database."""
        return self._db('ims2')
    def ims3db(self):
        return self.imsdb()

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
        """Does an SQL query of all the stiff in IMS2 and passes it to
        puke()."""
        sqls=cls.slurp_sql()
        if('str'==type(sqls).__name__):
            sqls=[sqls]
        c=cls.ims2_cursor()

        # I'm not sure we are ever going to have more then one sql at
        # at time
        for sql in sqls:
            c.execute(sql)
            cls.puke(c)
    @classmethod
    def puke(cls,c):
        """Processes all the items in the provided cursor and saves
        them in the database."""
        raw=c.fetchone()
        while raw:
            cooked=cls(raw)
            cooked.store()
            raw=c.fetchone()
    # def interaction(self,interaction_id=None):
    #     """If the table has an interaction_id returns an Interaction
    #     object."""
    #     if(None==interaction_id):
    #         interaction_id=self['interaction_id']
    #     c=self.ims_cursor()
    #     c.execute('''SELECT * FROM interactions WHERE interaction_id=%s''',
    #               (interaction_id,))
    #     row=c.fetchone()
    #     print interaction_id
    #     return Interaction(row)
    def pubmed_id(self):
        """Returns the PubMed ID as reported from the IMS2 database, a string.
        Otherwise returns None if current object has no
        'publication_id' item. """
        pub_id=self['publication_id']
        if None==pub_id:
            sql='''SELECT publication_pubmed_id FROM interactions
JOIN publications USING(publication_id) WHERE interaction_id=%s'''
            use_id=self['interaction_id']
        else:
            sql='''SELECT publication_pubmed_id FROM publications
WHERE publication_id=%s'''
            use_id=pub_id

        c=self.ims2_cursor()
        c.execute(sql,(use_id,))
        return BioGRID.ims.fetch_one(c,'publication_pubmed_id')
        

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
        except _mysql_exceptions.IntegrityError:
            if not(self.validate_user_id()):
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
                return Interaction_source.factory('BioGRID').id()
            return Interaction_source.factory(name).id()
        out=super(Interaction,self).__getitem__(name)
        if None==out:
            if 'interaction_type_id'==name:
                out=Interaction_type.factory('Protein-Protein').id()
        return out
    def store(self):
        try:
            return super(Interaction,self).store()
        except _mysql_exceptions.IntegrityError:
            pp_id=Interaction_type.factory('Protein-Protein').id()
            if pp_id==self['interaction_type_id']:
                pmid=self.pubmed_id()
                c=self.ims2_cursor()
                c.execute('''SELECT modification_type FROM interaction_matrix
WHERE interaction_id=%s''',(self.id(),))
                mod_type=BioGRID.ims.fetch_one(c,'modification_type')
                self.warn('skipping %s where PubMed ID is %s'
                          % (mod_type,pmid))
            else:
                raise


class Interaction_history(BioGRID.ims.Interaction_history,_Table):
    def store(self):
        try:
            return super(Interaction_history,self).store()
        except _mysql_exceptions.IntegrityError:
                pubmed_id=self.pubmed_id()
                self.warn("Skipping where pubmed_id=%s and user_id=%d"
                          % (self.pubmed_id(),self['user_id']))

class Interaction_type(BioGRID.ims._Table):
    pass

class Participant_role(BioGRID.ims._Table):
    pass

class Unknown_participant(BioGRID.ims.Unknown_participant,_Table):
    @classmethod
    def slurp_sql(cls):
        return 'SELECT * FROM interaction_forced_additions'
    @classmethod
    def get_participant(cls,force,ab):
        if 'Found'==force['interactor_%s_forced_status' % ab]:
            c=cls.ims_cursor()
            sql='''SELECT * FROM participants WHERE
participant_value=%s AND participant_type_id=%s'''
            c.execute(sql, (force['interactor_%s_name' % ab],PARTICIPANT_TYPE))
            fetched=c.fetchone()
            if None==fetched:
                p=Participant(
                    {'participant_value':force['interactor_%s_name' % ab],
                     'participant_type_id':PARTICIPANT_TYPE}
                    )
                p.store()
                return p
            else:
                return Participant(fetched)
        
        # Now we need to actually create an Unknown_participant object!
        up=Unknown_participant(
            {'unknown_participant_identifier':force['interactor_%s_name' % ab],
             'participant_type_id':PARTICIPANT_TYPE,
             'organis_id':force['interactor_%s_organism_id' % ab],
             'publication_id':force['publication_id'],
             'unknown_participant_status':'active'}
            )
        up.store()
        
        p=Participant(
            {'participant_value':up.id(),
             'participant_type_id':UNKNOWN_PARTICIPANT_TYPE,
             'participant_status':'active'}
            )
        p.store()

        return p
    @classmethod
    def puke(cls,c):
        for force in c.fetchall():
            #print force

            i=Interaction(
                {'publication_id':force['publication_id'],
                 'interaction_type':Interaction_type.factory('Protein-Protein').id(),
                 'interaction_status':'normal',
                 'interaction_source_id':Interaction_source.factory('BioGRID').id()}
                )
            i.store()

            foo=cls.get_participant(force,'A')
            a_id=foo.id()
            a=Interaction_participant(
                {'interaction_id':i.id(),
                 'participant_id':a_id,
                 'participant_role_id':Participant_role.factory('bait').id(),
                 'status':'active'}
                )
            a.store()

            bar=cls.get_participant(force,'B')
            b_id=bar.id()
            b=Interaction_participant(
                {'interaction_id':i.id(),
                 'participant_id':b_id,
                 'participant_role_id':Participant_role.factory('prey').id(),
                 'status':'active'}
                )
            b.store()
            

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

#    def id(self):
#        return None

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
        try:
            out=self.row['interaction_qualification_id']
        except KeyError:
            return None
        return out
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
        cfg=cls.config
        return '''
(SELECT interaction_id,publication_id,interactor_A_id AS interactor_id,%d AS participant_role_id FROM interactions)
UNION
(SELECT interaction_id,publication_id,interactor_B_id AS interactor_id,%d AS participant_role_id FROM interactions)
''' % (Participant_role.factory('bait').id(),
       Participant_role.factory('prey').id())
    def __getitem__(self,name):
        out=super(Interaction_participant,self).__getitem__(name)

        if None==out:
            if 'participant_id'==name:
                iid=self['interactor_id']
                try:
                    return Interaction_participant.P2P[iid]
                except KeyError:
                    #print "%s !!!!!!" % iid
                    p=Participant(
                        {'participant_value':iid,
                         'participant_type_id':PARTICIPANT_TYPE}
                        )
                    p.store()
                    pid=p.id()
                    Interaction_participant.P2P[self['interactor_id']]=pid
                    # map interactor id -> participant id
                    self.warn('New Participant: %d -> %d' % (iid,pid))
                    return Interaction_participant.P2P[self['interactor_id']]
            elif 'interaction_participant_status'==name:
                return 'active'
        return out
    def store(self):
        try:
            return super(Interaction_participant,self).store()
        except _mysql_exceptions.IntegrityError:
            self.warn('Skipping where PubMed ID is %s' % self.pubmed_id())

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
            self.warn(
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
            #print self.row
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
            #print row
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
    @classmethod
    def slurp_sql(cls):
        return '''
(SELECT DISTINCT interactor_A_id AS participant_value FROM interactions)
UNION DISTINCT
(SELECT DISTINCT interactor_B_id AS participant_value FROM interactions)
'''
    def __getitem__(self,name):
        out=super(Participant,self).__getitem__(name)
        if None==out:
            if 'participant_type_id'==name:
                return PARTICIPANT_TYPE
            if 'participant_status'==name:
                return 'active'
        return out

class Complex(BioGRID.ims._Table,_Table):
    """This table is only in IMS2, not IMS3. Data from it is now
    stored in the Interaction tables."""

    def logs(self):
        """Read items from the IMS2.complex_history table and returns
        them."""
        c=self.ims2_cursor()
        c.execute("SELECT * FROM complex_history WHERE complex_id=%s",
                  (self['complex_id'],))
        return c.fetchall()
    def notes(self):
        c=self.ims2_cursor()
        c.execute("SELECT * FROM complex_qualifications WHERE complex_id=%s",
                  (self['complex_id'],))
        return c.fetchall()
    @classmethod
    def table(cls):
        return 'complexes'
    @classmethod
    def puke(cls,c):
        raw=c.fetchone()
        complex_id=Interaction_type.factory('Complex').id()
        source_id=Interaction_source.factory('BioGRID').id()
        while raw:
            cpx=Complex(raw)
            i=Interaction(
                {'publication_id':cpx['publication_id'],
                 'interaction_type_id':complex_id,
                 'interaction_source_id':source_id}
                )
            i.store()
            interaction_id=i.id()
            for interactor_id in cpx['complex_participants'].split('|'):
                #pid=cpx.get_participant_id(bid,PARTICIPANT_TYPE)
                #pid=cpx.pgid(bid,PARTICIPANT_TYPE)
                ip=Interaction_participant(
                    {'interaction_id':interaction_id,
                     'interactor_id':int(interactor_id),
                     'participant_role_id':Participant_role.factory(
                            'unspecified').id()
                     }
                    )
                ip.store()

                for log in cpx.logs():
                    log['interaction_id']=i.id()
                    log['interaction_history_comment']=log['complex_history_comment']
                    log['interaction_history_date']=log['complex_history_date']
                    ih=Interaction_history(log)
                    ih.store()

                for note in cpx.notes():
                    note['interaction_id']=i.id()
                    note['interaction_note_text']=note['complex_qualification']
                    note['interaction_note_status']=note['complex_qualification_status']
                    foo=BioGRID.ims.Interaction_note(note)
                    foo.store()

            raw=c.fetchone()




