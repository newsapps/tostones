from fabric.api import *

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
    env.s3_bucket = 'media.apps.chicagotribune.com'

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.s3_bucket = 'media-beta.tribapps.com'
    
"""
Commands - deployment
"""
def deploy():
    """
    Deploy built tables to S3.
    
    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    
    gzip_assets()
    deploy_to_s3()

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
    run('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s' % env)