#!/usr/bin/env bash
cd ~

sudo apt-get update --assume-yes > /dev/null && sudo apt-get upgrade --assume-yes
sudo apt-get install --assume-yes python3-pip git make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
liblzma-dev openssh-server

# create a symlink /usr/bin/python to the installed python binary since without it, pyenv won't detect a 
# a system default version of python, making it impossible to switch back to the system version once 
# pyenv has been activated
python < /dev/null > /dev/null 2>&1
if [ $? -gt 0 ]; then 
        sudo ln -s $(which python3) $(dirname $(which python3))/python
fi

export PATH_PYENV="$HOME/.pyenv"
rm -rf $PATH_PYENV
git clone https://github.com/pyenv/pyenv.git $PATH_PYENV

export PATH_BASHRC_ALT="$HOME/.exports"
echo "source $PATH_BASHRC_ALT" >> $HOME/.bashrc

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $PATH_BASHRC_ALT
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $PATH_BASHRC_ALT
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n\teval "$(pyenv init -)"\nfi' >> $PATH_BASHRC_ALT
source $PATH_BASHRC_ALT

pyenv install 3.5.3
pyenv global 3.5.3

pip3 install --upgrade virtualenv

# backing up $PATH_BASHRC_ALT to .bashrc_bak if the backup does not already exist
if [ ! -f ${PATH_BASHRC_ALT}_bak ]; then
	cp $PATH_BASHRC_ALT ${PATH_BASHRC_ALT}_bak
fi

export PATH_VIRTUALENV="$HOME/enrhelp_virtualenv"
rm -rf $PATH_VIRTUALENV
python3 -m virtualenv $PATH_VIRTUALENV
source $PATH_VIRTUALENV/bin/activate

pip3 install --upgrade setuptools wheel
export PATH_REPO="$PATH_VIRTUALENV/enrhelp_repo"
git clone https://iudukala@bitbucket.org/ComputingSEP/2018-11-enrolment-helper.git $PATH_REPO

sudo apt-get --assume-yes purge mysql*
sudo apt-get --assume-yes install mysql-server libmysqlclient-dev

pip3 install -r $PATH_REPO/requirements.txt
deactivate

export MYSQL_TEMP_SCRIPT="$HOME/.mysql_server_config_file.sql"

echo -n """
drop user 'root'@'localhost';
create user 'root'@'localhost';
grant all privileges on *.* to 'root'@'localhost' with grant option;

create database Enrolment_Helper character set utf8;
create user 'enrolment_helperuser'@'localhost' identified by 'user';
grant all privileges on Enrolment_Helper.* to 'enrolment_helperuser'@'localhost';
""" > $MYSQL_TEMP_SCRIPT;
sudo mysql -uroot < $MYSQL_TEMP_SCRIPT;
rm $MYSQL_TEMP_SCRIPT



# echo $(echo "AAAAAAAAAA" && echo "BBBBBBBBBBBB" >&2) 2>&1 > /dev/null | cat
