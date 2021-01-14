from zope.interface import Interface


class DataFlowPipeline(Interface):
    def create_pipeline(self, argv):
        pass

    def execute(self):
        pass
