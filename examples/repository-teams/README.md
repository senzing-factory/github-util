# Repository teams

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

## Find repositories assigned to a team

1. Repositories assigned to `t-ast`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/repository-teams
    ./github-util.py print-repository-names --topics-include=t-ast
    ```

1. Repositories assigned to `t-comm`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/repository-teams
    ./github-util.py print-repository-names --topics-include=t-comm
    ```

1. Repositories assigned to `t-g2-python`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/repository-teams
    ./github-util.py print-repository-names --topics-include=t-g2-python
    ```

1. Repositories assigned to `t-gdev`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/repository-teams
    ./github-util.py print-repository-names --topics-include=t-gdev
    ```

## Find repositories that aren't assigned to a team

Currently there are 4 teams identified by GitHub topics:  `t-ast`, `t-comm`, `t-g2-python`, `t-gdev`.

1. List any repositories that do not belong to a team and are not deprecated/archived/obsolete.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}/examples/repository-teams

    ./github-util.py print-repository-names \
      --topics-not-any=t-ast,t-comm,t-g2-python,t-gdev \
      --topics-exclude=archived,deprecated,obsolete
    ```
