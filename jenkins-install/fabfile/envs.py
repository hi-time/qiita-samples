# coding:utf-8
from fabric.api import env
from fabric.decorators import task

# @task
# def git_only():
#      # PG
#      env.environment = 'templete'
#      # Git
#      env.git = 'git@git.com:PROJECT/repository_name.git'
#      env.git_path = '/path/to/dir/'
#      env.git_repository = 'repository_name/'
#      env.branch = 'master'

# @task
# def ftp_deploy():
#      # PG
#      env.environment = 'templete'
#      # Git
#      env.git = 'git@git.com:PROJECT/repository_name.git'
#      env.git_path = '/path/to/dir/'
#      env.git_repository = 'repository_name/'
#      env.branch = 'master'
#
#      # FTP
#      env.ftp_host = 'YOUR_FTP_HOST'
#      env.ftp_user = 'YOUR_FTP_USER'
#      env.ftp_pass = 'YOUR_FTP_PASS'
#      env.ftp_ignore = '.git'
