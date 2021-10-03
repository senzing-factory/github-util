# Update git action file

## Prerequisites

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing
    export GIT_REPOSITORY=github-util
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. :pencil2: Set `GITHUB_ACCESS_TOKEN`.
   This is needed to access GitHub above the "public" limit.
   For information on how to obtain an access token, see
   [Creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

    ```console
    export GITHUB_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

## add-to-project.sh

1. Run `add-to-project.sh` for `t-ast`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

    export SENZING_TOPICS_INCLUDED=t-ast
    export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-t-ast.yaml

    ./add-to-project.sh
    ```

1. Run `add-to-project.sh` for `t-comm`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

    export SENZING_TOPICS_INCLUDED=t-comm
    export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-t-comm.yaml

    ./add-to-project.sh
    ```

1. Run `add-to-project.sh` for `t-g2-python`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

    export SENZING_TOPICS_INCLUDED=t-g2-python
    export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-t-g2-python.yaml

    ./add-to-project.sh
    ```

1. Run `add-to-project.sh` for `t-gdev`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/add-to-project

    export SENZING_TOPICS_INCLUDED=t-gdev
    export ACTION_SOURCE_FILE=~/senzing.git/github-util/examples/add-to-project/add-to-project-t-gdev.yaml

    ./add-to-project.sh
    ```
