#! /usr/bin/env python3

'''
# -----------------------------------------------------------------------------
# github-util.py
#
# Work with GitHub.
#
# References:
# - GitHub
#   - https://github.com/PyGithub/PyGithub
#   - https://pygithub.readthedocs.io/
#   - https://pygithub.readthedocs.io/en/latest/github_objects.html
# -----------------------------------------------------------------------------
'''

# Import from standard library. https://docs.python.org/3/library/

import argparse
import base64
import copy
import json
import linecache
import logging
import os
import re
import signal
import sys
import time

# Import from https://pypi.org/

import requests
from github import Github

__all__ = []
__version__ = "1.4.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2020-03-12'
__updated__ = '2022-05-17'

# See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-product-ids.md

SENZING_PRODUCT_ID = "5012"
LOG_FORMAT = '%(asctime)s %(message)s'

# Working with bytes.

KILOBYTES = 1024
MEGABYTES = 1024 * KILOBYTES
GIGABYTES = 1024 * MEGABYTES

# The "configuration_locator" describes where configuration variables are in:
# 1) Command line options, 2) Environment variables, 3) Configuration files, 4) Default values

CONFIGURATION_LOCATOR = {
    "configuration_file": {
        "default": None,
        "env": "GITHUB_CONFIGURATION_FILE",
        "cli": "github-configuration-file"
    },
    "debug": {
        "default": False,
        "env": "SENZING_DEBUG",
        "cli": "debug"
    },
    "github_access_token": {
        "default": None,
        "env": "GITHUB_ACCESS_TOKEN",
        "cli": "github-access-token"
    },
    "is_user": {
        "default": False,
        "env": "SENZING_IS_USER",
        "cli": "is-user"
    },
    "organization": {
        "default": "Senzing",
        "env": "GITHUB_ORGANIZATION",
        "cli": "organization"
    },
    "print_format": {
        "default": "{0}",
        "env": "SENZING_PRINT_FORMAT",
        "cli": "print-format"
    },
    "sleep_time_in_seconds": {
        "default": 0,
        "env": "SENZING_SLEEP_TIME_IN_SECONDS",
        "cli": "sleep-time-in-seconds"
    },
    "sleep_time_in_seconds_dockerfiles": {
        "default": 10,
        "env": "SENZING_SLEEP_TIME_IN_SECONDS_DOCKERFILES",
        "cli": "sleep-time-in-seconds-dockerfiles"
    },
    "topics_all": {
        "default": "",
        "env": "SENZING_TOPICS_ALL",
        "cli": "topics-all"
    },
    "topics_any": {
        "default": "",
        "env": "SENZING_TOPICS_ANY",
        "cli": "topics-any"
    },
    "topics_excluded": {
        "default": "",
        "env": "SENZING_TOPICS_EXCLUDED",
        "cli": "topics-excluded"
    },
    "topics_included": {
        "default": "",
        "env": "SENZING_TOPICS_INCLUDED",
        "cli": "topics-included"
    },
    "topics_not_all": {
        "default": "",
        "env": "SENZING_TOPICS_NOT_ALL",
        "cli": "topics-not-all"
    },
    "topics_not_any": {
        "default": "",
        "env": "SENZING_TOPICS_NOT_ANY",
        "cli": "topics-not-any"
    },
    "subcommand": {
        "default": None,
        "env": "SENZING_SUBCOMMAND",
    }
}

# Enumerate keys in 'configuration_locator' that should not be printed to the log.

KEYS_TO_REDACT = [
    "github_access_token",
]

G2_REPOSITORIES = {
    "compressedfile": {
        "artifacts": ["CompressedFile.py"]
    },
    "dumpstack": {
        "artifacts": ["DumpStack.py"]
    },
    "g2audit": {
        "artifacts": ["G2Audit.py"]
    },
    "g2command": {
        "artifacts": ["G2Command.py"]
    },
    "g2config": {
        "artifacts": ["G2Config.py"]
    },
    "g2configmgr": {
        "artifacts": ["G2ConfigMgr.py"]
    },
    "g2configtables": {
        "artifacts": ["G2ConfigTables.py"]
    },
    "g2configtool": {
        "artifacts": ["G2ConfigTool.py", "G2ConfigTool.readme"]
    },
    "g2createproject": {
        "artifacts": ["G2CreateProject.py"]
    },
    "g2database": {
        "artifacts": ["G2Database.py"]
    },
    "g2diagnostic": {
        "artifacts": ["G2Diagnostic.py"]
    },
    "g2engine": {
        "artifacts": ["G2Engine.py"]
    },
    "g2exception": {
        "artifacts": ["G2Exception.py"]
    },
    "g2explorer": {
        "artifacts": ["G2Explorer.py"]
    },
    "g2export": {
        "artifacts": ["G2Export.py"]
    },
    "g2health": {
        "artifacts": ["G2Health.py"]
    },
    "g2hasher": {
        "artifacts": ["G2Hasher.py"]
    },
    "g2iniparams": {
        "artifacts": ["G2IniParams.py"]
    },
    "g2loader": {
        "artifacts": ["G2Loader.py"]
    },
    "g2paths": {
        "artifacts": ["G2Paths.py"]
    },
    "g2product": {
        "artifacts": ["G2Product.py"]
    },
    "g2project": {
        "artifacts": ["G2Project.py"]
    },
    "g2s3": {
        "artifacts": ["G2S3.py"]
    },
    "g2setupconfig": {
        "artifacts": ["G2SetupConfig.py"]
    },
    "g2snapshot": {
        "artifacts": ["G2Snapshot.py"]
    },
    "g2updateproject": {
        "artifacts": ["G2UpdateProject.py"]
    }
}

ETC_FILES = [
    "demo",
    "g2purge.umf",
    "governor_postgres_xid.py",
]

# -----------------------------------------------------------------------------
# Define argument parser
# -----------------------------------------------------------------------------


def get_parser():
    ''' Parse commandline arguments. '''

    subcommands = {
        'print-branches': {
            "help": 'Print branches',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'print-copy-files-from-senzing-install': {
            "help": 'Print copy-files-from-senzing-install.sh',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'print-dependabot': {
            "help": 'Print dependabot alerts',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'print-git-clone': {
            "help": 'Print git clone https://...',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'print-git-clone-mirror': {
            "help": 'Print git clone --mirror https://...',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'print-pull-requests': {
            "help": 'Print pull requests',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'print-repository-names': {
            "help": 'Print repository names.',
            "argument_aspects": ["common", "print"],
            "arguments": {
                "--is-user": {
                    "dest": "is_user",
                    "metavar": "SENZING_IS_USER",
                    "help": "Use a GitHub User, not GitHub Organization. DEFAULT: 'False' (not a user)"
                },
                "--topics-all": {
                    "dest": "topics_all",
                    "metavar": "SENZING_TOPICS_ALL",
                    "help": "All repository topics must be present. DEFAULT: '' (no evaluation)"
                },
                "--topics-any": {
                    "dest": "topics_any",
                    "metavar": "SENZING_TOPICS_ANY",
                    "help": "Any repository topics must be present. DEFAULT: '' (no evaluation)"
                },
                "--topics-excluded": {
                    "dest": "topics_excluded",
                    "metavar": "SENZING_TOPICS_EXCLUDED",
                    "help": "Which repository topics to exclude. DEFAULT: '' (exclude none)"
                },
                "--topics-included": {
                    "dest": "topics_included",
                    "metavar": "SENZING_TOPICS_INCLUDED",
                    "help": "Which repository topics to include. DEFAULT: '' (include all)"
                },
                "--topics-not-all": {
                    "dest": "topics_not_all",
                    "metavar": "SENZING_TOPICS_NOT_ALL",
                    "help": "All repository topics are bit present. DEFAULT: '' (no evaluation)"
                },
                "--topics-not-any": {
                    "dest": "topics_not_any",
                    "metavar": "SENZING_TOPICS_NOT_ANY",
                    "help": "Any repository topics is not present. DEFAULT: '' (no evaluation)"
                },
            },
        },
        'print-submodules-sh': {
            "help": 'Print modules.sh',
            "argument_aspects": ["common"],
            "arguments": {},
        },
        'sleep': {
            "help": 'Do nothing but sleep. For Docker testing.',
            "arguments": {
                "--sleep-time-in-seconds": {
                    "dest": "sleep_time_in_seconds",
                    "metavar": "SENZING_SLEEP_TIME_IN_SECONDS",
                    "help": "Sleep time in seconds. DEFAULT: 0 (infinite)"
                },
            },
        },
        'update-dockerfiles': {
            "help": 'Update Dockerfiles.',
            "argument_aspects": ["common"],
            "arguments": {
                "--configuration-file": {
                    "dest": "configuration_file",
                    "metavar": "SENZING_CONFIGURATION_FILE",
                    "help": "Configuration file. DEFAULT: None"
                },
                "--sleep-time-in-seconds-dockerfiles": {
                    "dest": "sleep_time_in_seconds_dockerfiles",
                    "metavar": "SENZING_SLEEP_TIME_IN_SECONDS_DOCKERFILES",
                    "help": "Sleep time in seconds. DEFAULT: 10 seconds"
                },
            },
        },
        'version': {
            "help": 'Print version of program.',
        },
        'docker-acceptance-test': {
            "help": 'For Docker acceptance testing.',
        },
    }

    # Define argument_aspects.

    argument_aspects = {
        "common": {
            "--debug": {
                "dest": "debug",
                "action": "store_true",
                "help": "Enable debugging. (SENZING_DEBUG) Default: False"
            },
            "--github-access-token": {
                "dest": "github_access_token",
                "metavar": "GITHUB_ACCESS_TOKEN",
                "help": "GitHub Personal Access token. See https://github.com/settings/tokens"
            },
            "--organization": {
                "dest": "organization",
                "metavar": "GITHUB_ORGANIZATION",
                "help": "GitHub account/organization name."
            },
        },
        "print": {
            "--print-format": {
                "dest": "print_format",
                "metavar": "SENZING_PRINT_FORMAT",
                "help": "Format of output. Default: '{0}'"
            },
        },
    }

    # Augment "subcommands" variable with arguments specified by aspects.

    for subcommand, subcommand_value in subcommands.items():
        if 'argument_aspects' in subcommand_value:
            for aspect in subcommand_value['argument_aspects']:
                if 'arguments' not in subcommands[subcommand]:
                    subcommands[subcommand]['arguments'] = {}
                arguments = argument_aspects.get(aspect, {})
                for argument, argument_value in arguments.items():
                    subcommands[subcommand]['arguments'][argument] = argument_value

    parser = argparse.ArgumentParser(
        description="Reports from GitHub. For more information, see https://github.com/Senzing/github-util")
    subparsers = parser.add_subparsers(
        dest='subcommand', help='Subcommands (SENZING_SUBCOMMAND):')

    for subcommand_key, subcommand_values in subcommands.items():
        subcommand_help = subcommand_values.get('help', "")
        subcommand_arguments = subcommand_values.get('arguments', {})
        subparser = subparsers.add_parser(subcommand_key, help=subcommand_help)
        for argument_key, argument_values in subcommand_arguments.items():
            subparser.add_argument(argument_key, **argument_values)

    return parser

# -----------------------------------------------------------------------------
# Message handling
# -----------------------------------------------------------------------------

# 1xx Informational (i.e. logging.info())
# 3xx Warning (i.e. logging.warning())
# 5xx User configuration issues (either logging.warning() or logging.err() for Client errors)
# 7xx Internal error (i.e. logging.error for Server errors)
# 9xx Debugging (i.e. logging.debug())


MESSAGE_INFO = 100
MESSAGE_WARN = 300
MESSAGE_ERROR = 700
MESSAGE_DEBUG = 900

MESSAGE_DICTIONARY = {
    "100": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}I",
    "101": "Added   Repository: {0} Label: {1}",
    "102": "Updated Repository: {0} Label: {1}",
    "103": "Deleted Repository: {0} Label: {1}",
    "104": "Repository '{0}' has been archived.  Not modifying its labels.",
    "120": "Processing Repository: {0}",
    "121": "  Created branch: {0}",
    "122": "  Processing file: {0}",
    "123": "  Created pull request: {0}",
    "124": "  Skipping",
    "125": "  resolved_properties: {0}",
    "126": "  No changes in repository '{0}'.",
    "140": "Changed repositories: {0}",
    "293": "For information on warnings and errors, see https://github.com/Senzing/github-util",
    "294": "Version: {0}  Updated: {1}",
    "295": "Sleeping infinitely.",
    "296": "Sleeping {0} seconds.",
    "297": "Enter {0}",
    "298": "Exit {0}",
    "299": "{0}",
    "300": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}W",
    "350": "  Branch '{0}' already exists. Reusing it. Ref: {1}; Exception: {2}",
    "351": "  Pull request already exists for '{0}'. Exception: {1}",
    "499": "{0}",
    "500": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "696": "Bad SENZING_SUBCOMMAND: {0}.",
    "697": "No processing done.",
    "698": "Program terminated with error.",
    "699": "{0}",
    "700": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "701": "GITHUB_ACCESS_TOKEN is required",
    "899": "{0}",
    "900": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}D",
    "998": "Debugging enabled.",
    "999": "{0}",
}


def message(index, *args):
    ''' Return an instantiated message. '''
    index_string = str(index)
    template = MESSAGE_DICTIONARY.get(index_string, "No message for index {0}.".format(index_string))
    return template.format(*args)


def message_generic(generic_index, index, *args):
    ''' Return a formatted message. '''
    return "{0} {1}".format(message(generic_index, index), message(index, *args))


def message_info(index, *args):
    ''' Return an info message. '''
    return message_generic(MESSAGE_INFO, index, *args)


def message_warning(index, *args):
    ''' Return a warning message. '''
    return message_generic(MESSAGE_WARN, index, *args)


def message_error(index, *args):
    ''' Return an error message. '''
    return message_generic(MESSAGE_ERROR, index, *args)


def message_debug(index, *args):
    ''' Return a debug message. '''
    return message_generic(MESSAGE_DEBUG, index, *args)


def get_exception():
    ''' Get details about an exception. '''
    exception_type, exception_object, traceback = sys.exc_info()
    frame = traceback.tb_frame
    line_number = traceback.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_number, frame.f_globals)
    return {
        "filename": filename,
        "line_number": line_number,
        "line": line.strip(),
        "exception": exception_object,
        "type": exception_type,
        "traceback": traceback,
    }

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------


def get_configuration(subcommand, args):
    ''' Order of precedence: CLI, OS environment variables, INI file, default. '''
    result = {}

    # Copy default values into configuration dictionary.

    for key, value in list(CONFIGURATION_LOCATOR.items()):
        result[key] = value.get('default', None)

    # "Prime the pump" with command line args. This will be done again as the last step.

    for key, value in list(args.__dict__.items()):
        new_key = key.format(subcommand.replace('-', '_'))
        if value:
            result[new_key] = value

    # Copy OS environment variables into configuration dictionary.

    for key, value in list(CONFIGURATION_LOCATOR.items()):
        os_env_var = value.get('env', None)
        if os_env_var:
            os_env_value = os.getenv(os_env_var, None)
            if os_env_value:
                result[key] = os_env_value

    # Copy 'args' into configuration dictionary.

    for key, value in list(args.__dict__.items()):
        new_key = key.format(subcommand.replace('-', '_'))
        if value:
            result[new_key] = value

    # Add program information.

    result['program_version'] = __version__
    result['program_updated'] = __updated__

    # Special case: subcommand from command-line

    if args.subcommand:
        result['subcommand'] = args.subcommand

    # Special case: Change boolean strings to booleans.

    booleans = [
        'debug',
        'is_user',
    ]
    for boolean in booleans:
        boolean_value = result.get(boolean)
        if isinstance(boolean_value, str):
            boolean_value_lower_case = boolean_value.lower()
            if boolean_value_lower_case in ['true', '1', 't', 'y', 'yes']:
                result[boolean] = True
            else:
                result[boolean] = False

    # Special case: Change integer strings to integers.

    integers = [
        'sleep_time_in_seconds',
        'sleep_time_in_seconds_dockerfiles'
    ]
    for integer in integers:
        integer_string = result.get(integer)
        result[integer] = int(integer_string)

    # Special case: Turn string to list

    topic_list = [
        "topics_all",
        "topics_any",
        "topics_excluded",
        "topics_included",
        "topics_not_all",
        "topics_not_any"
    ]

    for topic in topic_list:
        if result.get(topic):
            result["{0}_list".format(topic)] = result.get(topic).split(',')

    return result


def validate_configuration(config):
    ''' Check aggregate configuration from commandline options, environment variables, config files, and defaults. '''

    user_warning_messages = []
    user_error_messages = []

    # Perform subcommand specific checking.

    subcommand = config.get('subcommand')

    if subcommand in ['comments']:

        if not config.get('github_access_token'):
            user_error_messages.append(message_error(701))

    # Log warning messages.

    for user_warning_message in user_warning_messages:
        logging.warning(user_warning_message)

    # Log error messages.

    for user_error_message in user_error_messages:
        logging.error(user_error_message)

    # Log where to go for help.

    if len(user_warning_messages) > 0 or len(user_error_messages) > 0:
        logging.info(message_info(293))

    # If there are error messages, exit.

    if len(user_error_messages) > 0:
        exit_error(697)


def redact_configuration(config):
    ''' Return a shallow copy of config with certain keys removed. '''
    result = config.copy()
    for key in KEYS_TO_REDACT:
        try:
            result.pop(key)
        except Exception:
            pass
    return result

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def construct_line(command, line, properties):
    ''' Construct a replacement line. '''

    result = line  # Default.
    if line.startswith(command):
        regex_string = "{0}(.+?)=".format(command)
        match = re.search(regex_string, line)
        if match:
            key = match.group(1).strip()
            value = properties.get(key)
            if value:
                result = "{0} {1}={2}".format(command, key, value)
    return result


def create_signal_handler_function(args):
    ''' Tricky code.  Uses currying technique. Create a function for signal handling.
        that knows about "args".
    '''

    def result_function(signal_number, frame):
        logging.info(message_info(298, args))
        logging.debug(message_debug(901, signal_number, frame))
        sys.exit(0)

    return result_function


def bootstrap_signal_handler(signal_number, frame):
    ''' Exit on signal error. '''
    logging.debug(message_debug(901, signal_number, frame))
    sys.exit(0)


def entry_template(config):
    ''' Format of entry message. '''
    debug = config.get("debug", False)
    config['start_time'] = time.time()
    if debug:
        final_config = config
    else:
        final_config = redact_configuration(config)
    config_json = json.dumps(final_config, sort_keys=True)
    return message_info(297, config_json)


def exit_template(config):
    ''' Format of exit message. '''
    debug = config.get("debug", False)
    stop_time = time.time()
    config['stop_time'] = stop_time
    config['elapsed_time'] = stop_time - config.get('start_time', stop_time)
    if debug:
        final_config = config
    else:
        final_config = redact_configuration(config)
    config_json = json.dumps(final_config, sort_keys=True)
    return message_info(298, config_json)


def exit_error(index, *args):
    ''' Log error message and exit program. '''
    logging.error(message_error(index, *args))
    logging.error(message_error(698))
    sys.exit(1)


def exit_silently():
    ''' Exit program. '''
    sys.exit(0)


def has_valid_topic(topics, topics_all_list, topics_any_list, topics_excluded_list, topics_included_list, topics_not_all_list, topics_not_any_list):
    ''' Verify that the topic qualifies the repository. '''

    if topics_excluded_list:
        for topic in topics:
            if topic in topics_excluded_list:
                return False

    if topics_included_list:
        count = 0
        for topic in topics:
            if topic in topics_included_list:
                count += 1
        if count == 0:
            return False

    if topics_any_list:
        count = 0
        for topic in topics:
            if topic in topics_any_list:
                count += 1
        if count == 0:
            return False
        return True

    if topics_not_any_list:
        count = 0
        for topic in topics:
            if topic in topics_not_any_list:
                count += 1
        if count == 0:
            return True
        return False

    if topics_all_list:
        total = len(topics_all_list)
        count = 0
        for topic in topics:
            if topic in topics_all_list:
                count += 1
        if count != total:
            return False
        return True

    if topics_not_all_list:
        total = len(topics_not_all_list)
        count = 0
        for topic in topics:
            if topic in topics_not_all_list:
                count += 1
        if count != total:
            return True
        return False

    return True


def run_query(headers, query):
    ''' A simple function to use requests.post to make the API call. Note the json= section. '''

    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code != 200:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    return request.json()


def symbolic_resolution(properties, values):
    ''' Do symbolic resolution recursively through a dictionary. '''

    # Simple symbolic resolution for a string.

    if isinstance(properties, str):
        return values.get(properties, properties)

    if isinstance(properties, bool):
        return values.get(properties, properties)

    # Complex symbolic resolution for other data types.

    if isinstance(properties, list) is list:
        result = []
        for value in properties:
            result.append(symbolic_resolution(value, values))

    if isinstance(properties, dict):
        result = {}
        for key, value in properties.items():
            result[key] = symbolic_resolution(value, values)

    return result


def update_line(line, resolved_properties):
    '''Update line based on Docker Keyword.'''

    if line.startswith("ARG"):
        result = construct_line("ARG", line, resolved_properties.get("arg", {}))
    elif line.startswith("ENV"):
        result = construct_line("ENV", line, resolved_properties.get("env", {}))
    else:
        result = line
    return result


def add_property(dictionary, property_name, property_value):
    '''Add a property to a dictionary.'''

    property_type = type(dictionary.get(property_name))
    if property_type is dict:
        dictionary[property_name].update(property_value)
    elif property_type is list:
        dictionary[property_name].extend(property_value)
    else:
        dictionary[property_name] = property_value

# -----------------------------------------------------------------------------
# do_* functions
#   Common function signature: do_XXX(args)
# -----------------------------------------------------------------------------


def do_docker_acceptance_test(subcommand, args):
    ''' For use with Docker acceptance testing. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Epilog.

    logging.info(exit_template(config))


def do_print_dependabot(subcommand, args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Pull variables from config.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")

    # Log into GitHub.

    github = Github(github_access_token)

    # See https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad

    headers = {
        "Authorization": "Bearer {0}".format(config.get("github_access_token"))
    }

    query = """
{{
  repository(name: "{repository-name}", owner: "senzing") {{
    vulnerabilityAlerts(first: 100) {{
      nodes {{
        createdAt
        dismissedAt
        securityVulnerability {{
          package {{
            name
          }}
          advisory {{
            description
          }}
        }}
      }}
    }}
  }}
}}
"""

    github_organization = github.get_organization(organization)
    for repository in github_organization.get_repos():

        # Query GitHub's GraphQL API https://docs.github.com/en/graphql

        variables = {
            "repository-name": repository.name
        }
        result = run_query(headers, query.format(**variables))

        # Parse results.

        nodes = result.get('data', {}).get('repository', {}).get('vulnerabilityAlerts', {}).get('nodes', [])
        if len(nodes) == 0:
            continue

        # Assemble report.

        packages = []
        for node in nodes:
            package_name = node.get("securityVulnerability", {}).get("package", {}).get('name')
            if package_name not in packages:
                packages.append(package_name)
        packages.sort()

        # Print report.

        print("\nRepository: {0}".format(repository.name))
        print("  Vulnerabilities found by dependabot:")
        for package in packages:
            print("   - {0}".format(package))


def do_print_git_clone(subcommand, args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Pull variables from config.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")

    # Log into GitHub.

    github = Github(github_access_token)

    # Print repository names.

    github_organization = github.get_organization(organization)
    for repo in github_organization.get_repos():
        print("git clone {0}".format(repo.clone_url))


def do_print_git_clone_mirror(subcommand, args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Pull variables from config.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")

    # Log into GitHub.

    github = Github(github_access_token)

    # Print repository names.

    github_organization = github.get_organization(organization)
    for repo in github_organization.get_repos():
        print("git clone --mirror {0}".format(repo.clone_url))


def do_print_pull_requests(subcommand, args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Pull variables from config.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")
    print_format = config.get("print_format")

    # Log into GitHub and get the organization.

    github = Github(github_access_token)
    github_organization = github.get_organization(organization)
    repositories = github_organization.get_repos()

    # Process each repository listed in the configuration.

    for repository in repositories:
        pulls = repository.get_pulls()
        for pull in pulls:
            assignee = "none"
            if pull.assignee is not None:
                assignee = pull.assignee.login
            print_string = "{0} - {1} - {2}".format(repository.name, assignee, pull.title)
            print(print_format.format(print_string))


def do_print_repository_names(subcommand, args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Pull variables from config.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")
    print_format = config.get("print_format")
    topics_all_list = config.get("topics_all_list")
    topics_any_list = config.get("topics_any_list")
    topics_excluded_list = config.get("topics_excluded_list")
    topics_included_list = config.get("topics_included_list")
    topics_not_all_list = config.get("topics_not_all_list")
    topics_not_any_list = config.get("topics_not_any_list")
    is_user = config.get("is_user")

    # Log into GitHub.

    github = Github(github_access_token)

    if is_user:
        # https://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html
        github_organization = github.get_user()
        repos = github_organization.get_repos(affiliation="owner")
    else:
        # https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html
        github_organization = github.get_organization(organization)
        repos = github_organization.get_repos()

    # Print repository names.

    for repo in repos:

        # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html

        topics = repo.get_topics()
        if has_valid_topic(topics, topics_all_list, topics_any_list, topics_excluded_list, topics_included_list, topics_not_all_list, topics_not_any_list):
            print(print_format.format(repo.name))


def do_print_submodules_sh(subcommand, args):
    ''' Print a list of submodules. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Prolog.

    logging.info(entry_template(config))

    # Pull values from configuration.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")

    # Log into GitHub.

    github = Github(github_access_token)

    # Determine current version.

    github_organization = github.get_organization(organization)
    for repository in G2_REPOSITORIES.keys():
        repo = github_organization.get_repo(repository)
        release = repo.get_latest_release()
        G2_REPOSITORIES[repository]['version'] = release.title

    # Print output.

    print('#!/usr/bin/env bash')
    print('')
    print('# Format: repository;version;artifact')
    print('')
    print('SUBMODULES=(')
    for key, value in G2_REPOSITORIES.items():
        version = value.get('version', '0.0.0')
        artifacts = value.get('artifacts', [])
        for artifact in artifacts:
            print('    "{0};{1};{2}"'.format(key, version, artifact))
    print(')')

    # Epilog.

    logging.info(exit_template(config))


def do_print_branches(subcommand, args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Pull variables from config.

    github_access_token = config.get("github_access_token")
    organization = config.get("organization")
    print_format = config.get("print_format")

    # Log into GitHub and get the organization.

    github = Github(github_access_token)
    github_organization = github.get_organization(organization)
    repositories = github_organization.get_repos()

    # Process each repository listed in the configuration.

    for repository in repositories:
        branches = repository.get_branches()
        for branch in branches:
            if branch.name != "main":
                print_string = "{0} - {1}".format(repository.name, branch.name)
                print(print_format.format(print_string))


def do_print_copy_files_from_senzing_install(subcommand, args):
    ''' Create a bash script to copy files. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Prolog.

    logging.info(entry_template(config))

    # Print output.

    print('#!/usr/bin/env bash')
    print('')
    print('# Read metadata.')
    print('')
    print('source 01-user-variables.sh')
    print('')
    print('# Move files to individual repositories')
    print('')
    for key, value in G2_REPOSITORIES.items():
        artifacts = value.get('artifacts', [])
        for artifact in artifacts:
            print(
                "sudo cp ${{SOURCE_PYTHON_DIR}}/{0} ${{GIT_ACCOUNT_DIR}}/{1}".format(artifact, key))
            print("sudo rm ${{SOURCE_PYTHON_DIR}}/{0}".format(artifact))
            print('')

    print('# Move files to g2-python/g2/python ')
    print('')
    for file in ETC_FILES:
        print(
            "sudo cp -r  ${{SOURCE_PYTHON_DIR}}/{0} ${{GIT_ACCOUNT_DIR}}/g2-python/g2/python".format(file))
        print("sudo rm -rf ${{SOURCE_PYTHON_DIR}}/{0}".format(file))
        print("")

    # Epilog.

    logging.info(exit_template(config))


def do_sleep(subcommand, args):
    ''' Sleep.  Used for debugging. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)

    # Prolog.

    logging.info(entry_template(config))

    # Pull values from configuration.

    sleep_time_in_seconds = config.get('sleep_time_in_seconds')

    # Sleep.

    if sleep_time_in_seconds > 0:
        logging.info(message_info(296, sleep_time_in_seconds))
        time.sleep(sleep_time_in_seconds)

    else:
        sleep_time_in_seconds = 3600
        while True:
            logging.info(message_info(295))
            time.sleep(sleep_time_in_seconds)

    # Epilog.

    logging.info(exit_template(config))


def do_update_dockerfiles(subcommand, args):
    ''' Update dockerfiles. '''

    # Reference: https://gist.github.com/nottrobin/a18f9e33286f9db4b83e48af6d285e29

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(subcommand, args)
    validate_configuration(config)

    # Prolog.

    logging.info(entry_template(config))

    # Pull values from configuration.

    configuration_file = config.get("configuration_file")
    github_access_token = config.get("github_access_token")
    organization = config.get("organization")
    sleep_time_in_seconds_dockerfiles = config.get('sleep_time_in_seconds_dockerfiles')

    # Load configuration file

    with open(configuration_file) as file:
        config['file'] = json.load(file)

    # Pull values from configuration file.

    config_repositories = config.get('file', {}).get('repositories', {})
    config_properties = config.get('file', {}).get('properties', {})
    config_property_sets = config.get('file', {}).get('propertySets', {})

    # Log into GitHub and get the organization.

    github = Github(github_access_token)
    github_organization = github.get_organization(organization)

    # Process each repository listed in the configuration.

    changed_repositories = []
    for repository_name, repository_properties in config_repositories.items():

        # Sleep.

        if sleep_time_in_seconds_dockerfiles > 0:
            logging.info(message_info(296, sleep_time_in_seconds_dockerfiles))
            time.sleep(sleep_time_in_seconds_dockerfiles)

        # Start processing.

        logging.info(message_info(120, repository_name))
        properties = repository_properties.get("properties", {})
        property_set_names = repository_properties.get("propertySets", [])

        # Assemble properties.

        aggregated_properties = {}
        for property_set_name in property_set_names:
            property_set = copy.deepcopy(config_property_sets.get(property_set_name, {}))
            for property_name, property_value in property_set.items():
                add_property(aggregated_properties, property_name, property_value)
        for property_name, property_value in properties.items():
            add_property(aggregated_properties, property_name, property_value)

        # Symbolic replacement of property values.

        resolved_properties = symbolic_resolution(aggregated_properties, config_properties)
        resolved_properties_test = symbolic_resolution(aggregated_properties, config_properties)
        resolved_properties_test.get("env").pop("REFRESHED_AT")

        # Short circuit if "skip" requested.

        if resolved_properties.get("skip", False):
            logging.info(message_info(124))
            continue

        # Debug a particular repository. Will exit on first use.

        if resolved_properties.get("debug", False):
            logging.info(message_info(125, json.dumps(resolved_properties, sort_keys=True)))
            return

        # Get values from properties.

        assignee = resolved_properties.get("assignee")
        commit_message = resolved_properties.get("commitMessage")
        main_branch_name = resolved_properties.get("branchNameMain", "main")
        new_branch_name = resolved_properties.get("branchNameNew")
        pull_request_body = resolved_properties.get("pullRequestBody")
        pull_request_title = resolved_properties.get("pullRequestTitle")
        reviewers = resolved_properties.get("reviewers")
        source_file_names = resolved_properties.get("files")

        # Determine if there are any changes.

        has_changed = False
        repository = github_organization.get_repo(repository_name)
        for source_file_name in source_file_names:
            logging.info(message_info(122, source_file_name))

            source_file = repository.get_contents(source_file_name, main_branch_name)
            source_file_content = base64.b64decode(source_file.content).decode('utf-8')
            target_list = []
            for line in source_file_content.split('\n'):
                target_list.append(update_line(line, resolved_properties_test))
            target_file = "\n".join(target_list)
            target_file_content = target_file.encode()

            if source_file_content != target_file:
                has_changed = True

        # If no changes, skip making a Pull Request.

        if not has_changed:
            logging.info(message_info(126, repository_name))
            continue

        # Create or find branch.

        repository = github_organization.get_repo(repository_name)
        refs_heads_branch = 'refs/heads/{branch_name}'.format(branch_name=new_branch_name)
        sha_of_main_branch = repository.get_branch(main_branch_name).commit.sha

        try:
            repository.create_git_ref(refs_heads_branch, sha_of_main_branch)
            logging.info(message_info(121, new_branch_name))
        except Exception as err:
            logging.warning(message_warning(350, new_branch_name, refs_heads_branch, err))

        # Process files.

        for source_file_name in source_file_names:
            logging.info(message_info(122, source_file_name))

            # Modify file.

            source_file = repository.get_contents(source_file_name, refs_heads_branch)
            source_file_content = base64.b64decode(source_file.content).decode('utf-8')
            target_list = []
            for line in source_file_content.split('\n'):
                target_list.append(update_line(line, resolved_properties))
            target_file = "\n".join(target_list)
            target_file_content = target_file.encode()

            # Commit file.

            repository.update_file(
                path=source_file_name,
                message=commit_message,
                content=target_file_content,
                sha=source_file.sha,
                branch=new_branch_name)

        # Create pull request.

        try:
            pull_request = repository.create_pull(
                title=pull_request_title,
                body=pull_request_body,
                base=main_branch_name,
                head=new_branch_name)
            pull_request.create_review_request(reviewers)
            pull_request.add_to_assignees(assignee)
            logging.info(message_info(123, pull_request_title))
        except Exception as err:
            logging.error(message_error(351, pull_request_title, err))

        # Add to list of changed repositories.

        changed_repositories.append(repository_name)

    # Log changed repositories.

    changed_repository_list = ", ".join(changed_repositories)
    logging.info(message_info(140, changed_repository_list))

    # Epilog.

    logging.info(exit_template(config))


def do_version(subcommand, args):
    ''' Log version information. '''

    logging.info(message_info(294, __version__, __updated__))
    logging.debug(message_debug(902, subcommand, args))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == "__main__":

    # Configure logging. See https://docs.python.org/2/library/logging.html#levels

    LOG_LEVEL_MAP = {
        "notset": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "fatal": logging.FATAL,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    LOG_LEVEL_PARAMETER = os.getenv("SENZING_LOG_LEVEL", "info").lower()
    LOG_LEVEL = LOG_LEVEL_MAP.get(LOG_LEVEL_PARAMETER, logging.INFO)
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logging.debug(message_debug(998))

    # Trap signals temporarily until args are parsed.

    signal.signal(signal.SIGTERM, bootstrap_signal_handler)
    signal.signal(signal.SIGINT, bootstrap_signal_handler)

    # Parse the command line arguments.

    SUBCOMMAND = os.getenv("SENZING_SUBCOMMAND", None)
    PARSER = get_parser()
    if len(sys.argv) > 1:
        ARGS = PARSER.parse_args()
        SUBCOMMAND = ARGS.subcommand
    elif SUBCOMMAND:
        ARGS = argparse.Namespace(subcommand=SUBCOMMAND)
    else:
        PARSER.print_help()
        if len(os.getenv("SENZING_DOCKER_LAUNCHED", "")) > 0:
            SUBCOMMAND = "sleep"
            ARGS = argparse.Namespace(subcommand=SUBCOMMAND)
            do_sleep(SUBCOMMAND, ARGS)
        exit_silently()

    # Catch interrupts. Tricky code: Uses currying.

    SIGNAL_HANDLER = create_signal_handler_function(ARGS)
    signal.signal(signal.SIGINT, SIGNAL_HANDLER)
    signal.signal(signal.SIGTERM, SIGNAL_HANDLER)

    # Transform subcommand from CLI parameter to function name string.

    SUBCOMMAND_FUNCTION_NAME = "do_{0}".format(SUBCOMMAND.replace('-', '_'))

    # Test to see if function exists in the code.

    if SUBCOMMAND_FUNCTION_NAME not in globals():
        logging.warning(message_warning(696, SUBCOMMAND))
        PARSER.print_help()
        exit_silently()

    # Tricky code for calling function based on string.

    globals()[SUBCOMMAND_FUNCTION_NAME](SUBCOMMAND, ARGS)
