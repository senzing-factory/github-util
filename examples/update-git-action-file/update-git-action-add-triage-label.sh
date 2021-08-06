#!/usr/bin/env bash

# Parameters for paths.

SENZING_GITHUB_UTIL_DIR=~/senzing.git/github-util
SENZING_GIT_REPOSITORY_DIR=~/senzing-test.git

# Parameters for github-util.py.

export SENZING_TOPICS_INCLUDED=test-ground

# Verify parameters.

if [ -z ${GITHUB_ACCESS_TOKEN+x} ]; then
    echo "GITHUB_ACCESS_TOKEN is not set.";
    exit
fi

# Make the directory to clone repositories into.

mkdir -p ${SENZING_GIT_REPOSITORY_DIR}


# BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null 2>&1 && pwd )"
# GIT_REPOSITORY_DIR="$(dirname ${BIN_DIR})"
# TARGET_PYTHON_DIR=${GIT_REPOSITORY_DIR}/g2/python

# Populate submodules.


# git pull
# git submodule update --init --recursive

# Process each submodule.

export REPOSITORIES=$(${SENZING_GITHUB_UTIL_DIR}/github-util.py print-repository-names)
for REPOSITORY in ${REPOSITORIES[@]};
do

    echo ${REPOSITORY}

    cd ${SENZING_GIT_REPOSITORY_DIR}
    git clone "git@github.com:Senzing/${REPOSITORY}.git"

    # Get requested version of submodule.

    # cd ${GIT_REPOSITORY_DIR}/${SUBMODULE_NAME}
    # git checkout main
    # git pull
    # git checkout ${SUBMODULE_VERSION}

    # echo "Copy ${SUBMODULE_NAME}/${SUBMODULE_ARTIFACT}"

    # Copy artifact into collection.

    # cd ${GIT_REPOSITORY_DIR}/${SUBMODULE_NAME}
    # cp ${SUBMODULE_ARTIFACT} ${TARGET_PYTHON_DIR}/

done
