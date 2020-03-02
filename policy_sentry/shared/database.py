"""
Classes for the Actions, ARNs, and Conditions Tables structure
Functions for building the database - by parsing through the AWS Docs and storing it in the database
"""
import os
import sys
import json
import logging
from sqlite3 import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
from sqlalchemy import Column, Integer, String
from policy_sentry.configuration.access_level_overrides import (
    get_action_access_level_overrides_from_yml,
)
from policy_sentry.scraping.scrape import get_html
from policy_sentry.shared.constants import HTML_DIRECTORY_PATH
from policy_sentry.util.access_levels import determine_access_level_override
from policy_sentry.util.arns import (
    get_resource_path_from_arn,
    get_partition_from_arn,
    get_account_from_arn,
    get_region_from_arn,
    get_resource_from_arn,
    get_service_from_arn,
)
from policy_sentry.util.conditions import (
    get_comma_separated_condition_keys,
    get_service_from_condition_key,
)

logger = logging.getLogger(__name__)
Base = declarative_base()  # pylint: disable=invalid-name


class ActionTable(Base):
    """SQLAlchemy Declarative configuration for the IAM Actions table"""

    __tablename__ = "actiontable"
    id = Column(Integer, primary_key=True)
    service = Column(String(50))
    name = Column(String(50))
    description = Column(String(50))
    access_level = Column(String(50))
    resource_type_name = Column(String(50))
    resource_type_name_append_wildcard = Column(String(50))
    resource_arn_format = Column(String(50))
    condition_keys = Column(String(50))
    dependent_actions = Column(String(50))

    def __repr__(self):
        return (
            "<Action(service='%s', name='%s', description='%s', access_level='%s', resource_type_name='%s', resource_type_name_append_wildcard='%s', resource_arn_format='%s', condition_keys='%s', dependent_actions='%s')>"
            % (
                self.service,
                self.name,
                self.description,
                self.access_level,
                self.resource_type_name,
                self.resource_type_name_append_wildcard,
                self.resource_arn_format,
                self.condition_keys,
                self.dependent_actions,
            )
        )


class ArnTable(Base):
    """SQLAlchemy Declarative configuration for the Resource Types table"""

    __tablename__ = "arntable"
    id = Column(Integer, primary_key=True)
    resource_type_name = Column(String(50))
    raw_arn = Column(String(50))
    originating_service = Column(String(50))
    arn = Column(String(50))
    partition = Column(String(50))
    service = Column(String(50))
    region = Column(String(50))
    account = Column(String(50))
    resource = Column(String(50))
    resource_path = Column(String(50))
    condition_keys = Column(String(50))

    def __repr__(self):
        return (
            "<Arn(resource_type_name='%s', raw_arn='%s', originating_service='%s', arn='%s', partition='%s', service='%s', region='%s', account='%s', resource='%s', resource_path='%s', condition_keys='%s')>"
            % (
                self.resource_type_name,
                self.raw_arn,
                self.originating_service,
                self.arn,
                self.partition,
                self.service,
                self.region,
                self.account,
                self.resource,
                self.resource_path,
                self.condition_keys,
            )
        )


class ConditionTable(Base):
    """SQLAlchemy Declarative configuration for the Condition Keys table"""

    __tablename__ = "conditiontable"
    id = Column(Integer, primary_key=True)
    # the service that this applies to. aws:RequestTag can apply to many
    # services
    service = Column(String(50))
    condition_key_name = Column(String(50))  # name of the condition key
    # i.e., aws for aws:RequestTag; ec2 for ec2:Region
    condition_key_service = Column(String(50))
    description = Column(String(50))
    # String, ARN, Boolean, Date, Numeric, Long
    condition_value_type = Column(String(50))

    def __repr__(self):
        return (
            "<ConditionTable(service='%s', condition_key_name='%s', condition_key_service='%s', description='%s', condition_value_type='%s')>"
            % (
                self.service,
                self.condition_key_name,
                self.condition_key_service,
                self.description,
                self.condition_value_type,
            )
        )


def create_database(db_session, services, access_level_overrides_file):
    """
    Calls the functions to build the ARN tables.

    :param db_session: the SQLAlchemy database session.
    :param services: List of all services to build the tables for. Defaults to all AWS Services
    :param access_level_overrides_file: A file we can use to override the Access levels per action
    :return: the SQLAlchemy database session.
    """
    directory = HTML_DIRECTORY_PATH + "/"
    logger.info("Reading the html docs from this directory: %s", directory)
    logger.info("Using access level overrides file %s", access_level_overrides_file)
    print("Building tables...")
    for service in services:
        print(service, sep="", end=", ", flush=True)
        build_arn_table(db_session, service)
        db_session.commit()
        build_action_table(db_session, service, access_level_overrides_file)
        db_session.commit()
        build_condition_table(db_session, service)
        db_session.commit()
    return db_session


def connect_db(db_file, initialization=False):
    """
    Given the absolute path to a SQLite database, connect to the database and return a database session.
    :param db_file: The absolute path to the SQLite database.
    :param initialization: Boolean to indicate whether or not this is at the initialization step. If set to True, this will not throw an error when the database file does not exist. Defaults to False.
    :return: Database session object.
    """
    # Valid SQLite URL forms are:
    #  sqlite:///:memory: (or, sqlite://)
    #  sqlite:///relative/path/to/file.db
    #  sqlite:////absolute/path/to/file.db # Using this one. db_file is
    # prefixed with another / so it works out to 4
    if db_file == "bundled":
        database_path = str(os.path.dirname(__file__)) + "/data/aws.sqlite3"
    else:
        database_path = db_file

    if not initialization and not os.path.isfile(database_path):
        logger.critical(
            "ERROR: The database path does not exist. Please run `policy_sentry initialize` to "
            "initialize the IAM database."
        )
        sys.exit(1)
    engine = create_engine(str("sqlite:///" + database_path), echo=False)
    try:
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)  # pylint: disable=invalid-name
        Session.configure(bind=engine)
        db_session = Session()
    except OperationalError as o_e:
        logger.critical(o_e)
        sys.exit()
    return db_session


def build_action_table(db_session, service, access_level_overrides_file):
    """
    Builds the action table in the SQLite database.
    See the first Table on any service-specific page in the Actions, Resources, and Condition Keys documentation.
    That information is scraped, parsed, and stored in the SQLite database using this function.

    :param db_session: Database session object
    :param service: AWS Service to query. This can be called in a loop or for a single service (see connect_db function above).
    :param access_level_overrides_file: The path to the file that we use for overriding access levels that are incorrect in the AWS documentation
    """
    directory = os.path.abspath(os.path.dirname(__file__)) + "/data/docs/"
    html_list = get_html(directory, service)
    access_level_overrides_cfg = get_action_access_level_overrides_from_yml(
        service, access_level_overrides_file
    )
    for df_list in html_list:
        for df in df_list:  # pylint: disable=invalid-name
            table = json.loads(df.to_json(orient="split"))
            table_data = df
            # Actions table
            if "Actions" in table_data and "Access Level" in table_data:
                for i in range(len(table["data"])):
                    # If the table is set to none
                    # If the cell is blank, that indicates it needs wildcard
                    if table["data"][i][3] is None:
                        resource_type_name = "None"
                        resource_type_name_append_wildcard = "False"
                        resource_arn_format = "*"
                    # Check if resource type name has wildcard suffix - i.e., parameter* instead of parameter
                    # If it does, set the append_wildcard flag to true,
                    # and set the resource name to that but without the
                    # wildcard to make searching easier
                    elif "*" in table["data"][i][3]:
                        temp_resource_type_name = table["data"][i][3]
                        resource_type_name = temp_resource_type_name[:-1]
                        if resource_type_name is None:
                            resource_type_name = "None"
                        resource_type_name_append_wildcard = "True"
                        query_resource_arn_format = db_session.query(
                            ArnTable.raw_arn
                        ).filter(
                            and_(
                                ArnTable.service.ilike(service),
                                ArnTable.resource_type_name.like(resource_type_name),
                            )
                        )
                        first_result = query_resource_arn_format.first()
                        try:
                            resource_arn_format = first_result.raw_arn
                        # For EC2 RunInstances, ResourceTypes have some duplicates.
                        # The Resource Types (*required) column has duplicates
                        # and the Access Level has `nan`
                        except AttributeError:
                            continue
                    else:
                        resource_type_name = table["data"][i][3]
                        resource_type_name_append_wildcard = "False"
                        first_result = (
                            db_session.query(ArnTable.raw_arn)
                            .filter(
                                ArnTable.service.ilike(service),
                                ArnTable.resource_type_name.like(table["data"][i][3]),
                            )
                            .first()
                        )
                        try:
                            if "*" in first_result.raw_arn:
                                resource_arn_format = first_result.raw_arn[:-1]
                            else:
                                resource_arn_format = first_result.raw_arn
                        except AttributeError:
                            continue
                    # For lambda:InvokeFunction, the cell is 'lambda:InvokeFunction [permission only]'.
                    # To avoid this, let's test for a space in the name.
                    # If there is a space, remove the space and all text after
                    # it.
                    # pylint: disable=unused-variable
                    if " " in table["data"][i][0]:
                        text_with_space = table["data"][i][0]
                        action_name, sep, tail = text_with_space.partition(" ")
                    else:
                        action_name = table["data"][i][0]

                    # Access Level #####
                    # access_level_overrides_cfg will only be true if the service in question is present
                    # in the overrides YML file
                    if access_level_overrides_cfg:
                        override_result = determine_access_level_override(
                            service,
                            action_name,
                            table["data"][i][2],
                            access_level_overrides_cfg,
                        )
                        if override_result:
                            access_level = override_result
                            logger.debug(
                                "Override: Setting access level for %s:%s to %s",
                                service,
                                action_name,
                                access_level,
                            )
                        else:
                            access_level = table["data"][i][2]
                    else:
                        access_level = table["data"][i][2]
                    # Condition keys #####
                    if table["data"][i][4] is None:
                        condition_keys = None
                    # If there are multiple condition keys, make them comma separated
                    # Otherwise, if we ingest them as-is, it will show up as
                    # two spaces
                    elif "  " in table["data"][i][4]:
                        condition_keys = get_comma_separated_condition_keys(
                            table["data"][i][4]
                        )
                    else:
                        condition_keys = table["data"][i][4]

                    ##### Dependent actions #####
                    if table["data"][i][5] is None:
                        dependent_actions = None
                    elif "  " in table["data"][i][5]:
                        # Let's just use the same method that we use for
                        # separating condition keys
                        dependent_actions = get_comma_separated_condition_keys(
                            table["data"][i][5]
                        )
                    else:
                        dependent_actions = table["data"][i][5]

                    db_session.add(
                        ActionTable(
                            service=service,
                            name=action_name,
                            description=table["data"][i][1],
                            access_level=access_level,
                            resource_type_name=resource_type_name,
                            resource_type_name_append_wildcard=resource_type_name_append_wildcard,
                            resource_arn_format=str(resource_arn_format),
                            condition_keys=condition_keys,
                            dependent_actions=dependent_actions,
                        )
                    )
                    db_session.commit()
            elif "Resource Types" in table_data and "ARN" in table_data:
                continue
            else:
                continue
    db_session.commit()


def build_arn_table(db_session, service):
    """
    Builds the ARN Table - the table of resource types - in the SQLite database.

    :param db_session: SQLAlchemy database session.
    :param service: The AWS service prefix
    """
    directory = os.path.abspath(os.path.dirname(__file__)) + "/data/docs/"
    html_list = get_html(directory, service)
    for df_list in html_list:
        for df in df_list:  # pylint: disable=invalid-name
            table = json.loads(df.to_json(orient="split"))
            table_data = df
            if "Resource Types" in table_data and "ARN" in table_data:
                for i in range(len(table["data"])):
                    # Replace the random spaces in the ARN
                    temp_raw_arn = table["data"][i][1].replace(" ", "")
                    # Handle resource ARN path
                    if get_resource_path_from_arn(temp_raw_arn):
                        resource_path = get_resource_path_from_arn(temp_raw_arn)
                    else:
                        resource_path = ""
                    # Handle condition keys
                    if table["data"][i][2] is None:
                        condition_keys = None
                    # If there are multiple condition keys, make them comma separated
                    # Otherwise, if we ingest them as-is, it will show up as
                    # two spaces
                    elif "  " in table["data"][i][2]:
                        condition_keys = get_comma_separated_condition_keys(
                            table["data"][i][2]
                        )
                    else:
                        condition_keys = table["data"][i][2]
                    db_session.add(
                        ArnTable(
                            resource_type_name=table["data"][i][0],
                            raw_arn=str(temp_raw_arn),
                            # Fix for https://github.com/salesforce/policy_sentry/issues/114
                            # For example, the EC2 image builder's ARN table has a Raw ARN format of
                            # arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}
                            # with a resource arn type of "kmsKey", whereas the KMS service's ARN table has
                            # the same raw ARN format, but with a resource arn type of "key"
                            originating_service=service,  # Ex: imagebuilder service prefix, or kms service prefix
                            arn="arn",
                            partition=get_partition_from_arn(temp_raw_arn),
                            service=get_service_from_arn(temp_raw_arn),
                            region=get_region_from_arn(temp_raw_arn),
                            account=get_account_from_arn(temp_raw_arn),
                            # Ex: kmsKey for imagebuilder service, key for KMS service
                            resource=get_resource_from_arn(temp_raw_arn),
                            resource_path=resource_path,
                            condition_keys=condition_keys,
                        )
                    )
                    db_session.commit()


def build_condition_table(db_session, service):
    """
    Build the Conditions table - the list of conditions available to each service.

    :param db_session: SQLAlchemy database session
    :param service: AWS Service Prefix
    """
    directory = os.path.abspath(os.path.dirname(__file__)) + "/data/docs/"
    html_list = get_html(directory, service)
    for df_list in html_list:
        for df in df_list:  # pylint: disable=invalid-name
            table = json.loads(df.to_json(orient="split"))
            table_data = df
            if (
                "Condition Keys" in table_data
                and "Description" in table_data
                and "Type" in table_data
            ):
                for i in range(len(table["data"])):
                    # Description: sometimes it is empty, like the conditions table for S3.
                    # In order to avoid errors with NULL Database entries, set
                    # to 'None'
                    if table["data"][i][1] is None:
                        temp_description = "None"
                    else:
                        temp_description = table["data"][i][1]
                    # Name: sometimes there are random spaces in the string, like 'aws:RequestTag/$  {  TagKey}'.
                    condition_key_name = table["data"][i][0].replace(" ", "")
                    db_session.add(
                        ConditionTable(
                            service=service,
                            condition_key_name=condition_key_name,
                            condition_key_service=get_service_from_condition_key(
                                table["data"][i][0]
                            ),
                            description=temp_description,
                            condition_value_type=str.lower(table["data"][i][2]),
                        )
                    )
                    db_session.commit()
