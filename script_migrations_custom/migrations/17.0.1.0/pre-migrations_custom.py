import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)

UNINSTALL_MODULE = ['l10n_cl_hr_expense', 'clear_data']
# UNINSTALL_MODULE = ['l10n_cl_hr_expense', 'stock_no_negative', 'account_bank_statement_online_import_fintoc'
#                     'common_connector_library_forecast_fix', 'script_migration_common_connector_library'
#                     'script_migration_shopify_ept', 'shopify_ept', 'common_connector_library', 'studio_customization']
# DELETE_ASSETS = ['shopify_ept', 'common_connector_library'] + UNINSTALL_MODULE


def migrate(cr, version):
    _logger.info('BMYA-script | pre-migrations_custom: executing function migrate')
    for module in UNINSTALL_MODULE:
        util.remove_module(cr, module)
    # for module in DELETE_ASSETS:
    #     cr.execute("DELETE FROM ir_asset WHERE path LIKE '/{}%';".format(module))
    cr.execute("DELETE FROM ir_ui_view WHERE id=3012;")
