# github-util

## Overview

The [github-util.py](github-util.py) python script works with GitHub metadata.

To see all of the subcommands, run:

```console
$ ./github-util.py --help
usage: github-util.py [-h]
                      {print-git-clone,print-git-clone-mirror,print-repository-names,sleep,version,docker-acceptance-test}
                      ...

Reports from GitHub.

positional arguments:
  {print-git-clone,print-git-clone-mirror,print-repository-names,sleep,version,docker-acceptance-test}
                        Subcommands (GITHUB_SUBCOMMAND):
    print-git-clone     Print git clone https://...
    print-git-clone-mirror
                        Print git clone --mirror https://...
    print-repository-names
                        Print repository names.
    sleep               Do nothing but sleep. For Docker testing.
    version             Print version of program.
    docker-acceptance-test
                        For Docker acceptance testing.

optional arguments:
  -h, --help            show this help message and exit

```
