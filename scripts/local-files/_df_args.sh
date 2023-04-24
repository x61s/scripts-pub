#!/bin/bash

'''
Replacing `REGISTRY_URL` variable with external ARG
'''

pwd

is_git_tree=$(git rev-parse --is-inside-work-tree)

if [[ ${is_git_tree} ]]; then
    git branch
    git pull
else
    echo
    echo "This is not a GIT repository. Nothing to do here..."
    exit
fi

df_path=deploy/build # project subdirectory

if [[ -d ${df_path} ]]; then

    echo
    pushd ${df_path}

    for filename in *; do

        echo
        echo "${filename}"
        
        if [ -f "${filename}" ]; then
        
            (grep -q 'ARG REGISTRY_URL' ${filename})
            
            exit_code=$?
            
            if [[ ${exit_code} == 0 ]]; then
                echo "ARG REGISTRY_URL found"
            else
                echo "ARG REGISTRY_URL added"
                sed -i '1s/^/ARG REGISTRY_URL\n\n/' ${filename}
            fi

            old_registry=registry.project.company.net
            echo "Replacing ${old_registry} URL in ${filename}..."
            sed -i "s/${old_registry}/\${REGISTRY_URL}/g" ${filename}

            old_registry=nexus.project.company.net
            echo "Replacing ${old_registry} URL in ${filename}..."
            sed -i "s/${old_registry}/\${REGISTRY_URL}/g" ${filename}
            
            echo
            echo "///////////"
            echo
            cat ${filename}
            echo
            echo "///////////"
            echo
        
        else
            echo "${filename} is directory, skip it..."
        fi
        
    done

    echo "You are in: $(pwd)"
    git branch
    read -r -p "Commit? [y/N] " commit_response
    
    if [[ "$commit_response" =~ ^(y|Y)$ ]]; then
        git add .
        git commit -m "TASK: add ARG REGISRTY_URL to dockerfiles"
        git push
        echo "Yes"
        echo
    else
        echo "No"
        echo
    fi

    popd
    
    echo
    read -p "Press any key to resume ..."

else

    echo "! ${df_path} does not exist, skipping this project..."
    
fi
