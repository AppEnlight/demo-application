from pyramid.config import Configurator
import redis


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.registry.redis_conn = redis.StrictRedis.from_url(
        settings['redis.url'])
    config.scan()

    return config.make_wsgi_app()
