import random
import decimal
import time
import requests
import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from datetime import datetime

from ..models import (
    User,
    Address
)

log = logging.getLogger(__name__)

custom_log = logging.getLogger('other.namespace.logging')


@view_config(route_name='/', renderer='appenlight_demo:templates/index.jinja2')
def home(request):
    # its a bit too fast ;-)
    time.sleep(0.02)
    users = request.dbsession.query(User)

    # lets load all our users from database and lazy load
    # adresses to illustrate that every access to addresses
    # generates new query
    for user in users:
        for addr in user.addresses:
            pass
    return {"random": random}


@view_config(route_name='action', match_param="action=exception",
             renderer='string')
def test_exception(request):
    # do not buffer - send immediately - usually not good setting for production
    request.environ['appelight.force_send'] = 1
    request.environ['appenlight.tags']['action'] = 'exception_request'
    request.environ['appenlight.tags']['somedate'] = datetime.utcnow()
    request.environ['appenlight.tags']['price'] = 25.5
    request.environ['appenlight.tags']['count'] = random.randint(1, 5)
    msg = 'this log entry was sent with exception report {}'
    log.warning(msg.format(random.randint(1,999)))
    run_exc = random.randint(1, 4)
    dict__that_can_be_inspected = {
        "key_integer": 12345,
        "some_key_with_string": "Unladen Swallow",
        "this_is_a_list": ["a", "b", "cyes", 42]
    }

    if run_exc == 1:
        raise Exception('My custom exception %s' % random.randint(1, 30))
    elif run_exc == 2:
        decimal.Decimal('nondec')
    elif run_exc == 3:
        dict__that_can_be_inspected['non_existant']
    else:
        request.dbsession.execute('SELECT 1.0/0, %s ' % random.randint(1, 30))
        raise Foo()
    return {}


@view_config(route_name='action', match_param="action=slow_report",
             renderer='string')
def test_slow_report(request):
    # do not buffer - send immediately - usually not
    # good setting for production
    request.environ['appenlight.tags']['action'] = 'slow_request'
    request.environ['appenlight.tags']['somedate'] = datetime.utcnow()
    request.environ['appelight.force_send'] = 1
    request.environ['appelight.message'] = "Client marks most timed calls " \
                                           "as slow - for demonstration " \
                                           "purposes"
    request.registry.redis_conn.get('test key A')
    request.registry.redis_conn.set('testkey', 'ABC')
    base_url = request.route_url('/')
    result = requests.get(base_url + 'test/slow_endpoint?msg='
                                     'i_simulate_some_external_resource')
    some_var_with_result = result.text
    users = request.dbsession.query(User)

    # lets load all our users from database and lazy load
    # adresses to illustrate that every access to addresses
    # generates new query
    for user in users:
        for addr in user.addresses:
            pass
    request.dbsession.execute('SELECT users.id, addresses.id, forums.id, posts.id , '
                              '1 + :param1 + :param2, :param3 '
                              'from users join addresses join forums join posts',
                              {"param1": -1, "param2": 11,
                               "param3": 'some_string'}).fetchall()
    log.info(
        'this log entry was sent with slow report %s' % random.randint(1, 999))
    return HTTPFound('/')


@view_config(route_name='action', match_param="action=logging",
             renderer='string')
def test_logging(request):
    # do not buffer - send immediately -
    # usually not good setting for production
    request.environ['appelight.force_send'] = 1
    custom_log.critical('yes life of ' + unichr(960))
    custom_log.info('some info entry',
                    extra={'tag': 'foo', 'count': random.randint(1, 199)})
    custom_log.error('and this is custom USER message: %s' % request.POST.get(
        'log_message'), extra={'action': 'logging',
                               'price': random.randint(1, 199)})
    custom_log.warning(
        'Matched GET /\xc4\x85\xc5\xbc\xc4\x87\xc4\x99'
        '\xc4\x99\xc4\x85/fizzbuzz some incorrect encoding here')
    return HTTPFound('/')


@view_config(route_name='action', match_param="action=slow_endpoint",
             renderer='json')
def slow_endpoint(request):
    # simulate slow endpoint
    time.sleep(0.3)
    return {'some_key': 'some_value'}
