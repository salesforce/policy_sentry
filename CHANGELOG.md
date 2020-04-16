# Changelog
## Future release (Unreleased)
* Add conditions support

## 0.8.0.3 (2020-04-16)
* Added logging for Query functions (#161)
* Added `get_expanded_policy` function and moved some of the `analysis.analyze` functions to `analysis.expand` (Fixes #164)
* Fixed `analyze_by_access_level` function (Fixes #162)

## 0.8.0.2 (2020-04-12)
* AWS IAM Data refresh
* Fixes to scraping given AWS restructuring of Actions Resources and Condition Keys page

## 0.8.0.1 (2020-04-11)
* The original 0.8.0 release had some issues with the query functions that used to accept 'all' as the service_prefix parameter. This release fixes that issue and brings it back to its previous working status.
* Fix issue where service-wide wildcard-only actions were overwriting each other (#155)

## 0.8.0 (2020-04-09)
* Policy Sentry is now 10x faster!!
* Refactored database approach - not using SQLite Database anymore.

## 0.7.3 (2020-04-01)
* Add skip-resource-constraints feature for CRUD mode (Fixes #145)
* Reduced the example Docker image size
* Path management fixes for windows (#152)

## 0.7.2.1 (2020-03-23)
* Change `get_actions_that_support_wildcard_arns_only` and `get_actions_at_access_level_that_support_wildcard_arns_only` to accept "all" as input to the `service` parameter. This allows you to get results across all AWS service prefixes.

## 0.7.2 (2020-03-17)
* Removed `write-policy-dir` command.
* Better logging for the `write-policy` command
* Fixes #142 - the issue with validating matching resource ARN types

## 0.7.1.2 (2020-03-08)
* Minor fix for `kmsKey` ARN type under `imagebuilder` service. Fixes #114
* Added PyInvoke command for updating the aws documentation.
* The query commands can be called directly (query.query_action_table) to avoid Click-related errors

## 0.7.1.1 (2020-02-10)
* Fix redshift:getclustercredentials override (#132)
* Update overrides to include new resource based policies (EFS is new and worklink was not previously included)
* Docs refresh
* Fixed logging - now just specify `-v debug` instead of `--log-level DEBUG`

## 0.7.1 (2020-02-19)
* **Breaking change** and **new**: Template is modified again. This allows easy additions of wildcard-only actions with access levels specific to services (such as "S3 actions at read access level that do not support resource constraints"), so you never have to look at individual IAM actions again.
* **New**: Output will be in UpperCamelCase rather than all lowercase, for human readability. Note that if `--minimize` is specified for `write-policy`, it will give me lowercase. Otherwise, it will be UpperCamelCase. Fixes #124.
* **New**: Terraform module - #112
* Small bugs - #126

## 0.7.0.2 (2020-02-10)
* Ignore empty entries in the yaml template

## 0.7.0.1 (2020-02-07)
* Quick fix for @jlongman's issue - #118
* Fix the overly verbose logs for #119

## 0.7.0 (2020-02-06)
User-facing changes:
* The `initialize` command is now completely optional.
* **Removed**: The `analyze` command is deprecated and removed. We moved this functionality over to Parliament [here](https://github.com/duo-labs/parliament/pull/66)
* **Removed**: The `download-policies` command is deprecated and removed.
* **Breaking change**: Template format is vastly different. You will have to either pin to an old version or update your templates.
* Now users do not have to specify the `--crud` flag - Policy Sentry will automatically detect the format.
* **Removed**: `analyze` and `download-policies` commands.

Developer library changes:
* A **lot**. Removed a lot of the old functions.
* Replaced `ArnActionGroup` with `SidGroup`. This will allow us to do conditions, etc. It is also easier to read.
* The old `write-policy` logic using `ArnActionGroup` is nuked. Now using `SidGroup`, since that will help us take advantage of condition keys. And it's clean(er).
* `write-policy` is easier to call as a method.
* Unit tests are in a nested folder structure that resembles the rest of the python package.
* Moved to Python Black instead of autopep8
* Replaced a lot of print statements with logging.

## 0.6.11 (2020-01-28)
### Changed
* Now you can skip the long wait under the `initialize` command - the initialize command finishes instantly. To rebuild the database, run `initialize --build`, or to build it with the latest AWS docs, use `initialize --fetch`. Fixes #101
* Documentation updates. Fixes #102

## 0.6.10 (2020-01-24)
### Changed
* writing: In the last version, if you specified "tagging" in your YML file, the write-policy command was ignoring it. This fixes that. #100

## 0.6.9 (2020-01-24)
### Added
* database: Fixes #51 - Give the user an error when the database file does not exist (in `connect_db` function). Except for the case of the initialize function.
* query: The `query` command now supports querying for wildcard only actions at an access level per service. For example, the only wildcard-only action under S3 at the Permissions management access level is `s3:PutAccountPublicAccessBlock`
* query: The `query` command now supports yaml output. This Fixes #95 (output in the Query command) but does not fix #11 (since #11 is asking for the write-policy command to support YAML, and was before the query functionality came out).
* query: the `get_actions_matching_condition_key_crud_and_arn` is available. This provides some scaffolding for #21
* travis: Auto-deployment of Python package with TravisCI
* aws-docs: Fixes #71 - cognito-identity Write actions as permissions management

## 0.6.8 (2020-01-10)
* query: The function `get_all_actions_with_access_level` now supports "all" as a valid input, so you can easily request all IAM actions that are at a certain access level, regardless of service.

## 0.6.7 (2020-01-09)
### Changed
* write-policy: `command/write_policy/write_policy_with_actions` and `command/write_policy/write_policy_with_access_levels` can be called directly.
* template: `arn` is now `role_arn` to avoid confusion when writing templates
* template: `tag` is now `tagging` to avoid inconsistency when writing templates
* template: `writing/template/` now exposes `get_crud_template_dict` and `get_actions_template_dict` so developers can create the templates by calling the library. We might add on additional ones so they can just pass in lists without having to know the format, but not right now. They can pass that into `write_policy_with_actions` and `write_policy_with_access_levels`

## 0.6.6 (2020-01-08)
### Added
### Added
* docs: PyInvoke commands to support the Sphinx documentation testing locally
* docs: Sample scripts to demonstrate the usage of our methods for developers who want to import Policy Sentry
* Documentation uplift in general
* docs: A lot of the docstrings in the code
### Changed
* database: Fixed an issue where the bundled database was being appended to instead of overwritten when going through an update.
* database: Fixed an issue where condition keys were being stored as `'aws:RequestTag/$  {  TagKey}'` - we need it without extra spaces.

## 0.6.5 (2020-01-03)
### Added
* Docker support
* database: Fix an issue with pre-bundled database paths.
* write-policy: Write-policy allows either stdin or input-file. Fixes #78.
* template: YAML Validation via Schema

## 0.6.4 (2020-01-03)
### Added
* Developers can now easily leverage Policy Sentry as a python package without needing to build the database from the docs. Just use `` before passing in commands that require the `db_session` and you're ready to go. Fixes #74
* `utils/run_tests.sh` to make local testing easier before having TravisCI do all the work. Updated this in the documentation. Fixed an issue with the tasks.py for the uninstall-package invoke command.
* `--version` flag. Fixes #48
* Renamed write-policy template's `roles_with_crud_levels` and `roles_with_actions` to `policy_with_crud_levels` and `policy_with_actions` since this makes way more sense. Discussion is in #65. Version bump to 0.7.0 because this creates breaking changes.
### Changed
* Pyinvoke file now has try/except to catch failures, so we can have the build fail if the Invoke commands tests give non zero responses.
* Moved to a saner subfolder structure, where the folders are mostly specific to their commands.
  - The new folders are `analysis`, `configuration`, `downloading`, `querying`, `scraping`, `util`, and `writing`
  - Files in the `analysis` folder, for example, relate to the `analyze` command. They don't import from each other, with the occasional exception of re-using functions from the `querying` folder. They all import common methods from the `util` folder and the `shared` folder as well.
* Renamed all the function names under querying folder so they make more sense.

## 0.6.3 (2019-12-19)
### Added
* Added basic integration testing with PyInvoke. Fixes #58. Generally overhauled the invoke tasks file.
### Changed
* Minor change - broke up the guts of `get_actions_from_policy_file` into a separate function, `get_actions_from_policy` so we can use this outside of Policy Sentry. Added unit tests to match.
* Swapped names to example JSON policy files
* Fixed some missing unit tests
* Fixed the cheat sheet documentation in Readme and ReadtheDocs. Fixed "Contributing" docs, and `initialize --fetch`
* Modified the comments in the Policy Sentry YML Template (`--create-template`) so it makes more sense on its own.

## 0.6.2 (2019-12-17)
### Added
* `overrides-resource-policies.yml` to specifically identify API calls that modify resource based policies.
* `resource-policies.txt` to answer Scott Piper's question about API calls that can modify resource policies.
### Changed
* The `--fetch` argument was not working because AWS changed their documentation. This incorporates the new documentation instead and changed the logic for the scraping process.
* The initialization command now copies both overrides yml files, not just one
* Improved invoke and travis for integration testing
### Changed
* `--fetch` argument now passes security check. Using requests and beautifulsoup instead of wget and subprocess.

## 0.6.1 (2019-12-01)
### Added
* `--fetch` argument to `policy_sentry initialize` command.
* Cutting this as a new release - 0.6.1. This release makes it so people don't have to rely on our HTML docs being up to date.

## 2019-12-01
### Added
* Ran download-docs again to get the CloudWatch synthetics API added.

### Changed
* Made updates to the access-level-overrides.yml file
* download-docs utilities - used long form flags for wget command

## 0.6.0 (2019-11-27)
### Changed
* pylint
  - `.pylintrc` generated, added items to the exclusion list.
  - Fixes for pylint
### Changed
* Refined the Network exposure actions to Create actions only - i.e., those that could cause exposure only (it does not include delete actions, only create). Typically only API calls that have public IPs as an option

## 2019-11-26
### Added
* Added test cases for new parts of analyze command
* Created constants.py to reduce unnecessary code
* Analyze command now allows for single policy files as well as recursively looking throughout the directory,
* Cutting a new release when this is done due to the major changes involved.
### Changed
* Moved generate-report back to the analyze command.
* Move analysis folder from `~/.policy_sentry/policy-analysis` to `~/.policy_sentry/analysis`
* Update the command cheat sheet and the ReadTheDocs stuff for this


## 2019-11-24
### Changed
* Fixed analyze function's accuracy - normalizes incoming lists of actions so it accepts lists of actions regardless of lower/upper/camel case.
## 2019-11-22
### Added
* Initial set of improvements for uplift of the analyze-iam-policy feature.
  - Created generate-report command (will eventually move this over to the regular analyze command, just keeping it separate for now)
  - Added scaffolding for generating report templates in Markdown and then to HTML using Jinja2 templates
  - Added functionality to download policies recursively
## 2019-11-21 Part 2
### Changed
* **Fixed issue where initialize was not working due to db_session being declared outside of a function. This only applied to the last release.**
* Analyze command: Added credentials-exposure.txt audit file
* Fixed some stuff in the documentation that had old errors.
* Version bump
* HTML Documentation update approach (Fixes GH-23)
    * `get_links.py` and other util scripts are now updated. We no longer have to maintain the big list of service-to-html-names.
    * Missing services are now fixed by this HTML documentation update approach:
      - applicationinsights
      - appmesh
      - appmesh-preview
      - backup-storage
      - chatbot
      - codestar-notifications
      - dataexchange
      - ec2-instance-connect
      - iotthingsgraph
      - mediapackage-vod
      - managedblockchain
      - personalize
      - rdsiamauthentiation
      - savingsplans
      - pinpointemailservice
      - workmailmessageflow
      - Marketplace links:
          - Marketplace catalog
          - Marketplace Entitlement Service
          - Marketplace Image Building Service
          - Marketplace Procurement systems integration
          - Private Marketplace

## 2019-11-21
### Changed
* `query` command is cleaner. Used click subgroups instead of if-else hell.
* Adjusted the docs to reflect this.
### Removed
* ROADMAP.md because this is in the documentation instead.

## 2019-11-15
### Changed
* Template format has less clutter
* Policies in CRUD mode can now support IAM Actions that cannot be restricted to ARNs. This Fixes #16.
* Adjusted the docs to reflect this.

## 2019-11-13
### Changed
* Added `--list-arn-types` under the query command.
  - This allows the user to query available ARN types and RAW ARN pairs
  - Added test case for the new query command
* Various documentation issues
  - Fixed links to the Wiki and such, since we moved to ReadTheDocs.
  - Fix command cheat sheets

## 2019-11-08
### Added
* Query capability to assist users in identifying actions to supply in future #16 feature
## 2019-11-07
### Added
* Query capabilities to address #29. This currently includes capabilities for:
  - Action Table:
    - (1) list of all actions in a service
    - (2) details on specific action
    - (3) details on actions matching a service and access levels
    - Need to provide more granular queries for querying the access table before finalizing PR. Especially the one based on access levels, and available condition keys per action or ARN.
  - ARN Table: (1) list of all raw ARNs in a service, (2) details about a specific ARN type
  - Conditions Table: (1) list of all condition keys available to a service, (2) details about a specific condition key
  - Specialized
    - Query the actions table for actions within a service that support specific Condition keys
    - Query the actions table for the same as above, but regardless of service
* To finalize the query capabilities, just need to run it by Matty, make adjustments with Click Contexts, and squash commits.

* Unit tests to accompany the query capabilities

### Changed
* Fixed naming of a few unit tests to improve output in nosetests.
* Fixed Condition Keys in actions table; it was previously set to the string 'None' instead of a null value.
* Fixed #33 by adding lines 214-222 to database.py

## 2019-10-24
### Added
* Added boto3 and botocore to setup.py
* Cutting a new release to provide a quick fix for those issues
* This fixes #28
### Changed
* Updated Pipfile.lock
* Fixed an issue with the list_policies command
* Fixed the help text for the `download-policies --include-unattached` flag

## 2019-10-19
### Added
* `analyze-iam-policy` Code to create policy-analysis directory, was missing with last release... added it
### Changed
* Removed leftover code before access-level overrides was a feature

## 2019-10-18, part 2
### Added
* access-level overrides now includes a TON of overrides Fixes #18.
* Services: Deepracer, Signer, EventBridge
* Releasing 0.5.1 because of all the major changes to the database
### Changed
* Links documents
* Improvements to the documentation updating scripts.

## 2019-10-18
### Added
* We can now override Access levels so we aren't entirely dependent upon accurate AWS documentation for proper ACLs. Fixes #8.
* Test cases for the new Access level override functions
* You can now supply a custom YML file as part of the initialize command to test out your own overrides (so you don't have to depend on updates to this repository if you don't want to)
* Created `policy_sentry/shared/data/access-level-overrides.yml` for a preloaded set, based on the current known issues with AWS IAM access levels.
* Cut a new release because this is a big improvement (and because I moved around a function or two)

## 2019-10-16
### Added
* Added test cases for YML files that have missing access level blocks - for example, if someone wants to generate a policy that doesn't include "Tagging" or "Permissions Management"
### Changed
* Test cases to allow missing access level blocks

## 2019-10-15
### Added
* Unit tests for the policy template generation
* `download-policies` command added
  - Downloads policies to `~/.policy_sentry/account-id/aws-managed` or `~/.policy_sentry/account-id/customer-managed`.

## 2019-10-14
### Changed
* `short_help` for Click commands to improve help messages
* `create-template` command added to make policy file writing easier.

## 2019-10-12
### Added
* Updated to 0.4.1
* New services added for coverage:
  - iq
  - iq-permission
  - deepracer
  - dbqms
  - forecast
  - lakeformation
  - rds-data

### Changed
* `utils/get_links.py` script had an issue with paths

## 2019-10-06
### Added
* Added `analyze` functionality to analyze a policy according to access levels, not just a list of actions.

### Changed
* Updated the HTML documentation to get the latest updates.
* Fixed old references to `scripts` directory; now it is the `utils` directory
* Fixed the path of the policy_sentry/shared/data/docs directory in the download-docs.sh script, since its previous reference was the root directory, which was accurate before we moved to pypi compatibility.

## 2019-10-02
### Changed
* Sanitizing directory before moving to GitHub
* Remove _docs directory since we are using the wiki

## 2019-09-19
### Added
* `write-policy-dir` command
* input-dir and output-dir directories under examples, to show `write-policy-dir` command usage

## 2019-09-14
### Changed
* Project structure now follows pypi format
* Changed download-docs stuff to utils folder.
* `create_all_tables` command is now `initialize`
* Changed Matty's folder structure a bit so the setup.py file is now in the root directory, which makes more sense.
* Fixed underscore vs. hyphen typo in the docs.
* html files still live in the main policy_sentry pypi package. The user can quickly generate the SQLite database using the initialize function (formerly create_all_tables)
* Lots of other cleanup.

### Added
* pypi modifications, such as the MANIFEST.in file
* Database file now resides in `$HOME/.policy_sentry/aws.sqlite3`
* Default audit file now resides in `$HOME/.policy_sentry/audit/permissions-access-level.txt`

## 2019-09-11
### Added
* Added modified unit tests in test_write_policy.py
* Created a policy.py file to contain ArnActionGroup

### Changed
* Moved Minimization functions over to their own file
* Instead of ArnActionCollection, now using ArnActionGroup name
* Moved functionality from the write_policy file to the relevant files in the shared folder.
* Fixed risky-iam.txt file name

## 2019-09-08
### Changed
* Modified the write_policy_with_actions function so it uses the write_policy with crud stuff. We can now delete a lot of the functions that we don't use anymore.
* Removed all the code that is now unused

## 2019-09-04
### Changed
* lots of code reviews and doc strings

## 2019-09-03
### Added
* pipfile and lockfile
* Feature to scrape docs locally: grab_docs.sh, utils/download-docs.sh, utils/get_links.py
* pylintrc file
* disabled *line-too-long* in pylint
* editorconfig file
* bandit as a dependency

### Changed
* update readme links to short version
* Feature to scrape docs locally: grab_docs.sh, utils/download-docs.sh, utils/get_links.py

### 2019-09-02

* Added Unit tests. Fixes #20

### 2019-09-01

* Feature: CRUD Functionality supports user-supplied input now (fixes GH-05)
* Database file now checked into git
* We now assume that you are using the same database file
* Just need to trim the write_policy file and combine functions
* Trimmed the command flags to make thing simpler
* Updated documentation to reflect reduced command flags.

### 2019-08-30 (pt 2)

* Added Condition keys table
* Actions Table now separates the Condition Keys by commas instead of double spaces

### 2019-08-30

* Version bump (0.1.0)
* Fixed class structure
* Moved command-specific documentation to the `_docs` folder for cleanliness

### 2019-08-26

* Added `create_all_tables` command
* Updated functions to include all services (it wasn't grabbing all services before).
* Added Note in README about the 3 services missing from the Actions, Resources, and Condition Keys page
* Added `analyze_iam_policy` command with test files
* Gives a warning when your action matches fishy IAM actions
* Split connect_db and create_tables out into different functions
* Permits using existing database.
* Added expand functionality.
* Added flag to `analyze_iam_policy` to allow custom audit file
* Fixed issue #3 for ecr and codecommit overlap
* Added minimize functionality

### 2019-08-23

* Removed check_access and moved it to a separate repository.
* Fixed imports

### 2019-08-05

* retired check_permissions_usage (Access Advisor check), since CloudMapper generates a great report using that.
* Write_policy now uses SQLite instead of funky objects
* CRUD Functionality now supported
