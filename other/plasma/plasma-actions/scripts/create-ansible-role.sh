#!/bin/bash

rolename=$(kdialog --title "Role name" --inputbox "Please enter the ansible role name:")

mkdir -p \
  $1/${rolename}/{tasks,templates,handlers,files}

touch $1/${rolename}/tasks/{main,install,configure}.yml
