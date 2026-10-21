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

# 17.0 views whose records no longer exist in the 19.0 code. Odoo only deletes
# them at the end of the upgrade, so while the remaining modules load they are
# still part of the combined arch:
# - l10n_cl_customer_reference.res_config_settings_view_form adds the field
#   l10n_cl_strict_customer_po_reference_validation, which only ever existed in
#   17.0 (never forward-ported). As soon as l10n_cl_customer_reference is
#   updated the field is gone, and the next module that validates a
#   res.config.settings view (l10n_cl_edi_docsonline_connect) fails with
#   ParseError and the registry does not load.
# - l10n_cl_edi_docsonline_connect: invoice views dropped in 19.0, removed here
#   for the same reason.
REMOVE_VIEW = [
    'l10n_cl_customer_reference.res_config_settings_view_form',
    'l10n_cl_edi_docsonline_connect.view_in_invoice_tree',
    'l10n_cl_edi_docsonline_connect.view_in_refund_invoice_tree',
    'l10n_cl_edi_docsonline_connect.view_invoice_gen_tree',
    'l10n_cl_edi_docsonline_connect.view_out_invoice_form',
    'l10n_cl_edi_docsonline_connect.view_out_invoice_tree',
    'l10n_cl_edi_docsonline_connect.view_out_refund_invoice_tree',
]


def migrate(cr, version):
    _logger.info('BMYA-script | fields_client_order_ref 19.0.0.1: removing modules stuck in an inconsistent state')
    for module in UNINSTALL_MODULE:
        util.remove_module(cr, module)
    _logger.info('BMYA-script | fields_client_order_ref 19.0.0.1: removing 17.0 views dropped in 19.0')
    util.remove_views(cr, *REMOVE_VIEW)
