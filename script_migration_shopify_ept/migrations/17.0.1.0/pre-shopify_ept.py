import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info('BMYA-script | pre-shopify_ept: executing function migrate')
