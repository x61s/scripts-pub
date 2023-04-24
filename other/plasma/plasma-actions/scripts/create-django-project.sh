#!/bin/bash

sec=5

echo "Press CTRL+C to cancel operation..."

while [ $sec -ge 0 ]; do
    echo -ne "${sec} "
    let "sec=${sec}-1"
    sleep 1
done

echo "Waiting for user input..."

projectname=$(kdialog --title "Django project name" --inputbox "Please enter the Django project name:")

if [ -z "${projectname}" ]; then
echo "ERROR: Empty name! You can close this terminal window."
exit
fi

mkdir -p \
  $1/${projectname}

cp -rv \
  ${HOME}/.local/share/gitignore-templates/.gitignore-python \
  ./.gitignore

pushd $1/${projectname}

/usr/bin/python3 -m venv venv

source ./venv/bin/activate

pip install django
django-admin startproject ${projectname}

kdialog --title "Development server" --yesno "Do you want to run develpoment server right now?"
if [ $? = 0 ]; then
python3 ${projectname}/manage.py migrate
python3 ${projectname}/manage.py runserver
fi

deactivate

popd

cat << EOF > README.txt
ACTIVATE virtual environment:
$ cd ./${projectname}
$ . ./venv/bin/activate

RUN development application server in virtual environment:
$ python3 ./${projectname}/manage.py runserver

DEACTIVATE virtual environment:
$ deactivate

To create git repository:
$ git init
$ git branch -m main
$ git add .
$ git config user.email "arinov.ilyas@gmail.com"
$ git config user.name "Ilyas B Arinov"
$ git commit -m "init commit"
$ git remote add origin git@github.com:x61s/${projectname}.git
$ git push -u origin main
EOF

echo "Done. You can close this terminal window!"
