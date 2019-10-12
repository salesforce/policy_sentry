# Changelog

## 2019-10-12
### Added
* New services added for coverage:
  - iq
  - iq-permission
  - deepracer
  - dbqms
  - forecast
  - lakeformation
  - rds-data

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
