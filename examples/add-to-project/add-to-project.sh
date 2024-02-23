#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# User modifications
# -----------------------------------------------------------------------------

# Internal parameters.

GITHUB_UTIL_DIR=~/senzing.git/github-util
GIT_REPOSITORY_DIR=~/senzing-test.git
GIT_MESSAGE="Add add-to-project.yaml"

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Verify parameters.

if [ -z ${GITHUB_ACCESS_TOKEN+x} ]; then
	echo "GITHUB_ACCESS_TOKEN is not set."
	exit
fi

# Make the directory to clone repositories into.

mkdir -p ${GIT_REPOSITORY_DIR}

# Process each submodule.

REPOSITORIES=$(${GITHUB_UTIL_DIR}/github-util.py print-repository-names)
for REPOSITORY in "${REPOSITORIES[@]}"; do
	echo "---- ${REPOSITORY} ------------------------------------------"

	DESTINATION_DIR=${GIT_REPOSITORY_DIR}/${REPOSITORY}/.github/workflows

	# Clone repository.

	cd ${GIT_REPOSITORY_DIR} || {
		echo "[ERROR] Failed to change directory"
		exit 1
	}
	git clone "git@github.com:Senzing/${REPOSITORY}.git"

	# Make repository directory the current working directory.

	cd ${GIT_REPOSITORY_DIR}/"${REPOSITORY}" || {
		echo "[ERROR] Failed to change directory"
		exit 1
	}

	# Checkout current main/main branch.

	git checkout main
	git checkout main
	git pull

	# Manipulate the files in the repository.

	mkdir -p "${DESTINATION_DIR}"
	cp "${ACTION_SOURCE_FILE}" "${DESTINATION_DIR}"

	# Add and commit all changes to local git repository.

	git add --all
	git commit -a -m "${GIT_MESSAGE}"

	# Push changes to GitHub

	git push

done
