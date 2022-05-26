# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    first_contract_date = fields.Date(related='employee_id.first_contract_date', groups="base.group_user")
    contract_id = fields.Many2one(related='employee_id.contract_id', groups="base.group_user")

    def action_open_contract_history(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id('hr_contract.hr_contract_history_view_form_action')
        action['res_id'] = self.id
        return action