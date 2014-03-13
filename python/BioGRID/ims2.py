"""Stuff to convert IMS2 database schema to IMS3"""
import BioGRID.ims

class Config(BioGRID.ims.Config):
    def ims2db(self):
        """Returns a MySQLdb pointer to the IMS2 database."""
        return self._db('ims2')

class Project(BioGRID.ims.Project):
    def __getitem__(self,name):
        """Overloaded to convert IMS3 names to IMS2 names."""
        if('project_addeddate'==name):
            name='project_timestamp'
        elif('project_status'==name):
            status=super(Project,self).__getitem__('project_status')
            if('open'==status):
                return 'public'
            else:
                return 'private'
        return super(Project,self).__getitem__(name)
        
        
class User(BioGRID.ims.User):
    pass

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
    ims2=cfg.ims2db() # not needed in --clean
    ims3=cfg.imsdb()

    for job in jobs:
        # First check for SQL files containing IMS3 schema
        file=open('%s/%s.sql' % (opts.sql_dir,job))
        if(opts.clean):
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

            # there doesn't really seem to be secure way to have dynamic
            # table names
            table_name='%ss' % job.lower()
            c.execute('SELECT * FROM %s' % table_name)

            raw=c.fetchone()
            Table=eval(job)
            while raw:
                cooked=Table(raw)
                cooked.store()
                raw=c.fetchone()
                ims3.commit()
