import json
import random
import requests
import logging

from datetime import datetime, timedelta

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from datetime import datetime

log = logging.getLogger(__name__)


@view_config(route_name='action', match_param="action=generate_shop_data",
             renderer='string')
def generate_shop_data(request):
    settings = request.registry.settings
    endpoint = '/api/logs?protocol_version=0.5'
    entries = []
    date = datetime.utcnow()
    for x in range(0, 200):
        price = random.randint(1, 100)
        quantity = random.randint(1, 100)
        date = date - timedelta(minutes=random.randint(10, 100))
        entries.append(
            {"log_level": "INFO",
             "message": "shop operation",
             "date": date.strftime('%Y-%m-%dT%H:%M:%S.0'),
             "namespace": "rc.shop.dummy_data",
             "server": "dummy.server.com",
             "primary_key": x,
             "permanent": True,
             "tags": [["action", 'buy'],
                      ["product", 'product_name %s' % price],
                      ["price", price],
                      ["quantity", quantity],
                      ["total_payment", price * quantity],
                      ]
             }
        )

    r = requests.post('{}{}'.format(settings['appenlight.base_url'], endpoint),
                      data=json.dumps(entries),
                      headers={
                          "Content-Type": "application/json",
                          "X-appenlight-api-key": settings[
                              'appenlight.api_key']
                      })
    if r.status_code != requests.codes.ok:
        log.error(r.text)
        raise Exception('Wrong response when generating test data')
    return HTTPFound(location=request.route_url('/'))


@view_config(route_name='action', match_param="action=generate_ticket_data",
             renderer='string')
def generate_ticket_data(request):
    settings = request.registry.settings
    endpoint = '/api/logs?protocol_version=0.5'
    entries = []
    date = datetime.utcnow()
    statuses = ['open', 'closed', 'pending', 'invalid']
    owners = ['brian', 'lisa', 'tom', 'martin', 'karen', 'sarah']
    for x in range(0, 200):
        product = random.randint(1, 10)
        date = date - timedelta(hours=random.randint(1, 8))
        entries.append(
            {"log_level": "INFO",
             "message": "support ticket",
             "timestamp": "",
             "date": (date - timedelta(days=x)).strftime(
                 '%Y-%m-%dT%H:%M:%S.0'),
             "namespace": "rc.support_tickets",
             "server": "dummy2.server.com",
             "permanent": True,
             # "primary_key": x,
             "tags": [
                 ["product", 'product_name %s' % product],
                 ["status",
                  random.choice(statuses)],
                 ['owner',
                  random.choice(owners)]
             ]
             }
        )

    r = requests.post('{}{}'.format(settings['appenlight.base_url'], endpoint),
                      data=json.dumps(entries),
                      headers={
                          "Content-Type": "application/json",
                          "X-appenlight-api-key": settings[
                              'appenlight.api_key']
                      })
    if r.status_code != requests.codes.ok:
        log.error(r.text)
        raise Exception('Wrong response when generating test data')
    return HTTPFound(location=request.route_url('/'))


@view_config(route_name='action', match_param="action=generate_intrusion_log",
             renderer='string')
def generate_intrusion_log(request):
    request.environ['appelight.force_send'] = 1

    custom_log = logging.getLogger('security')
    custom_log.critical('breach/fraud attempt',
                        extra={'action': 'fraud',
                               'user_id': random.randint(1, 199)})
    return HTTPFound('/')


@view_config(route_name='action', match_param="action=import_repo_stats",
             renderer='string', permission='special')
def import_repo_stats(request):
    pass
