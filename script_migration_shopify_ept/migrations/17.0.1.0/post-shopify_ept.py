import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info('BMYA-script | post-shopify_ept: executing function migrate')
