#!/bin/bash

echo "Processing test and comptest args..."

branch=gitlab-branch-name

git checkout master \
  && git pull \
  && git checkout -b ${branch}

if [[ -f "test.yml" ]]; then
    /usr/local/bin/_ct_args.py test.yml \
      && mv -v test.yml.new test.yml
fi

if [[ -f "ct-ci.yml" ]]; then
    /usr/local/bin/_ct_args.py ct-ci.yml \
      && mv -v ct-ci.yml.new ct-ci.yml
fi

git add . \
  && git commit -m "TASK: ct args, test args" \
  && git push --set-upstream origin ${branch}

echo "done"
