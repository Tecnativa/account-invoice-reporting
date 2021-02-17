# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2019 Iván Todorovich (Druidoo)
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    comment_template1_id = fields.Many2one(
        "base.comment.template",
        string="Top Comment Template",
        domain=[
            ("model_ids.model", "=", "account.move"),
            ("position", "=", "before_lines"),
        ],
    )

    comment_template2_id = fields.Many2one(
        "base.comment.template",
        string="Bottom Comment Template",
        domain=[
            ("model_ids.model", "=", "account.move"),
            ("position", "=", "after_lines"),
        ],
    )

    note1 = fields.Html("Top Comment")
    note2 = fields.Html("Bottom Comment")

    @api.onchange("comment_template1_id")
    def _set_note1(self):
        comment = self.comment_template1_id
        if comment:
            self.note1 = comment.text

    @api.onchange("comment_template2_id")
    def _set_note2(self):
        comment = self.comment_template2_id
        if comment:
            self.note2 = comment.text

    @api.depends("partner_id")
    def get_comment_template_item(self, position):
        return self.env["base.comment.template"].search(
            [
                ("model_ids.model", "=", "account.move"),
                ("position", "=", position),
                ("partner_ids", "in", self.partner_id.ids),
            ],
            limit=1,
        )

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        # before_lines
        comment_template = self.get_comment_template_item("before_lines")
        if comment_template:
            self.comment_template1_id = comment_template
            self._set_note1()
        # after_lines
        comment_template = self.get_comment_template_item("after_lines")
        if comment_template:
            self.comment_template2_id = comment_template
            self._set_note2()
        return res
