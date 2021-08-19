##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import fields, api
from odoo import models


class infrastructure_copy_data_from_instance(models.TransientModel):
    _name = "infrastructure.copy_data_from_instance.wizard"
    _description = "Infrastructure Copy Data From Instance Wizard"

    @api.model
    def get_target_instance(self):
        return self.env['infrastructure.instance'].browse(
            self.env.context.get('active_id', False))

    source_instance_id = fields.Many2one(
        'infrastructure.instance',
        'Source Instance',
        required=True,
        ondelete='cascade',
        domain="[('server_id','=',server_id),"
        "('id','!=',target_instance_id),('state', '=', 'active')]",
    )
    server_id = fields.Many2one(
        'infrastructure.server',
        'Server',
        compute='get_server_and_source_instance',
    )
    target_instance_id = fields.Many2one(
        'infrastructure.instance',
        'Target Instance',
        readonly=True,
        required=True,
        ondelete='cascade',
        default=get_target_instance,
    )

    @api.depends('target_instance_id')
    def get_server_and_source_instance(self):
        self.server_id = self.target_instance_id.server_id
        target_instance = self.target_instance_id
        self.source_instance_id = self.env['infrastructure.instance'].search([
            ('environment_id', '=', target_instance.environment_id.id),
            ('advance_type', '=', 'protected')],
            limit=1)
        # self.source_instance_id = self.env['infrastructure.instance'].search(
        #     [('environment_id', '=', target_instance.environment_id.id),
        #         ('id', '!=', target_instance.id)],
        #     limit=1)

    def action_confirm(self):
        self.ensure_one()
        return self.target_instance_id.copy_databases_from(
            self.source_instance_id)
