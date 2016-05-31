import os
import sys
import transaction
import random

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    User,
    Address,
    Forum,
    Post
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options,
                               name='appenlight_demo')

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for x in range(1, 20):
            model = User(username='username_{}'.format(x))
            dbsession.add(model)
            model.addresses.append(Address(
                address='Street {}'.format(x),
                phone='123-456-77{}'.format(x))
            )
        for x in range(1, 30):
            model = Forum(forum='forum_{}'.format(x))
            dbsession.add(model)
        for x in range(1, 70):
            model = Post(post='post_{}'.format(x),
                         forum_id=random.randint(1, 20))
            dbsession.add(model)
