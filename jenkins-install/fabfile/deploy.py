# coding:utf-8
from fabric.api import local, env, lcd
from fabric.decorators import task
from ftplib import FTP
import os

class AutoDeploy(object):
    diffs = []
    # Git Check Reposotory Function
    def isExistGit(self):
        return os.path.exists(env.git_path + env.git_repository   + '.git')

    # Git Clone Function
    def clone(self):
        with lcd(env.git_path):
            local('git clone {}'.format(env.git))
        with lcd(env.git_path + env.git_repository):
            local('git checkout {}'.format(env.branch))
            ls = local('git ls-files', capture=True)
            self.diffs = ls.split('\n')

    # Git Pull Function
    def pull(sefl):
        with lcd(env.git_path + env.git_repository):
            local('git checkout {}'.format(env.branch))
            local('git pull')

    # Git Diff Check Function
    def diff(self):
        with lcd(env.git_path + env.git_repository):
            local('git checkout {}'.format(env.branch))
            ls = local('git diff --name-only HEAD..{}'.format(env.branch), capture=True)
            self.diffs = ls.split('\n')

    # Diff Test Function
    def test_diff(self):
        with lcd(env.git_path + env.git_repository):
            local('git checkout {}'.format(env.branch))
            ls = local('git ls-files', capture=True)
            self.diffs = ls.split('\n')

    # Deploy FTP Server Function
    def deploy(self):
        # ftp接続
        ftp = FTP(env.ftp_host, env.ftp_user, passwd=env.ftp_pass)

        # 差分のみアップロード
        for fileName in self.diffs:
            if fileName.find(env.ftp_ignore) < 0:
                # ftp パスをROOTに変更
                ftp.cwd('/')
                dirs = fileName.split('/')

                # ディレクトリ層の存在チェック
                if len(dirs) > 1:
                    i = 0
                    while len(dirs)-1 > i:
                        try:
                            # フォルダ作成
                            ftp.mkd(dirs[i])
                        except:
                            # 既に存在する場合は何もしない
                            pass
                        finally:
                            # そのフォルダに入る
                            ftp.cwd('./{}'.format(dirs[i]))
                            i+=1

                try:
                    with open(env.git_path + fileName, 'rb') as f:
                        # 差分ファイルアップロード
                        print('Upload File {}'.format(fileName))
                        ftp.storbinary("STOR {}".format(dirs[i]), f)
                except Exception as e:
                    # 差分ファイル削除
                    print(e)
                    print('Delete File {}'.format(fileName))
                    ftp.delete(dirs[i])


@task
def deploy_git():
    print('Auto Deploy to Git')
    ad = AutoDeploy()

    if ad.isExistGit():
        print('Pull git repository!')
        ad.pull()
    else:
        print('Clone git repository!')
        ad.clone()

@task
def deploy_ftp():
    print('Auto Deploy to FTP')
    ad = AutoDeploy()

    if ad.isExistGit():
        print('Diff & Pull git repository!')
        ad.diff()
        # ad.test_diff()
        ad.pull()
        ad.deploy()
    else:
        print('Clone git repository!')
        ad.clone()
        ad.deploy()
