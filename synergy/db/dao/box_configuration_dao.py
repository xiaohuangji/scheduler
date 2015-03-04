__author__ = 'Bohdan Mushkevych'

from synergy.db.dao.base_dao import BaseDao
from synergy.db.model import box_configuration
from synergy.db.model.box_configuration import BoxConfiguration
from synergy.supervisor.supervisor_constants import COLLECTION_BOX_CONFIGURATION


class BoxConfigurationDao(BaseDao):
    """ Thread-safe Data Access Object for box_configuration table/collection """
    def __init__(self, logger):
        super(BoxConfigurationDao, self).__init__(logger=logger,
                                                  model_class=BoxConfiguration,
                                                  primary_key=[box_configuration.BOX_ID],
                                                  collection_name=COLLECTION_BOX_CONFIGURATION)
