import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info('BMYA-script | post-common_connector_library: executing function migrate')
