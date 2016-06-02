from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS

class RootFactory(object):
    """
    General factory for non-resource/report specific pages
    """

    def __init__(self, request):
        self.__acl__ = []
        password = request.registry.settings['protected_features_password']
        if request.params.get('password') == password:
            self.__acl__.append((Allow, Everyone, ALL_PERMISSIONS,))
