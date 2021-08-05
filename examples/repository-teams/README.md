# Repository teams


## Find repositories assigned to a team.

1. Repositories assigned to `t-ast`.
   Example:

    ```console
    github-util.py print-repository-names --topics-include=t-ast
    ```

1. Repositories assigned to `t-gdev`.
   Example:

    ```console
    github-util.py print-repository-names --topics-include=t-gdev
    ```

## Find repositories that aren't assigned to a team

Currently there are 3 teams identified by GitHub topics:  `t-ast`, `t-gdev`, `t-comm`.

1. List any repositories that do not belong to a team.
   Example:

    ```console
    github-util.py print-repository-names --topics-not-any=t-comm,t-ast,t-gdev
    ```