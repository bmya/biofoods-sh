import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info('BMYA-script | pre-common_connector_library: executing function migrate')
