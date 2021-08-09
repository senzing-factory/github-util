# Update git action file

## Prerequisites

1. :pencil2: Set `GITHUB_ACCESS_TOKEN`.
   This is needed to access GitHub above the "public" limit.
   For information on how to obtain an access token, see
   [Creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

    ```console
    export GITHUB_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

## update-git-action-add-triage-label.sh

1. In `update-git-action-add-triage-label.sh`, modify:

    1. `ACTION_SOURCE_FILE`: Location of file to be copied into a repository's `.github/workflow` directory.
    1. `GIT_MESSAGE`:  The message used when commiting the change.
    1. `GIT_REPOSITORY_DIR`: A fresh directory where Git repositories can be cloned from GitHub.
    1. `GITHUB_UTIL_DIR`: Directory containing `github-util.py`.
    1. `SENZING_TOPICS_INCLUDED`: List of GitHub topics used to select repositories.

1. Run `update-git-action-add-triage-label.sh`.
   Example:

    ```console
    ./update-git-action-add-triage-label.sh
    ```
