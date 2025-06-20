# Update Git action file

## Prerequisites

1. Set these environment variable values:

   ```console
   export GIT_ACCOUNT=<GITHUB_ORG>
   export GIT_REPOSITORY=github-util
   export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
   export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
   ```

   - Where `GITHUB_ORG` is one of `senzing`, `senzing-garage`, or `senzing-factory`

1. :pencil2: Set `GITHUB_ACCESS_TOKEN`.
   This is needed to access GitHub above the "public" limit.
   For information on how to obtain an access token, see
   [Creating a personal access token].

   ```console
   export GITHUB_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

## add-to-project.sh

1. Run `add-to-project.sh` for `senzing-app-server`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

   export SENZING_TOPICS_INCLUDED=senzing-app-server
   export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-app-server.yaml

   ./add-to-project.sh
   ```

1. Run `add-to-project.sh` for `senzing-community`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

   export SENZING_TOPICS_INCLUDED=senzing-community
   export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-community.yaml

   ./add-to-project.sh
   ```

1. Run `add-to-project.sh` for `senzing-garage`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

   export SENZING_TOPICS_INCLUDED=senzing-garage
   export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-garage.yaml

   ./add-to-project.sh
   ```

1. Run `add-to-project.sh` for `senzing-g2-python`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

   export SENZING_TOPICS_INCLUDED=senzing-g2-python
   export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-g2-python.yaml

   ./add-to-project.sh
   ```

1. Run `add-to-project.sh` for `senzing-gdev`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

   export SENZING_TOPICS_INCLUDED=senzing-gdev
   export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-gdev.yaml

   ./add-to-project.sh
   ```

1. Run `add-to-project.sh` for `senzing-factory`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

   export SENZING_TOPICS_INCLUDED=senzing-factory
   export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-factory.yaml

   ./add-to-project.sh
   ```

[Creating a personal access token]: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
