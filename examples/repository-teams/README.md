# Repository teams

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

## Find repositories assigned to a team

1. Repositories assigned to `senzing-app-server`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}
   ./github-util.py print-repository-names --topics-include=senzing-app-server
   ```

1. Repositories assigned to `senzing-g2-python`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}
   ./github-util.py print-repository-names --topics-include=senzing-g2-python
   ```

1. Repositories assigned to `senzing-garage`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}
   ./github-util.py print-repository-names --topics-include=senzing-garage
   ```

1. Repositories assigned to `senzing-gdev`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}
   ./github-util.py print-repository-names --topics-include=senzing-gdev
   ```

1. Repositories assigned to `senzing-factory`.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}
   ./github-util.py print-repository-names --topics-include=senzing-factory
   ```

## Find repositories that aren't assigned to a team

Currently there are 4 teams identified by GitHub topics: `senzing-app-server`, `senzing`, `senzing-g2-python`, `senzing-garage`, `senzing-gdev`, `senzing-factory`.

1. List any repositories that do not belong to a team and are not deprecated/archived/obsolete.
   Example:

   ```console
   cd ${GIT_REPOSITORY_DIR}

   ./github-util.py print-repository-names \
     --topics-not-any=senzing,senzing-app-server,senzing-g2-python,senzing-garage,senzing-gdev,senzing-factory \
     --topics-exclude=archived,deprecated,obsolete
   ```

[Creating a personal access token]: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
