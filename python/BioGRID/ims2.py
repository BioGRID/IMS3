"""Stuff to convert IMS2 database schema to IMS3.  Hopefully this will
be the only files with IMS2 information in it."""
import json
import BioGRID.ims
from time import strftime
import MySQLdb.cursors
import _mysql_exceptions
import warnings
import time

import sys
from pprint import pprint

# This means you should look it up in the quick_participants table.
global PARTICIPANT_TYPE
#PARTICIPANT_TYPE=1
global UNKNOWN_PARTICIPANT_TYPE
UNKNOWN_PARTICIPANT_TYPE=None

global DEFAULT_USER_ID
DEFAULT_USER_ID=1

global BAIT
BAIT='bait'
global PREY
PREY='hit'

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
        """Does an SQL query of all the stuff in IMS2 and passes it to
        puke()."""
        sqls=cls.slurp_sql()
        if('str'==type(sqls).__name__):
            sqls=[sqls]
        c=cls.ims2_cursor()

        qs=len(sqls)
        count=0
        #ims3=cls.config.imsdb()

        # Ontology_relationship returns a list of sql command to puke
        for sql in sqls:
            if(1!=qs):
                count+=1
                warnings.warn("%5d/%d queries" % (count,qs))
            c.execute(sql)
            cls.puke(c)
            #ims3.commit()
    @classmethod
    def fetchone(cls,c):
        return c.fetchone()
    @classmethod
    def also(cls):
        return False
    @classmethod
    def puke(cls,c):
        """Processes all the items in the provided cursor and saves
        them in the database."""
        raw=cls.fetchone(c)
        while raw:
            cooked=cls(raw)
            cooked.store()
            raw=cls.fetchone(c)
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

    @classmethod
    def pt_id2ot_id(cls,pt_id,warn=warnings):
        """Convert IMS2.phenotype_term_id to IMS3.ontology_term_id."""
        c=cls.ims2_cursor()
        sql='''SELECT ontology_term_id
FROM %(IMS3)s.ontology_terms AS ot
JOIN phenotypes AS pt ON(pt.phenotype_official_id=ot.ontology_term_official_id)
WHERE pt.phenotype_id=%(ID)s''' % {'IMS3':cls.config.imsdb_name(),'ID':pt_id}
        c.execute(sql)
        ot_id=c.fetchone()
        if None==ot_id:
            warn.warn("phenotype_id='%s' has no ontology match" % (pt_id))
            return False
        return ot_id['ontology_term_id']

    def pub2pub(self):
        """Convert IMS2.publication_id to IMS3.publication_id."""
        sql='''SELECT publication_id FROM publications WHERE
publication_pubmed_id=%s'''
        c=self.ims_cursor()
        c.execute(sql,(self.pubmed_id(),))
        return BioGRID.ims.fetch_one(c,'publication_id')
    def pubmed_id(self):
        """Returns the PubMed ID as reported from the IMS2 database, a string.
        Otherwise returns None if current object has no
        'publication_id' item. """
        try:
            pub_id=self.row['publication_id']
        except KeyError:
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

        # Setting this globally for the Interaction class
        if None==Interaction.IGNORE_ID:
            c=self.ims2_cursor()
            c.execute('SELECT tag_category_id AS id FROM tag_categories WHERE tag_category_name=%s',
                      ('Ignore Interactions',))
            Interaction.IGNORE_ID=BioGRID.ims.fetch_one(c,'id')
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
            out=super(Interaction,self).store()
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
                return
            else:
                raise

        self.throughput()
        return out

    def throughput(self,ims2_id=False,prefix='interaction'):
        if not(ims2_id):
            ims2_id=self.id()

        c=self.ims2_cursor()
        sql='''SELECT *
FROM %(TABLE)s_tag_mappings
JOIN tags USING(tag_id)
JOIN tag_categories USING(tag_category_id)
WHERE %(TABLE)s_id=%%s
AND tag_category_name='Throughput'
''' % {'TABLE':prefix}
        c.execute(sql,(ims2_id,))
        itm=self.fetchone(c)
        if(itm):
            ot_id=Ontology_term.factory(itm['tag_name'].lower()).id()
            io=Interaction_ontology({
                    'interaction_id':self.id(),
                    'ontology_term_id':ot_id,
                    'interaction_ontology_addeddate':itm[prefix+'_tag_mapping_timestamp'],
                    'interaction_ontology_status':itm[prefix+'_tag_mapping_status']})
            io.store()
        

    def force_attributes(self,cls,forced_id):
        """Should work with ether any *_forced_attributes table."""
        c=self.ims2_cursor()
        sql='''SELECT * FROM %(TABLE)s_forced_attributes
JOIN forced_attributes_types ON(forced_attribute_type_id=forced_attributes_types_id)
WHERE %(TABLE)s_forced_id=%%s''' % { 'TABLE': cls.TABLE_PREFIX }
        c.execute(sql,(forced_id,))
        for attr in c.fetchall():
            if 'Phenotype'==attr['forced_attributes_types_name']:
                pt_ids=attr['forced_attribute_type_id']
                for pt_id in pt_ids.split('|'):
                    ot_id=cls.pt_id2ot_id(pt_id,self)
                    if ot_id:
                        io=Interaction_ontology(
                            {'interaction_id':self.id(),
                             'ontology_term_id':ot_id,
                             'interaction_ontology_type_id':1})
                        io.load()                    
            elif('Qualification'==attr['forced_attributes_types_name']):
                note__user=attr[cls.TABLE_PREFIX+'_forced_attribute_value'].split('|',2)
                note=note__user[0]
                note_dict={
                    'interaction_note_text':note,
                    'interaction_note_addeddate':attr[cls.TABLE_PREFIX+'_forced_attribute_timestamp'],
                    'interaction_id':self.id()}
                try:
                    # Some have a user_id, others, no so much
                    note_dict['user_id']=int(note__user[1])
                except IndexError:
                    note_dict['user_id']=1 # defalut from Interaction_notes.sql
                    self.warn('no user_id found in qualification, using default.')
                    inote=BioGRID.ims.Interaction_note(note_dict)
                    try:
                        inote.store()
                    except _mysql_exceptions.IntegrityError:
                        pprint(attr)
                        pprint(inote.row)
                        raise
            elif 'Quantitation'==attr['forced_attributes_types_name']:
                quant__type=attr['interaction_forced_attribute_value'].split('|',2)
                quant=quant__type[0]
                type_id=quant__type[1]
                BioGRID.ims.Interaction_quantitation({
                        'interaction_quantation_value':quant,
                        'interaction_quantation_type_id':type_id,
                        'interaction_quantation_addeddate':attr[cls.TABLE_PREFIX+'_forced_attribute_timestamp'],
                        'interaction_id':self.id()
                        })
                    
            elif('Tag'==attr['forced_attributes_types_name']):
                c.execute('SELECT * FROM tags JOIN tag_categories USING(tag_category_id)'
                          'WHERE tag_id=%s' % attr[cls.TABLE_PREFIX+'_forced_attribute_value'])
                tag=c.fetchone()
                if 'Throughput'==tag['tag_category_name']:
                    ot_id=Ontology_term.factory(tag['tag_name'].lower()).id()
                    io=Interaction_ontology({
                            'interaction_id':self.id(),
                            'ontology_term_id':ot_id,
                            'interaction_ontology_addeddate':attr[cls.TABLE_PREFIX+'_forced_attribute_timestamp']
                            })
                    io.load()
                elif 'Ignore Interactions'==tag['tag_category_name']:
                    self.warn('Ignoring tag: %s' % tag['tag_name'])
                else:
                    pprint(attr)
                    pprint(tag)
                    sys.exit(1)
            else:
                pprint(attr)
                sys.exit(1)


class Interaction_history(BioGRID.ims.Interaction_history,_Table):
    def store(self):
        try:
            return super(Interaction_history,self).store()
        except _mysql_exceptions.IntegrityError:
                pubmed_id=self.pubmed_id()
                self.warn("Skipping where pubmed_id=%s and user_id=%d"
                          % (self.pubmed_id(),self['user_id']))

# Classes that just pass the inheritance are generally used by other
# classes to insert items.

class Interaction_type(BioGRID.ims._Table):
    pass

class Participant_type(BioGRID.ims.Participant_type):
    pass

class Participant_role(BioGRID.ims._Table):
    pass


class Unknown_participant(BioGRID.ims.Unknown_participant,_Table):
    """This does the interaction_forced_additions, for
    complex_forced_additions see Complex_forced_addition below."""

    TABLE_PREFIX='interaction'

    @classmethod
    def slurp_sql(cls):
        return 'SELECT * FROM interaction_forced_additions'
    @classmethod
    def get_participant(cls,force,ab,pub_id):
        global PARTICIPANT_TYPE

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
        
        PARTICIPANT_TYPE=Participant_type.factory('Gene').id()
        # Now we need to actually create an Unknown_participant object!
        up=Unknown_participant(
            {'unknown_participant_identifier':force['interactor_%s_name' % ab],
             'participant_type_id':PARTICIPANT_TYPE,
             'organism_id':force['interactor_%s_organism_id' % ab],
             'publication_id':pub_id,
             'unknown_participant_status':'active'}
            )
        up.load()

        p=Participant(
            {'participant_value':up.id(),
             'participant_type_id':UNKNOWN_PARTICIPANT_TYPE,
             'participant_status':'active'}
            )
        p.load()

        return p
    @classmethod
    def puke(cls,c):
        for force in c.fetchall():
            i=Interaction(
                {'publication_id':force['publication_id'],
                 'interaction_type':Interaction_type.factory('Protein-Protein').id(),
                 'interaction_status':'normal',
                 'interaction_source_id':Interaction_source.factory('BioGRID').id()}
                )
            i.row['publication_id']=i.pub2pub()
            i.store()
            i.force_attributes(cls,force['interaction_forced_id'])

            pub_id=i.pub2pub()
            foo=cls.get_participant(force,'A',pub_id)
            a_id=foo.id()
            a=Interaction_participant(
                {'interaction_id':i.id(),
                 'participant_id':a_id,
                 'participant_role_id':Participant_role.factory(BAIT).id(),
                 'status':'active'}
                )
            a.store()

            bar=cls.get_participant(force,'B',pub_id)
            b_id=bar.id()
            b=Interaction_participant(
                {'interaction_id':i.id(),
                 'participant_id':b_id,
                 'participant_role_id':Participant_role.factory(PREY).id(),
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
    '''The ids for IMS2 and IMS3 match for this table.'''
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
            global PARTICIPANT_TYPE
            PARTICIPANT_TYPE=Participant_type.factory('Gene').id()
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
''' % (Participant_role.factory(BAIT).id(),
       Participant_role.factory(PREY).id())
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

class Publication_history(BioGRID.ims.Publication_history,_Table):
    _rename={'modification_type':'progress_type'}
    @classmethod
    def ims2_table(cls):
        return 'progress'
    def __getitem__(self,name):
        if 'publication_id'==name:
            return self.pub2pub()
        return super(Publication_history,self).__getitem__(name)
    def store(self):
        if(0==self.row['user_id']):
            self.row['user_id']=DEFAULT_USER_ID
            self.warn('Setting user_id=0 to %s' % DEFAULT_USER_ID)

        try:
            return super(Publication_history,self).store()
        except _mysql_exceptions.OperationalError:
            pub_id=self.row['publication_id']
            self.warn('Skipping where PubMed ID is %s' % self.pubmed_id())
            #self.warn('Skipping where publication_id==%d' % self.row['publication_id'])
        except _mysql_exceptions.IntegrityError:
            pprint(self.row);
            sys.exit(1)


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

class Pubmed_mapping(BioGRID.ims.Pubmed_mapping,_Table):
    _rename={'publication_pubmed_id':'pubmed_id'}

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
    def __init__(self,passthru):
        super(Participant,self).__init__(passthru)
        global PARTICIPANT_TYPE
        PARTICIPANT_TYPE=Participant_type.factory('Gene').id()

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

class Participant_tag(BioGRID.ims.Participant_tag,_Table):
    _rename={'participant_tag_shortcode':'genetag_shortcode',
             'participant_tag_name':'genetag_name',
             'participant_tag_description':'genetag_description',
             'participant_tag_type_id':'genetag_type_id',
             'participant_tag_parent_id':'genetag_parent_id',
             'participant_tag_addeddate':'geentag_addeddate',
             'participant_tag_status':'genetag_status'}
    @classmethod
    def ims2_table(cls):
        return 'genetags'

class Participant_tag_type(BioGRID.ims.Participant_tag_type,_Table):
    _rename={'participant_tag_type_name':'genetag_type_name',
             'participant_tag_type_desc':'genetag_type_desc',
             'participant_tag_type_addeddate':'genetag_type_addeddate',
             'participant_tag_type_status':'genetag_type_status'}
    @classmethod
    def ims2_table(cls):
        return 'genetag_types'
    def __getitem__(self,name):
        if 'iplex_project_id'==name:
            return 1 # there in only one iplex_project
        else:
            return super(Participant_tag_type,self).__getitem__(name)

class Participant_tag_mapping(BioGRID.ims.Participant_tag_mapping,_Table):
    _rename={'participant_tag_id':'genetag_id',
            'participant_tag_evidence_type_id':'genetag_source_id',
            'participant_tag_evidence_value':'genetag_source_value',
             'participant_tag_mapping_addeddate':'genetag_mapping_addeddate',
             'participant_tag_mapping_status':'genetag_mapping_status'}
    @classmethod
    def ims2_table(cls):
        global PARTICIPANT_TYPE
        PARTICIPANT_TYPE=Participant_type.factory('Gene').id()
        return 'genetag_mappings'
    def __getitem__(self,name):
        if 'participant_id'==name:
            global PARTICIPANT_TYPE
            gene_id=self['gene_id']
            p_id=self.get_participant_id(gene_id,PARTICIPANT_TYPE)
            if None==p_id:
                p=Participant({
                        'participant_value':gene_id,
                        'participant_type_id':PARTICIPANT_TYPE
                        })
                p.store()
                p_id=p.id()
                self.warn('New Participant where gene_id=%s -> participant_id=%s' % (gene_id,p_id))
            return p_id
        elif 'participant_tag_evidence_value_text'==name:
            return None
        elif 'participant_tag_mapping_rank'==name:
            return None
        elif 'user_id'==name:
            return DEFAULT_USER_ID
        return super(Participant_tag_mapping,self).__getitem__(name)
    # def store(self):
    #     try:
    #         super(Participant_tag_mapping,self).store()
    #     except _mysql_exceptions.OperationalError:
    #         #self.warn('gene_id=%s ==> participant_id=%s' % (self['gene_id'],self['participant_id']))
    #         pprint(self.row)
    #         raise

class Participant_tag_evidence_type(BioGRID.ims.Participant_tag_evidence_type,_Table):
    _rename={'participant_tag_evidence_type_name':'genetag_source_name',
             'participant_tag_evidence_type_addeddate':'genetag_source_addeddate',
             'participant_tag_evidence_type_status':'genetag_source_status'}
    @classmethod
    def ims2_table(cls):
        return 'genetag_sources'
    

class Complex(BioGRID.ims._Table,_Table):
    """This table is only in IMS2, not IMS3. Data from it is now
    stored in the Interaction tables."""

    TABLE_PREFIX='complex'

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

    def ontology(self,i):
        """Writes complex_phenotypes and
        complex_phenotypes_qualifitation to the interaction_ontologies
        and interaction_ontology_qualifiers.  Needs to happend after
        all normal interactions are loaded as we don't what to change
        there IDs, but these get new IDs."""
        c=self.ims2_cursor()
        ims3_db=self.config.imsdb_name()

        sql='''SELECT complex_phenotype_id,
ontology_term_id,interaction_ontology_type_id
FROM complex_phenotypes
JOIN phenotypes AS pt USING(phenotype_id)
JOIN %(IMS3)s.ontology_terms AS ot ON(pt.phenotype_official_id=ot.ontology_term_official_id)
JOIN %(IMS3)s.interaction_ontology_types ON(flag=interaction_ontology_type_shortcode)
WHERE complex_id=%(ID)s''' % {'IMS3':ims3_db,'ID':self['complex_id']}
        c.execute(sql)
        cfts=c.fetchall() # cfts = complex_phenotypes
        if(0<len(cfts)):
            self.warn('Adding %s item(s) to interaction_ontology table' % len(cfts))
            io_ids={} # IMS2.complex_phenotype_id => IMS3.interaction_ontology_id
            for cft in cfts:
                io=Interaction_ontology(
                    {'interaction_id':i.id(),
                     'ontology_term_id':cft['ontology_term_id'],
                     'interaction_ontology_type_id':cft['interaction_ontology_type_id']})
                io.store()
                io_ids[cft['complex_phenotype_id']]=io.id()
                #self.warn(io_ids)

                if(0<len(io_ids)):
                    self.warn('Adding %s item(s) to Interaction_ontology_qualifiers table' % len(io_ids))
                    for complex_phenotype_id in io_ids:
                        interaction_ontology_id=io_ids[complex_phenotype_id]
                        sql='''SELECT
ot.ontology_term_id,
complex_phenotypes_qualifier_status AS status,
complex_phenotypes_qualifier_addeddate AS addeddate
FROM complex_phenotypes_qualifiers
JOIN phenotypes AS pt USING(phenotype_id)
JOIN %(IMS3)s.ontology_terms AS ot ON(pt.phenotype_official_id=ot.ontology_term_official_id)
WHERE complex_phenotype_id=%(ID)s''' % {'IMS3':ims3_db,'ID':complex_phenotype_id}
                        #self.warn(sql)
                        c.execute(sql)
                        for cptq in c.fetchall():
                            ioq=BioGRID.ims.Interaction_ontology_qualifier(
                                {'interaction_ontology_id':interaction_ontology_id,
                                 'ontology_term_id':cptq['ontology_term_id'],
                                 'interaction_ontology_qualifier_addeddate':cptq['addeddate'],
                                 'interaction_ontology_qualifier_status':cptq['status']})
                            ioq.store()


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
                {'publication_id':cpx.pub2pub(),
                 'interaction_type_id':complex_id,
                 'interaction_source_id':source_id})
            i.store()
            interaction_id=i.id()
            cpx.ontology(i)
            i.throughput(cpx.id(),'complex')

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
                    #print i.id()
                    log['interaction_id']=interaction_id
                    log['interaction_history_comment']=log['complex_history_comment']
                    log['interaction_history_date']=log['complex_history_date']
                    ih=Interaction_history(log)
                    ih.store()

                for note in cpx.notes():
                    note['interaction_id']=interaction_id
                    note['interaction_note_text']=note['complex_qualification']
                    note['interaction_note_status']=note['complex_qualification_status']
                    foo=BioGRID.ims.Interaction_note(note)
                    foo.store()

            raw=c.fetchone()


class Complex_forced_addition(BioGRID.ims._Table,_Table):
    """Slurps the IMS2 table inte the Interactions and Participants
    table."""

    TABLE_PREFIX='complex'

    @classmethod
    def puke(cls,c):
        complex_id=Interaction_type.factory('Complex').id()
        source_id=Interaction_source.factory('BioGRID').id()

        # loop thourght each forced complex
        raw=c.fetchone()
        while raw:

            
            cpx=Complex_forced_addition(raw)
            if 0==cpx['complex_organism_id']:
                # skip complex items with no organism specified
                cpx.warn('skipping where complex_organism_id=0')
            else:
                # Create the Interaction
                i=Interaction(
                    {'publication_id':cpx.pub2pub(),
                     'interaction_type_id':complex_id,
                     'interaction_source_id':source_id}
                    )
                i.store()
                interaction_id=i.id()

                # Loop proteins in the quick database
                for gene_id in cpx['complex_participants_success'].split('|'):
                    ip=Interaction_participant(
                        {'interaction_id':interaction_id,
                         'participant_id':i.get_participant_id(gene_id,PARTICIPANT_TYPE),
                         'participant_role_id':Participant_role.factory('unspecified').id(),
                         'interaction_participant_addeddate':cpx['complex_forced_timestamp'],
                         'interaction_participant_status':'active'}
                        )
                    ip.store()

                # Add unknown items
                for part in cpx['complex_participants_errors'].split('|'):
                    # add it to the fake quick table
                    up=Unknown_participant(
                        {'unknown_participant_identifier':part,
                         'participant_type_id':PARTICIPANT_TYPE,
                         'organism_id':raw['complex_organism_id'],
                         'publication_id':i['publication_id'],
                         'unknown_participant_status':'active'}
                        )
                    up.load()

                    # Write the participant...
                    p=Participant(
                        {'participant_value':up.id(),
                         'participant_type_id':UNKNOWN_PARTICIPANT_TYPE,
                         'participant_addeddate':cpx['complex_forced_timestamp'],
                         'participant_status':'active'}
                        )
                    # ...or fetch it actually.
                    p.load()

                    # add it to the interaction
                    ip=Interaction_participant(
                        {'interaction_id':interaction_id,
                         'participant_id':p.id(),
                         'participant_role_id':Participant_role.factory('unspecified').id(),
                         'interaction_participant_addeddate':cpx['complex_forced_timestamp'],
                         'interaction_participant_status':'active'}
                        )
                    ip.store()

                    i.force_attributes(cls,raw['complex_forced_id'])
                    
            raw=c.fetchone()
            



class Ontology(BioGRID.ims.Ontology,_Table):
    _rename={'ontology_name':'phenotype_ontology_name',
             'ontology_url':'phenotype_ontology_url',
             # we need to skip ontology_rootid for now as we need an
             #id from ontology_terms first.
             #'ontology_rootid':'phenotype_ontology_rootid',
             'ontology_addeddate':'phenotype_ontology_addeddate',
             'ontology_lastparsed':'phenotype_ontology_lastparsed',
             'ontology_status':'phenotype_ontology_status'}
    @classmethod
    def ims2_table(cls):
        return 'phenotypes_ontologies'

class Ontology_term(BioGRID.ims.Ontology_term,_Table):
    _rename={'ontology_term_official_id':'phenotype_official_id',
             'ontology_term_name':'phenotype_name',
             'ontology_term_desc':'phenotype_desc',
             'ontology_term_synonyms':'phenotype_synonyms',
             'ontology_term_replacement':'phenotype_replacement',
             'ontology_term_subsets':'phenotype_subsets',
             'ontology_term_preferred_name':'phenotype_preferred_name',
             'ontology_term_addeddate':'phenotype_addeddate',
             'ontology_term_status':'phenotype_status',
             'ontology_term_childcount':'phenotype_child_count',
             'ontology_term_parent':'phenotype_parents'}
    @classmethod
    def ims2_table(cls):
        return 'phenotypes'
    @classmethod
    def slurp_sql(cls):
        ims2_table=cls.ims2_table()
        return '''SELECT %s.*,ontology_id FROM %s
JOIN phenotypes_ontologies USING(phenotype_ontology_id)
JOIN %s.ontologies ON(phenotype_ontology_name=ontology_name)
''' % (ims2_table,ims2_table,cls.config.imsdb_name())

    @classmethod
    def fetchone(cls,c):
        """Removes peskey '-' and replaces them with None."""
        raw=c.fetchone()

        # if raw is false it's the end of the query.
        if raw:
            for i in raw:
                if '-'==raw[i]:
                    raw[i]=None
        return raw



    @classmethod
    def also(cls):
        c=cls.ims2_cursor()
        ims3_name=cls.config.imsdb_name()

        # Now we need to go and populate the ontologies.ontology_rootid
        another_c=cls.ims2_cursor()        
        sql='''UPDATE %s.ontologies,(
SELECT ontology_id,ontology_term_id
FROM phenotypes_ontologies
JOIN phenotypes ON(phenotype_ontology_rootid=phenotype_id)
JOIN %s.ontology_terms ON(phenotype_official_id=ontology_term_official_id)
)AS foo
SET ontology_rootid=ontology_term_id WHERE foo.ontology_id=%s.ontologies.ontology_id
''' % (ims3_name,ims3_name,ims3_name)
        another_c.execute(sql)

        # populate ontology_rootid then create the foreign key
        c.execute('ALTER TABLE %s.ontologies ADD FOREIGN KEY(ontology_rootid)REFERENCES ontology_terms(ontology_term_id)' % (ims3_name))

        return True

class Ontology_organism(BioGRID.ims.Ontology_organism,_Table):
    # We need to jump through a couple of hoops to get the new
    # ontology_ids.
    @classmethod
    def slurp_sql(cls):
        return '''SELECT organism_id,ontology_id
FROM phenotypes_organisms
JOIN phenotypes_ontologies ON(phenotype_ontology_rootid=phenotype_id)
JOIN %s.ontologies ON(phenotype_ontology_name=ontology_name)
''' % (cls.config.imsdb_name())

class Ontology_relationship(BioGRID.ims.Ontology_relationship,_Table):
    _rename={'ontology_relationship_type':'phenotype_relationship_type',
             'ontology_relationship_status':'phenotype_relationship_status'}
    @classmethod
    def slurp_sql(cls):
        limit=5000
        ims3_name=cls.config.imsdb_name()
        c=cls.ims2_cursor()
        c.execute('SELECT COUNT(*)AS count FROM phenotypes_relationships')
        total=c.fetchone()
        total=total['count']

        sql='''SELECT phenotype_relationship_id,phenotype_relationship_type,phenotype_relationship_status,
ontology_terms.ontology_term_id,op.ontology_term_id AS ontology_parent_id
FROM phenotypes_relationships
JOIN phenotypes USING(phenotype_id)
JOIN %(IMS3)s.ontology_terms ON(phenotypes.phenotype_official_id=ontology_terms.ontology_term_official_id)
JOIN phenotypes AS pp ON(phenotype_parent_id=pp.phenotype_id)
JOIN %(IMS3)s.ontology_terms AS op ON(pp.phenotype_official_id=op.ontology_term_official_id)
''' % {'IMS3':ims3_name}

        offset=0
        sqls=[]
        while(offset < total):
            sqls.append(sql + ' LIMIT %d OFFSET %d' % (limit,offset))
            offset+=limit
        warnings.warn("%d rows broken into %d pieces" % (total,len(sqls)))

        # Getting root nodes, I guess.
        sql='''SELECT phenotype_relationship_id,phenotype_relationship_type,phenotype_relationship_status,
ontology_terms.ontology_term_id,NULL AS ontology_parent_id
FROM phenotypes_relationships
JOIN phenotypes USING(phenotype_id)
JOIN %(IMS3)s.ontology_terms ON(phenotypes.phenotype_official_id=ontology_terms.ontology_term_official_id)
WHERE phenotype_parent_id=0''' % {'IMS3':ims3_name}
        sqls.append(sql)

        return sqls
    
global p_id2o_id
p_id2o_id={}

class Interaction_ontology(BioGRID.ims.Interaction_ontology,_Table):

    @classmethod
    def ims2_table(cls):
        return 'interaction_phenotypes'

    @classmethod
    def slurp_sql(cls):
        sql='''SELECT *
FROM %(table)s
JOIN phenotypes AS pt USING(phenotype_id)
JOIN %(IMS3)s.ontology_terms AS ot ON(pt.phenotype_official_id=ot.ontology_term_official_id)
JOIN interactions USING(interaction_id)
''' % {'table':cls.ims2_table(),'IMS3':cls.config.imsdb_name()}
        return sql

    def __getitem__(self,name):
        out=super(Interaction_ontology,self).__getitem__(name)
        if 'interaction_ontology_type_id'==name:
            try:
                flag=self.row['flag']
                out=BioGRID.ims.Interaction_ontology_type.factory(flag).id()
            except KeyError:
                pass
        return out

    def store(self):
        out=super(Interaction_ontology,self).store()
        p_id2o_id[self['interaction_phenotype_id']]=self.id();
        return out;

    def __eq__(self,other):
        '''For now, just return True.'''
        return True

class Interaction_ontology_qualifier(BioGRID.ims.Interaction_ontology_qualifier,_Table):
    @classmethod
    def slurp_sql(cls):
        # this one gets a new set of prymary keys
        return '''SELECT
interaction_phenotype_id,
ot.ontology_term_id,
interaction_phenotypes_qualifier_status AS interaction_ontology_qualifier_status,
interaction_phenotypes_qualifier_addeddate AS interaction_ontology_qualifier_addeddate
FROM interaction_phenotypes_qualifiers
JOIN phenotypes AS pt USING(phenotype_id)
JOIN %(IMS3)s.ontology_terms AS ot ON(pt.phenotype_official_id=ot.ontology_term_official_id)
''' % {'IMS3':cls.config.imsdb_name()}
    def store(self):
        try:
            self.row['interaction_ontology_id']=p_id2o_id[self.row['interaction_phenotype_id']]
        except KeyError:
            self.warn("Skipping interaction_phenotype_id=%d not in interaction_phenotypes" %
                      self.row['interaction_phenotype_id']);
            return

        try:
            return super(Interaction_ontology_qualifier,self).store()
        except _mysql_exceptions.IntegrityError as x:
            if 0!=str(x).count("FOREIGN KEY (`interaction_ontology_id`)"):
                self.warn("Skipping where interaction_phenotpyes_id=%d doesn't exist" % (self['interaction_ontology_id']))
            else:
                raise


class Dataset_queue(BioGRID.ims.Dataset_queue,_Table):
    _rename={'dataset_queue_filename':'dataset_queue_file',
            'dataset_queue_data':'dataset_queue_processed_data',
            'dataset_queue_interaction_count':'dataset_queue_interactions'}

class Experimental_system(BioGRID.ims._Table,_Table):
    '''What is really in the IMS2.experimental_systems table is
    hardcoded in the Ontology_term.sql file.  This exptract items from
    IMS2.interaction_matrix.experimental_system_id and plops them in
    the IMS3.interaciton_ontologies table.'''
    @classmethod
    def slurp_sql(cls):
        # Join ims3.interactions just to get get of bogus interactions
        # in ims.
        return '''SELECT interaction_id,ontology_term_id,interaction_history_date
FROM interaction_matrix
JOIN %(IMS3)s.interactions USING(interaction_id)
JOIN experimental_systems USING(experimental_system_id)
JOIN %(IMS3)s.ontology_terms ON(ontology_id=1 AND
 experimental_system_name=ontology_term_name)''' % {'IMS3':cls.config.imsdb_name()}
    def store(self):
        io=Interaction_ontology(
            {'interaction_id':self['interaction_id'],
             'ontology_term_id':self['ontology_term_id'],
             'interaction_ontology_addeddate':self['interaction_history_date']})
        io.load()
