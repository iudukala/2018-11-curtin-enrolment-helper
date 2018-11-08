#!/usr/bin/env bash

# installation script for mac 
# tested on macOS mojave
#

# todo:
# redirect output to log file instead of stdout

# ensuring no virtualenv is already active
deactivate 2> /dev/null

# initializing required variables
export PATH_MAIN_SOURCE="$HOME/Documents/Python"

export PATH_PROOT="$HOME/EnrolmentHelper_root"

export PATH_VIRTUALENV="$PATH_PROOT/virtualenv_EH"
export PATH_REPO="$PATH_MAIN_SOURCE/enrolment_helper"
# the name for the 
export NAME_VENV="ehvenv"

# write shell environment configuration data to a separate file instead of polluting the primary 
# config file (.bashrc/.zshrc)
export PATH_CONFIGFILE=$HOME/.ehexports
rm -f $PATH_CONFIGFILE


# make bash and zsh source that file everytime they starts up
echo "source $PATH_CONFIGFILE" >> $HOME/.bashrc >> $HOME/.zshrc

# adding the user specific install directory for python packages to $PATH
printf "export PATH=\$PATH:\$(python3 -m site --user-base)/bin\n" >> $PATH_CONFIGFILE
source $PATH_CONFIGFILE



# installing dependencies
brew install python3 pyenv mysql-server
xcode-select --install
# installing tools to the user install directory to minimizing global changees
pip3 install --user virtualenv virtualenvwrapper

# virtualenvwrapper required exports
{
  echo "export PATH_MAIN_SOURCE=$PATH_MAIN_SOURCE"
  # base location for new virtual environments
  echo "export WORKON_HOME=\$HOME/.virtualenvs"
  echo "export PROJECT_HOME=\$PATH_MAIN_SOURCE"
  # python interpreter to be to be used
  echo "export VIRTUALENVWRAPPER_PYTHON=$(which python3)"
  echo "export VIRTUALENVWRAPPER_VIRTUALENV=$(which virtualenv)"
  echo "export VIRTUALENVWRAPPER_WORKON_CD=1"

  # this line is printed without shell expansion so that even when a new subshell session is initiated
  # from an existing shell where a virtual environment is active, virtualenvwrapper has the path to the
  # python 3.x binary. if $(python3) is expanded when a venv is active, it will fail. this is stated explicitly
  # since usually dynamic expansions allow more flexibility with paths
  echo "source $(python3 -m site --user-base)/bin/virtualenvwrapper.sh"
} >> $PATH_CONFIGFILE

brew install openssl zlib sqlite
# macos required exports for python installs via pyenv - listed in an array
declare -a DEP_FLAGS=(openssl zlib sqlite);

# exporting CPPFLAGS and LDFLAGS needed to compile and install python via pyenv
for ITEM in ${DEP_FLAGS[@]}; do
  export BP_TEMP=$(brew --prefix $ITEM)
  export CPPFLAGS="${CPPFLAGS} -I${BP_TEMP}/include";
  export LDFLAGS="${LDFLAGS} -L${BP_TEMP}/lib"
  export PKG_CONFIG_PATH="${PKG_CONFIG_PATH} ${BP_TEMP}/lib/pkgconfig"
done




# backing up project repo folder if it already exists
if [ ! -d ${PATH_REPO}_bak ]; then
	mv $PATH_REPO ${PATH_REPO}_bak
fi

git clone https://iudukala@bitbucket.org/ComputingSEP/2018-11-enrolment-helper.git $PATH_REPO








# direnv setup for both bash and zsh
brew install direnv
printf """# shell hooks for bash/zsh
if [[ \$SHELL == *zsh ]]; then
  echo ZSH HOOK
  eval \"\$(direnv hook zsh)\"
  else
    if [[ \$SHELL == *bash ]]; then
      echo BASH HOOK
      eval \"\$(direnv hook bash)\"
    fi
fi
""" >> $PATH_CONFIGFILE

# installing the required python version
export PYTHON_VERSION='3.5.0'
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION


# dependency setup complete

if [[ $(python --version) = "Python $PYTHON_VERSION" ]]; then
  echo "Match"
fi

source $PATH_CONFIGFILE

mkvirtualenv -a $PATH_REPO -p $(pyenv root)/versions/$PYTHON_VERSION/bin/python ehvenv -r $PATH_REPO/requirements.txt
workon 
printf "Created virtualenv $NAME_VENV in $WORKON_HOME via virtualenvwrapper. Use \"workon $NAME_VENV\" to activate\n"




pip install -r $PATH_REPO/requirements.txt

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

# printing in color bash
# for code ($(seq 0 0 255)) print -P -- "$code: %F{$code}This is how your text would look like%f"
# brew install zsh-syntax-highlighting
# mysql -uroot -proot -e "select @@datadir;"
# mysql -uUSER -p -e 'SHOW VARIABLES WHERE Variable_Name LIKE "%dir"'