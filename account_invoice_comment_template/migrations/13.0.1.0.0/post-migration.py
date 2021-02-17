# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO base_comment_template_ir_model_rel
        (template_id, model_id)
        SELECT bct.id, (
            SELECT imd.id
            FROM ir_model_data imd
            WHERE imd.name = 'model_account_move'
            AND imd.module = 'account'
        ) AS model_id
        FROM base_comment_template bct
        WHERE bct.id IN (
            SELECT comment_template1_id
            FROM account_move
            WHERE comment_template1_id IS NOT NULL
        ) OR bct.id IN (
            SELECT comment_template2_id
            FROM account_move
            WHERE comment_template2_id IS NOT NULL
        )
        """,
    )
