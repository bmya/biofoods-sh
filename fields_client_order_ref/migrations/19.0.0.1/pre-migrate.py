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

# shopify_l10n_cl depends on shopify_attribute_mapping in 19.0, a module that
# did not exist in 17.0. The upgrade does not install new dependencies by
# itself, so without this shopify_l10n_cl is left unloaded and on 17.0.
# Plain SQL instead of util.force_install_module: by the time this script runs
# base is already loaded (not 'to upgrade'), and in that case
# force_install_module goes through upgrade-util's auto-discovery, meant for
# pre/post scripts of base. Marking the module 'to install' is enough: the
# loading loop installs it and then picks up shopify_l10n_cl.
INSTALL_MODULE = [
    ('shopify_attribute_mapping', 'shopify_l10n_cl'),
]


def migrate(cr, version):
    _logger.info('BMYA-script | fields_client_order_ref 19.0.0.1: removing modules stuck in an inconsistent state')
    for module in UNINSTALL_MODULE:
        util.remove_module(cr, module)
    _logger.info('BMYA-script | fields_client_order_ref 19.0.0.1: removing 17.0 views dropped in 19.0')
    util.remove_views(cr, *REMOVE_VIEW)
    _logger.info('BMYA-script | fields_client_order_ref 19.0.0.1: installing new dependencies of 19.0 modules')
    for module, if_installed in INSTALL_MODULE:
        cr.execute(
            """
            UPDATE ir_module_module
               SET state = 'to install'
             WHERE name = %s
               AND state = 'uninstalled'
               AND EXISTS (SELECT 1 FROM ir_module_module
                            WHERE name = %s
                              AND state IN ('installed', 'to upgrade'))
            """,
            [module, if_installed],
        )
        _logger.info('BMYA-script | %s marked to install: %s', module, bool(cr.rowcount))
