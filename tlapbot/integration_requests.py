import requests
from flask import current_app

def send_redeem(redeem, action_id):
    if current_app.config['INTEGRATION_INSTANCE_URL']:
        url = current_app.config['INTEGRATION_INSTANCE_URL'] + '/DoAction'
        current_app.logger.debug(f'calling integration for {redeem}: {url}.')
        try:
            r = requests.post(url, json={"action": {"id": action_id}})
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error occured sending redeem webhook: {e.args[0]}')
        if r.status_code != 204:
            current_app.logger.error(f'Failed to send redeem. Error: {r.status_code}')
        return
    
def send_integration(redeem, action_id, data):
    if current_app.config['INTEGRATION_INSTANCE_URL']:
        url = current_app.config['INTEGRATION_INSTANCE_URL'] + '/DoAction'
        current_app.logger.debug(f'calling integration for {redeem}: {url}.')
        try:
            r = requests.post(url, json={"action": {"id": action_id},
                                         "args": data})
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error occured sending redeem webhook: {e.args[0]}')
        if r.status_code != 204:
            current_app.logger.error(f'Failed to send redeem. Error: {r.status_code}')
        return