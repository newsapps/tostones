from fabric.api import *

import config

"""
Base configuration
"""
env.project_name = 'tables'

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.s3_bucket = config.S3_PRODUCTION_BUCKET

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.s3_bucket = config.S3_STAGING_BUCKET
    
"""
Commands - deployment
"""
def deploy():
    """
    Deploy built tables to S3.
    
    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    
    build_tables()
    gzip_assets()
    deploy_to_s3()
    
def build_tables():
    """
    Rebuilds all tables.
    """
    local('rm -rf out')
    local('table-setter build . -p tables')
    local('python rename_tables.py')

def runserver():
    """
    Runs local dev server
    """
    # local('table-setter start out/tables') # breaks for some reason
    local('cd out; python -m SimpleHTTPServer')

def build_and_run():
    """
    Rebuilds all tables and runs local dev server
    """
    build_tables()
    runserver()

def gzip_assets():
    """
    GZips every file in the assets directory and places the new file
    in the gzip directory with the same filename.
    """
    local('python gzip_assets.py')

def deploy_to_s3():
    """
    Deploy the latest built tables to S3.
    """
    env.gzip_path = 'gzip/tables/'
    local(('s3cmd -P --add-header=Content-encoding:gzip --guess-mime-type sync %(gzip_path)s s3://%(s3_bucket)s/%(project_name)s/') % env)

"""
Deaths, destroyers of worlds
"""
def shiva_the_destroyer():
    """
    Remove all directories, databases, etc. associated with the application.
    """
    require('settings', provided_by=[production, staging])
    
    local('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s' % env)