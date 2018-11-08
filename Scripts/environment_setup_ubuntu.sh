#!/usr/bin/env bash

# Author: Isuru Udukala (19329914@student.curtin.edu)

# installation script for ubuntu (and other debian based flavors)
# tested on a clean install of Ubuntu 18.04.1
# should work on debian as well (not tested)
#
#

# ensuring no virtualenv is already active
deactivate 2> /dev/null

# reading bitbucket username to gain access to clone the repository
read -p "Bitbucket.org username: " USERNAME;

# installing dependencies
sudo apt-get update --assume-yes && sudo apt-get upgrade --assume-yes
sudo apt-get install --assume-yes python3-pip git make build-essential zlib1g-dev libbz2-dev liblzma-dev openssh-server \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev
# libssl1.0-dev is required for installing python versions before 3.5.0 while libssl-dev is required for 3.5.3 and after
# this is mentioned in [pyenv common build problems] @ https://github.com/pyenv/pyenv/wiki/common-build-problems
# sudo apt-get install --assume-yes libssl-dev 
sudo apt-get install --assume-yes libssl1.0-dev
# direnv to make activating virtualenvs easier
sudo apt-get install --assume yes direnv


# create a symlink /usr/bin/python to the installed python 3 binary since without it, pyenv won't detect a system default 
# version of python, making it impossible to switch back once pyenv has been activated
python < /dev/null > /dev/null 2>&1
if [ $? -gt 0 ]; then 
        sudo ln -s $(which python3) $(dirname $(which python3))/python
fi

# write environment configuration data to a separate file instead of polluting .bashrc
# and makes it easier to use with a different shell such as zsh (only 1 'source' command must be added to .zshrc)
export PATH_BASHRC_ALT="$HOME/.EH_exports"
rm -f $PATH_BASHRC_ALT
# make bash source that file everytime it starts up if it already doesn't
if [ ! grep -q "source $PATH_BASHRC_ALT" $HOME/.bashrc ]; then
    echo "source $PATH_BASHRC_ALT" >> $HOME/.bashrc
fi

#setting up pyenv
export PATH_PYENV="$HOME/.pyenv"
rm -rf $PATH_PYENV
git clone https://github.com/pyenv/pyenv.git $PATH_PYENV

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $PATH_BASHRC_ALT
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $PATH_BASHRC_ALT
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n\teval "$(pyenv init -)"\nfi' >> $PATH_BASHRC_ALT
source $PATH_BASHRC_ALT

#installing the required python version
export PYTHON_VERSION='3.5.0'
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION

#installing virtualenv
pip3 install --upgrade virtualenv


#setting up project directories
export PATH_PROOT="$HOME/EnrolmentHelper"
export PATH_VIRTUALENV="$PATH_PROOT/virtualenv"
export PATH_REPO="$PATH_PROOT/source"

# backing up project folder if it already exists
if [ ! -d ${PATH_PROOT}_bak ]; then
	mv $PATH_PROOT ${PATH_PROOT}_bak
fi

python3 -m virtualenv -p $(pyenv root)/versions/$PYTHON_VERSION/bin/python $PATH_VIRTUALENV
source $PATH_VIRTUALENV/bin/activate

pip3 install --upgrade setuptools wheel

rm -rf $PATH_REPO
git clone https://${USERNAME}@bitbucket.org/ComputingSEP/2018-11-enrolment-helper.git $PATH_REPO
# git clone https://iudukala@bitbucket.org/ComputingSEP/2018-11-enrolment-helper.git $PATH_REPO

sudo apt-get --assume-yes purge mysql*
sudo apt-get --assume-yes install mysql-server libmysqlclient-dev

pip3 install -r $PATH_REPO/requirements.txt

# configuring mysql server
export MYSQL_CONFIG_SCRIPT="$HOME/.EH_mysql_config.sql"
echo -n """
drop user 'root'@'localhost';
create user 'root'@'localhost' identified by 'root';
grant all privileges on *.* to 'root'@'localhost' with grant option;

create database Enrolment_Helper character set utf8;
create user 'enrolment_helperuser'@'localhost' identified by 'user';
grant all privileges on Enrolment_Helper.* to 'enrolment_helperuser'@'localhost';
grant all privileges on test_Enrolment_Helper.* to 'enrolment_helperuser'@'localhost';
""" > $MYSQL_CONFIG_SCRIPT;
sudo mysql -uroot < $MYSQL_CONFIG_SCRIPT;
rm $MYSQL_CONFIG_SCRIPT

python $PATH_REPO/manage.py migrate
python $PATH_REPO/manage.py makemigrations
python $PATH_REPO/manage.py populate_db
python $PATH_REPO/manage.py createsuperuser

printf "\nRepository path : $PATH_REPO\n";
printf "\nVirtualenv environment path : $PATH_VIRTUALENV\n"

# echo $(echo "AAAAAAAAAA" && echo "BBBBBBBBBBBB" >&2) 2>&1 > /dev/null | cat


# DOCUMENTATION AND SOURCE FOR TOOLS USED
#
# pyenv                  : https://github.com/pyenv/pyenv
# virtualenv        doc  : https://virtualenv.pypa.io/en/latest/
#                   src  : https://github.com/pypa/virtualenv
#
# virtualenvwrapper doc  : https://virtualenvwrapper.readthedocs.io/en/latest/index.html
# (not implemented yet)
#
# direnv            doc  : https://direnv.net/
#
#
#
