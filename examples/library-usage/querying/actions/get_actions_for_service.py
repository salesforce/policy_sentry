#! /usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_for_service


if __name__ == '__main__':
    db_session = connect_db('bundled')
    actions = get_actions_for_service(db_session, 'cloud9')
    print(actions)

"""
Output:

    cloud9:createenvironmentec2
    cloud9:createenvironmentmembership
    cloud9:deleteenvironment
    cloud9:deleteenvironmentmembership
    cloud9:describeenvironmentmemberships
    cloud9:describeenvironmentstatus
    cloud9:describeenvironments
    cloud9:getusersettings
    cloud9:listenvironments
    cloud9:updateenvironment
    cloud9:updateenvironmentmembership
    cloud9:updateusersettings
"""
