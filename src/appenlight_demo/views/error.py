from pyramid.view import view_config


@view_config(context=Exception, renderer='../templates/error.jinja2')
def exception_view(request):
    request.response.status = 500
    request.registry.redis_conn.get('test key')
    return {}
