#!/bin/bash

'''
Automatically renaming files.
'''

pwd

df_path=deploy/build # project subdirectory
df_newname=App.Dockerfile

if [[ -d ${df_path} ]]; then

    pushd ${df_path}

    for filename in *; do

        df_oldname=$(basename ${filename})

        if [[ ${filename} =~ (.Dockerfile)$ ]]; then
            
            echo "${filename} - OK"

        else

            echo "${filename}"
            
            if [[ ${df_oldname} == 'Dockerfile' ]]; then
                df_newname=App.${df_oldname}
            else
                df_newname=${df_oldname}.Dockerfile
            fi

            read -r -p "Do you want to rename ${filename} to ${df_newname}? [y/N] " response
            if [[ "$response" =~ ^(y|Y)$ ]]; then
                mv ${filename} ${df_path}/${df_newname}
                echo "Yes"
                echo
            else
                echo "No"
                echo
            fi

        fi

    done

    popd

else

    echo "! ${df_path} does not exist, skipping this project..."
    
fi
