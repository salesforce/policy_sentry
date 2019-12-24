# Changelog
## 2019-12-24
## Added
* `utils/run_tests.sh` to make local testing easier before having TravisCI do all the work. Updated this in the documentation. Fixed an issue with the tasks.py for the uninstall-package invoke command.
* `--version` flag. Fixes #48
* Added logging

## 2019-12-19
## Changed
* Minor change - broke up the guts of `get_actions_from_policy_file` into a separate function, `get_actions_from_policy` so we can use this outside of Policy Sentry. Added unit tests to match.
* Swapped names to example JSON policy files
* Fixed some missing unit tests

## 2019-12-18
## Added
* Added basic integration testing with PyInvoke. Fixes #58. Generally overhauled the invoke tasks file.
## Changed
* Fixed the cheat sheet documentation in Readme and ReadtheDocs. Fixed "Contributing" docs, and `initialize --fetch`
* Modified the comments in the Policy Sentry YML Template (`--create-template`) so it makes more sense on its own.

## 2019-12-17
### Added
* Version bump to 0.6.2
* `overrides-resource-policies.yml` to specifically identify API calls that modify resource based policies.
* `resource-policies.txt` to answer Scott Piper's question about API calls that can modify resource policies.
### Changed
* The `--fetch` argument was not working because AWS changed their documentation. This incorporates the new documentation instead and changed the logic for the scraping process.
* The initialization command now copies both overrides yml files, not just one

## 2019-12-11
### Added
* Improved invoke and travis for integration testing

## 2019-12-10
### Changed
* `--fetch` argument now passes security check. Using requests and beautifulsoup instead of wget and subprocess.

## 2019-12-01
### Added
* `--fetch` argument to `policy_sentry initialize` command.
* Cutting this as a new release - 0.6.1. This release makes it so people don't have to rely on our HTML docs being up to date.

## 2019-12-01
### Added
* Ran download-docs again to get the CloudWatch synthetics API added.

### Changed
* Made updates to the access-level-overrides.yml file
* download-docs utilities - used long form flags for wget command

## 2019-11-27, part 2
### Changed
* pylint
  - `.pylintrc` generated, added items to the exclusion list.
  - Fixes for pylint

## 2019-11-27
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
