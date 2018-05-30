### Python環境構築

1. pyenvをCloneする
```
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
```

1. bash_profileに環境変数を追記する  
```
# pyenv export  
export PYENV_ROOT=$HOME/.pyenv  
export PATH=$PYENV_ROOT/bin:$PATH  
eval "$(pyenv init -)"  
```

1. bash_profileを再読み込みする
```
source ~/.bash_profile
```

1. python 3.6.5 をインストールする
```
pyenv install 3.6.5  
```

1. 標準のpythonを3.6.5に変更する
```
pyenv global 3.6.5  
```

1. virtualenv / virtualenvwrapperのインストール
```
pip install virtualenv  
pip install virtualenvwrapper  
```

1. python仮想環境構築
```
virtualenv --no-site-packages 仮想環境名
```

1. 仮想環境を使う
```
source path/bin/activate
```

1. 仮想環境を終了する
```
deactivate
```
