##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import models, fields, _
from odoo.tools.safe_eval import safe_eval as eval
from fabric.api import run, cd, env
from odoo.exceptions import ValidationError
from .server import custom_sudo as sudo
from fabric.contrib.files import exists, append, sed
import errno
import time
import os


class server_configuration_command(models.Model):
    """"""

    _name = 'infrastructure.server_configuration_command'
    _description = 'server_configuration_command'
    _inherit = ['infrastructure.command']

    server_configuration_id = fields.Many2one(
        'infrastructure.server_configuration',
        string='server_configuration_id',
        ondelete='cascade',
        required=True
    )

    _order = "sequence"

    def execute_command(self):
        if context is None:
            context = {}
        user = self.env['res.users'].browse(uid)
        result = []
        server_id = context.get('server_id', False)
        if not server_id:
            raise ValidationError(_('No server in context'))
        server = self.env['infrastructure.server'].browse(
            cr, uid, server_id)
        for command in self.browse(ids):
            command_result = False
            env.user = server.user_name
            env.password = server.password
            env.host_string = server.main_hostname
            env.port = server.ssh_port
            cxt = {
                'self': self,
                'os': os,
                'errno': errno,
                'command': command,
                'run': run,
                'sudo': sudo,
                'server': server,
                'cd': cd,
                'pool': self.env,
                'time': time,
                'cr': cr,
                # Fabric file commands
                'exists': exists,
                'append': append,
                'sed': sed,
                # copy context to prevent side-effects of eval
                'context': dict(context),
                'uid': uid,
                'user': user,
            }
            # nocopy allows to return 'action'
            eval(command.command.strip(), cxt, mode="exec")
            if 'result' in cxt['context']:
                command_result = cxt['context'].get('result')
            result.append(command_result)
        return result
