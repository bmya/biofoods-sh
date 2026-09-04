import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)

# Modules stuck in an inconsistent state during the 17.0 -> 19.0 upgrade:
# - common_connector_library_forecast_fix, shopify_tax_configuration: kept
#   installable=False on purpose (see their manifests), but the database still
#   has them installed/to-upgrade from 17.0.
# - script_migration_common_connector_library, script_migration_shopify_ept,
#   script_migrations_custom: one-off 15.0->17.0 migration housekeeping
#   modules, already served their purpose (their manifests never got a 19.0
#   version, so Odoo auto-disables them - but the database still has them
#   installed/to-upgrade, and script_migrations_custom depends on the other
#   two so all three must go together).
# - l10n_cl_edi_skip_date_validation: ships installable=False upstream in
#   bmya-enterprise; the database still has it installed/to-upgrade.
UNINSTALL_MODULE = [
    'common_connector_library_forecast_fix',
    'shopify_tax_configuration',
    'script_migration_common_connector_library',
    'script_migration_shopify_ept',
    'script_migrations_custom',
    'l10n_cl_edi_skip_date_validation',
]


def migrate(cr, version):
    _logger.info('BMYA-script | fields_client_order_ref 19.0.0.1: removing modules stuck in an inconsistent state')
    for module in UNINSTALL_MODULE:
        util.remove_module(cr, module)
