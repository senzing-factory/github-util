# github-util

## Overview

The [github-util.py] python script works with GitHub metadata.

To see all of the subcommands, run:

```console
$ ./github-util.py --help
usage: github-util.py [-h]
                      {print-copy-files-from-senzing-install,print-dependabot,print-git-clone,print-git-clone-mirror,print-repository-names,print-submodules-sh,sleep,update-dockerfiles,version,docker-acceptance-test}
                      ...

Reports from GitHub. For more information, see
https://github.com/Senzing/github-util

positional arguments:
  {print-copy-files-from-senzing-install,print-dependabot,print-git-clone,print-git-clone-mirror,print-repository-names,print-submodules-sh,sleep,update-dockerfiles,version,docker-acceptance-test}
                        Subcommands (SENZING_SUBCOMMAND):
    print-copy-files-from-senzing-install
                        Print copy-files-from-senzing-install.sh
    print-dependabot    Print dependabot alerts
    print-git-clone     Print git clone https://...
    print-git-clone-mirror
                        Print git clone --mirror https://...
    print-repository-names
                        Print repository names.
    print-submodules-sh
                        Print modules.sh
    sleep               Do nothing but sleep. For Docker testing.
    update-dockerfiles  Update Dockerfiles.
    version             Print version of program.
    docker-acceptance-test
                        For Docker acceptance testing.

optional arguments:
  -h, --help            show this help message and exit
```

## Usage

### Generate PR and Branch reports

1. Use `make` to run `github-util.py print-pull-requests` and `github-util.py print-branches` reports.
   Reports will be in the `target` directory.

  ```console
  make reports
  ```

[github-util.py]: github-util.py
