#!/bin/sh

mkdir -p $OSQA_PROJECTDIR
svn co http://svn.osqa.net/svnroot/osqa/trunk $OSQA_PROJECTDIR
cd $OSQA_PROJECTDIR

# We need python2.5 to be compatible with WSGI
python2.5 ~/utils/bin/pip install -E $OSQA_ENVDIR -r osqa-requirements.txt
source $OSQA_ENVDIR

# [Optional] If you want a MySQL database
easy_install-2.5 --prefix $OSQA_ENVDIR mysql-python