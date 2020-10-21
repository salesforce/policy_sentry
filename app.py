'''
Created on 21/10/20

@author: skiran
'''
from policy_sentry.writing.sid_group import SidGroup
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home_page.html')

@app.route('/call_policy', methods=["POST"])
def call_policy():
    form_data = dict(request.form)
    output_data = {'mode': 'crud', 'name': '', 'read': [],
                   'write': [],
                   'list': [],
                   'tagging': [],
                   'permissions-management': [],
                   'wildcard-only': {'single-actions': [], 'service-read': [], 'service-write': [],
                                     'service-list': [], 'service-tagging': [],
                                     'service-permissions-management': []}}
    for key,val in form_data.items():
        indx = key.split('_')[-1]
        if 'arn' in key:
            if key.startswith('action'):
                action_name = form_data['action_name_'+indx]
                update_data = output_data
            else:
                action_name = form_data['wc_name_'+indx]
                update_data = output_data['wildcard-only']
            val = list(map(lambda x:x.strip(), val.split(',')))
            update_data[action_name].extend(val)
    sid_group = SidGroup()
    policy = sid_group.process_template(output_data, minimize=None)
    return jsonify(policy)

if __name__ == '__main__':
    app.run()
