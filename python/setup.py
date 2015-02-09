from distutils.core import setup
from glob import glob

setup(name='python-BioGRID-IMS',
      version='0.6',
      author='Sven Heinicke',
      author_email='sven@genomics.princeton.edu',
      url='http://wiki.thebiogrid.org/doku.php/interaction_management_system',
      packages=['BioGRID'],
      scripts=['ims22ims3'],

      # If share/ims/sql changes remember to change it in ims22ims3 too.
      data_files=[('share/ims/sql',glob('sql/*.sql'))]
      # Also, the SQL files are really in ../sql, but they get copied
      # by ../Makefile to ./sql in order to have bdist_rpm to
      # work. Generating the RPM files also needed MANIFEST.in
      # entries.
      )

