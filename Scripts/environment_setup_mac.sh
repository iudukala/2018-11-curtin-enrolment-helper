#!/usr/bin/env bash

# installation script for mac 
# 
#

brew install pyenv

# write environment configuration data to a separate file instead of polluting .bashrc
export PATH_BASHRC_ALT="$HOME/.EH_exports"
rm -f $PATH_BASHRC_ALT
# make bash source that file everytime it starts up
echo "source $PATH_BASHRC_ALT" >> $HOME/.bashrc

source $PATH_BASHRC_ALT

#installing the required python version
export PYTHON_VERSION='3.5.0'
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION

#installing virtualenv
pip3 install --upgrade virtualenv

# backing up $PATH_BASHRC_ALT to .bashrc_bak if the backup does not already exist
if [ ! -f ${PATH_BASHRC_ALT}_bak ]; then
	cp $PATH_BASHRC_ALT ${PATH_BASHRC_ALT}_bak
fi

#setting up project directories
export PATH_PROOT="$HOME/EnrolmentHelper_root"
export PATH_VIRTUALENV="$PATH_PROOT/virtualenv_EH"
export PATH_REPO="$PATH_PROOT/source_EH"

# cleaning project root folder
mv $PATH_PROOT ${PATH_PROOT}_bak
python3 -m virtualenv -p $(pyenv root)/versions/$PYTHON_VERSION/bin/python $PATH_VIRTUALENV
source $PATH_VIRTUALENV/bin/activate

pip3 install --upgrade setuptools wheel

rm -rf $PATH_REPO
git clone https://iudukala@bitbucket.org/ComputingSEP/2018-11-enrolment-helper.git $PATH_REPO

sudo apt-get --assume-yes purge mysql*
sudo apt-get --assume-yes install mysql-server libmysqlclient-dev

pip3 install -r $PATH_REPO/requirements.txt

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


xcode-select --install
brew install openssl zlib sqlite
# macos required exports for python installs via pyenv
declare -a DEP_FLAGS=(zlib openssl sqlite);
# exporting CPPFLAGS and LDFLAGS
for ITEM in ${DEP_FLAGS[@]}; do
  export BP_TEMP=$(brew --prefix $ITEM)
  export CPPFLAGS="${CPPFLAGS} -I${BP_TEMP}/include";
  export LDFLAGS="${LDFLAGS} -L${BP_TEMP}/lib"
  export PKG_CONFIG_PATH="${PKG_CONFIG_PATH} ${BP_TEMP}/lib/pkgconfig"
done
