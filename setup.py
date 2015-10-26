from distutils.core import setup

setup(name='synergy_scheduler',
      version='1.15',
      description='Synergy Scheduler',
      author='Bohdan Mushkevych',
      author_email='mushkevych@gmail.com',
      url='https://github.com/mushkevych/scheduler',
      packages=['synergy', 'synergy.db', 'synergy.db.dao', 'synergy.db.manager', 'synergy.db.model',
                'synergy.mq', 'synergy.conf', 'synergy.mx', 'synergy.scheduler', 'synergy.supervisor',
                'synergy.system', 'synergy.workers'],
      package_data={'synergy.mx': ['static/images/*', 'static/fonts/*', 'static/js/*', 'static/css/*', 'templates/*'],
                    'synergy.mq': ['AUTHORS', 'LICENSE']},
      long_description='Synergy Scheduler shines in governing interdependent processes and their jobs. '
                       'Has rich Web UI. Can also work as a cron-like job trigger.',
      license='BSD 3-Clause License',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: JavaScript',
          'Topic :: Office/Business :: Scheduling',
          'Topic :: Utilities',
      ],
      requires=['werkzeug', 'jinja2', 'amqp', 'pymongo', 'psutil', 'fabric', 'setproctitle', 'synergy_odm', 'mock',
                'xmlrunner', 'pylint', 'six']
      )
