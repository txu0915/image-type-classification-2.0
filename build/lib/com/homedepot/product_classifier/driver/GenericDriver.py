from zope.interface import Interface


class GenericDriver(Interface):
    def processor(self, argv):
        pass
