import subprocess
from distutils.command.build import build as _build

import setuptools
from setuptools import find_packages

dependencies = [
    'apache-beam[gcp]==2.15.0',
    'backports.functools-lru-cache==1.5',
    'backports.weakref==1.0.post1',
    'cloudpickle==1.2.2',
    'cycler==0.10.0',
    'decorator==4.4.0',
    'dill==0.2.9',
    'docopt==0.6.2',
    'enum34==1.1.6',
    'funcsigs==1.0.2',
    'futures==3.1.1',
    'gast==0.3.2',
    'gcsfs==0.2.3',
    'google-auth-oauthlib==0.4.0',
    'google-cloud-storage==1.16.1',
    'imutils==0.5.3',
    'joblib==0.13.2',
    'Keras==2.2.4',
    'matplotlib==2.2.4',
    'networkx==2.2',
    'oauthlib==3.1.0',
    'opencv-python-headless==4.1.1.26',
    'pandas==0.25.1',
    'pytz==2019.2',
    'PyWavelets==1.0.3',
    'requests-oauthlib==1.2.0',
    'scikit-image==0.14.5',
    'scikit-learn==0.20.4',
    'scipy==1.2.2',
    'subprocess32==3.5.4',
    'typing==3.6.6',
    'urllib3==1.25.6',
    'xgboost==0.82',
    'zope.interface==4.6.0'
]

CUSTOM_COMMANDS = [['apt-get', 'update'],
                   ['apt-get', '-y', 'install', 'libglib2.0']
                   ]


class build(_build):
    sub_commands = _build.sub_commands + [('CustomCommands', None)]


class CustomCommands(setuptools.Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def RunCustomCommand(self, command_list):
        print('Running command: %s' % command_list)
        p = subprocess.Popen(
            command_list,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # Can use communicate(input='y\n'.encode()) if the command run requires
        # some confirmation.
        stdout_data, _ = p.communicate()
        print('Command output: %s' % stdout_data)
        if p.returncode != 0:
            raise RuntimeError(
                'Command %s failed: exit code: %s' % (command_list, p.returncode))

    def run(self):
        for command in CUSTOM_COMMANDS:
            self.RunCustomCommand(command)


setuptools.setup(
    name='product-image-classifier-2.0',
    version='0.0.1',
    author=['karthik perikala','tianlong xu','andrew amontree'],
    author_email='karthik_perikala@homedepot.com',
    description='product-image-classifier-2.0',
    install_requires=dependencies,
    packages=find_packages() + ['.'],
    cmdclass={'build': build, 'CustomCommands': CustomCommands},
    zip_safe=False
)

### end ###
