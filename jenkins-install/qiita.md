### Jenkins導入 in AWS

1. 必要なパッケージをインストール  
```
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo  
sudo rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key  
sudo yum install -y jenkins git  
```

1. 仮想環境内にFabric1.14をインストール(要python2.7環境)
```
pip install fabric==1.14.0
```

1. fabric1.14を実行できることを確認
```
$ fab -V
Fabric 1.14.0
Paramiko 1.15.1
```

1. jenkinsの接続URLを変更する
```
sudo vim /etc/sysconfig/jenkins
```
```
#以下の行を修正  
JENKINS_ARGS="--prefix=/jenkins"
```

1. Nginxのリバースプロキシを設定  
    * リバースプロキシ時のbasic認証に注意  
```
sudo vim /etc/nginx/sites-available/xxxxx.conf
```
```
upstream jenkins{  
    ip_hash;  
    server 127.0.0.1:8080;  
}  
server {  
    ...  
    location /jenkins {  
        proxy_pass http://jenkins;  
    }  
    ...  
}  
```

1. Jenkins上でsudoを使えるようにする
```
sudo visudo
```
以下を追記する
```
# sudo for Jenkins
Defaults:jenkins !requiretty
jenkins ALL=(ALL) NOPASSWD:ALL
```

1. jenkinsをnginxと同じグループに追加する
```
sudo gpasswd -a jenkins nginx
```

1. nginxとjenkinsを再起動
```
sudo service nginx restart  
sudo service jenkins restart  
```

1. jenkinsが起動している事を確認する
```
https://yourhost.com/jenkins
```

1. jenkinsの初期設定を行う
    * Administratorの初期パスワードコピーしてを入力する  
    ```
    sudo cat /var/lib/jenkins/secrets/initialAdminPassword  
    ```
    * Customize Jenkinsで導入するプラグインは左側のおすすめを一式いれておく  
    * プラグインのインストールが終わったら初期ユーザを登録する  
    * グローバルセキュリティのユーザ認証注意
    * CSRFを無効にする

1. ssh秘密鍵作成
```
ssh-keygen -t rsa  
```

1. id_rsa.pubをgitサーバのSSH公開鍵に登録する
```
vim ~/.ssh/config  
```
```
Host xxxx.git.server  
    HostName xxxx.git.server  
    IdentityFile ~/.ssh/id_rsa.xxxx.git.server
    User ユーザID  
```

1. sshで接続できるか確認する
```
ssh -T xxxx.git.server
```

1. 公開ディレクトリを作成する
```
cd /var/www/html/  
mkdir ./PROJECT  
```

1. jenkinsにJobを登録する
  * 新規ジョブ作成 -> ジョブの名前を設定 -> パイプラインでジョブを作成  
  * ビルドトリガ->リモートからビルドにチェックを入れる  
    * 認証トークを設定する  
  * パイプラインに以下を設定(定義はPipeline script)
    * gitから直公開の場合
    ```
    node {
        stage('git') {
            sh '/usr/local/bin/fab -f /usr/local/jenkins/fabfile/ envs.BRANCH deploy_git'
        }
    }
    ```

    * ftp公開の場合
    ```
    node {
        stage('ftp') {
            sh '/usr/local/bin/fab -f /usr/local/jenkins/fabfile/ envs.BRANCH deploy_ftp'
        }
    }
    ```

    * Nginxの再起動が必要な場合は以下を追記
    ```
    stage('nginx') {
        try {
            sh 'sudo service nginx stop'
        } catch(Exception e) {
            echo 'Stoppping Error'
        }finally {
            sh 'sudo service nginx start'
        }
    }
    ```

1. デプロイ用のFabfileを作成する
    * fabfile/deploy.py  
    * fabfile/envs.py  
    * fabfile/\__init__.py  
    内容は省略

    * 上記を/usr/local/jenkins/に配置する  

    * envs.pyにプロジェクト設定を追記する  
    gitのパスは __/__ まで記載すること
    repositoryにはcloneした際に作られるrepository名のフォルダを指定

    ```
    @task
    def templete():
         # PG
         env.environment = 'templete'
         # Git
         env.git = 'xxxx.git.server:PROJECT/repository_name.git'
         env.git_path = '/path/to/dir/'
         env.git_repository = 'repository_name/'
         env.branch = 'master'

         # FTP
         env.ftp_host = 'YOUR_FTP_HOST'
         env.ftp_user = 'YOUR_FTP_USER'
         env.ftp_pass = 'YOUR_FTP_PASS'
         env.ftp_ignore = '.git'
    ```

1. Jenkinsからビルドを実行してエラーが出ないことを確認する
    * よくあるエラー  
    (内容はJenkinsのコンソール出力から確認できる)  
    1. fabricの実行に失敗する  
        * fabricのバージョンが2.XX  
        * fabfileのパーミッションエラー
        * fabfileの配置位置が間違えている  
        * envsの記載にミスがある  
    1. gitのcloneまたはpullに失敗する  
        * フォルダのパーミッションエラー  
    1. webサーバの再起動に失敗する  
        * sudoコマンドが許可されていない
    1. FTPへのアップロードに失敗する  
        * 接続情報が間違えている
        * 接続IPが許可されていない
        * フォルダのパーミッションエラー


1. gitサーバのwebhookにjenkinsのURLを登録する
    * プロジェクト設定 -> git -> 編集 -> webフックURL
    ```
    http://yourhost.com/jenkins/job/JOB名/build?token=認証トークン
    ```
