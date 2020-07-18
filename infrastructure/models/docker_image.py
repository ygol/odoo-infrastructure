# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class infrastructure_docker_image(models.Model):
    _name = 'infrastructure.docker_image'
    _description = 'Docker Image'

    name = fields.Char(
        'Name',
        required=True,
    )
    prefix = fields.Char(
        'Prefix',
    )
    pull_name = fields.Char('Pull Name', required=True)
    tag_ids = fields.One2many('infrastructure.docker_image.tag', 'docker_image_id', 'Tags')
    odoo_version_id = fields.Many2one('infrastructure.odoo_version', 'Odoo Version')
    service = fields.Selection([('odoo', 'Odoo'), ('postgresql', 'Postgresql'), ('nginx', 'Nginx'),('other', 'Other')], string='Service', default='odoo', required=True)
    pg_image_ids = fields.Many2many('infrastructure.docker_image', 'infrastructure_odoo_pg_image_rel', 'odoo_image_id', 'pg_image_id', string='Postgresql Images', domain=[('service', '=', 'postgresql')], help='Compatible Postgresql Images')
    odoo_image_ids = fields.Many2many('infrastructure.docker_image', 'infrastructure_odoo_pg_image_rel', 'pg_image_id', 'odoo_image_id', string='Odoo Images', domain=[('service', '=', 'odoo')], help='Compatible Odoo Images')
    odoo_data_dir = fields.Char(string='Odoo Data Directory', default='/var/lib/odoo')
    odoo_extra_addons_dir = fields.Char('Odoo Custom/Extra Addons', default='/mnt/extra-addons')
    odoo_etc_dir = fields.Char(string='Odoo Configuration Directory', default='/etc/odoo')
    odoo_config_file = fields.Char(string='Odoo Config File', default='odoo.conf')
    odoo_log_file = fields.Char(string='Odoo Log File', default='/etc/odoo/odoo.log')
    odoo_server_wide_modules = fields.Char()


class infrastructure_docker_image_tag(models.Model):
    _name = 'infrastructure.docker_image.tag'
    _description = 'Docker Image Tag'
    _order = 'sequence'

    name = fields.Char(
        'Name',
        required=True,
    )
    sequence = fields.Integer(
        'Name',
        default=10,
    )
    docker_image_id = fields.Many2one(
        'infrastructure.docker_image',
        'Name',
        required=True,
        ondelete='cascade',
    )
