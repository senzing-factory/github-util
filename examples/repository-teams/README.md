# Repository teams

## Find repositories assigned to a team

1. Repositories assigned to `t-ast`.
   Example:

    ```console
    github-util.py print-repository-names --topics-include=t-ast
    ```

1. Repositories assigned to `t-comm`.
   Example:

    ```console
    github-util.py print-repository-names --topics-include=t-comm
    ```

1. Repositories assigned to `t-g2-python`.
   Example:

    ```console
    github-util.py print-repository-names --topics-include=t-g2-python
    ```

1. Repositories assigned to `t-gdev`.
   Example:

    ```console
    github-util.py print-repository-names --topics-include=t-gdev
    ```

## Find repositories that aren't assigned to a team

Currently there are 3 teams identified by GitHub topics:  `t-ast`, `t-comm`, `t-g2-python`, `t-gdev`.

1. List any repositories that do not belong to a team and are not deprecated/archived/obsolete.
   Example:

    ```console
    github-util.py print-repository-names \
      --topics-not-any=t-ast,t-comm,t-g2-python,t-gdev \
      --topics-exclude=archived,deprecated,obsolete
    ```
