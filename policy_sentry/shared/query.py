from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable, ArnTable, ConditionTable

# https://stackoverflow.com/questions/34538457/alternative-to-stored-procedures-in-sqlite3
# https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html#retrieving-column-names
# def query_action_table(service):


# Per service
def query_condition_table(db_session, service):
    """Get a list of available conditions per AWS service"""
    results = []
    rows = db_session.query(ConditionTable.condition_key_name, ConditionTable.condition_value_type,
                            ConditionTable.description).filter(ConditionTable.service.like(service))
    for row in rows:
        results.append(str(row.condition_key_name))
    return results


# Per condition key name
def query_condition_table_by_name(db_session, service, condition_key_name):
    """Get details about a specific condition key in JSON format"""
    rows = db_session.query(ConditionTable.condition_key_name, ConditionTable.condition_value_type,
                            ConditionTable.description).filter(and_(ConditionTable.condition_key_name.like(condition_key_name), ConditionTable.service.like(service)))
    result = rows.first()
    output = {
        'name': result.condition_key_name,
        'description': result.description,
        'condition_value_type': result.condition_value_type
    }
    return output
