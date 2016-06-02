import redis

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authorization_policy = ACLAuthorizationPolicy()
    authentication_policy = AuthTktAuthenticationPolicy('not_so_secret')

    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          root_factory='appenlight_demo.security.RootFactory',
                          )
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.registry.redis_conn = redis.StrictRedis.from_url(
        settings['redis.url'])
    config.scan()

    return config.make_wsgi_app()
