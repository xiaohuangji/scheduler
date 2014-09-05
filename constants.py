__author__ = 'Bohdan Mushkevych'


PROCESS_SCHEDULER = 'Scheduler'
PROCESS_SUPERVISOR = 'Supervisor'
PROCESS_GC = 'GarbageCollectorWorker'
PROCESS_STREAM_GEN = 'EventStreamGenerator'
PROCESS_SESSION_WORKER_00 = 'SingleSessionWorker_00'
PROCESS_SESSION_WORKER_01 = 'SingleSessionWorker_01'
PROCESS_SITE_HOURLY = 'SiteHourlyAggregator'
PROCESS_SITE_DAILY = 'SiteDailyAggregator'
PROCESS_SITE_MONTHLY = 'SiteMonthlyAggregator'
PROCESS_SITE_YEARLY = 'SiteYearlyAggregator'
PROCESS_CLIENT_DAILY = 'ClientDailyAggregator'
PROCESS_CLIENT_MONTHLY = 'ClientMonthlyAggregator'
PROCESS_CLIENT_YEARLY = 'ClientYearlyAggregator'
PROCESS_ALERT_DAILY = 'AlertDailyWorker'

# process provides <process context> to unit testing: such as logger, queue, etc
PROCESS_UNIT_TEST = 'UnitTest'

# process provides <process context> to the launch.py script
PROCESS_LAUNCH_PY = 'LaunchPy'

TYPE_HORIZONTAL_AGGREGATOR = 'type_horizontal'
TYPE_VERTICAL_AGGREGATOR = 'type_vertical'
TYPE_GARBAGE_COLLECTOR = 'type_gc'
TYPE_ALERT = 'type_alert'

TOKEN_SCHEDULER = 'scheduler'
TOKEN_SUPERVISOR = 'supervisor'
TOKEN_GC = 'gc'
TOKEN_STREAM = 'stream'
TOKEN_SESSION = 'session'
TOKEN_SITE = 'site'
TOKEN_CLIENT = 'client'
TOKEN_ALERT = 'alert'

# ** QUEUES **
PREFIX_ROUTING = 'routing_'
PREFIX_QUEUE = 'queue_'

QUEUE_REQUESTED_PACKAGES = 'q_requested_package'
QUEUE_RAW_DATA = 'queue_raw_data'
ROUTING_IRRELEVANT = 'routing_irrelevant'

EXCHANGE_RAW_DATA = 'exchange_raw_data'
EXCHANGE_VERTICAL = 'exchange_vertical'
EXCHANGE_HORIZONTAL = 'exchange_horizontal'
EXCHANGE_ALERT = 'exchange_alert'
EXCHANGE_UTILS = 'exchange_utils'