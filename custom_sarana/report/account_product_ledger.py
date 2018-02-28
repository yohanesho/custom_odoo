# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError

class ReportGeneralLedger(models.AbstractModel):
    _name = 'report.custom_sarana.report_productledger'

    def _get_account_move_entry(self, accounts, categories, init_balance, sortby, display_account):
        """
        :param:
                accounts: the recordset of accounts
                init_balance: boolean value of initial_balance
                sortby: sorting by date or partner and journal
                display_account: type of account(receivable, payable and both)

        Returns a dictionary of accounts with following key and value {
                'code': account code,
                'name': account name,
                'debit': sum of total debit amount,
                'credit': sum of total credit amount,
                'balance': total balance,
                'amount_currency': sum of amount_currency,
                'move_lines': list of move line
        }
        """
        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = dict(map(lambda x: (x, []), categories.ids))

        # Prepare initial sql query and Get the initial move lines
        if init_balance:
            init_tables, init_where_clause, init_where_params = MoveLine.with_context(date_from=self.env.context.get('date_from'), date_to=False, initial_bal=True)._query_get()
            init_wheres = [""]
            if init_where_clause.strip():
                init_wheres.append(init_where_clause.strip())
            init_filters = " AND ".join(init_wheres)
            filters = init_filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')
            sql = ("""SELECT 0 AS lid, pc.id AS categ_id, '' AS ldate, '' AS lcode, NULL AS amount_currency, '' AS lref, 'Initial Balance' AS lname, COALESCE(SUM(l.debit),0.0) AS debit, COALESCE(SUM(l.credit),0.0) AS credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) as balance, '' AS lpartner_id,\
                '' AS move_name, '' AS mmove_id, '' AS currency_code,\
                NULL AS currency_id,\
                '' AS invoice_id, '' AS invoice_type, '' AS invoice_number,\
                '' AS partner_name\
                FROM account_move_line l\
                LEFT JOIN account_move m ON (l.move_id=m.id)\
                LEFT JOIN res_currency c ON (l.currency_id=c.id)\
                LEFT JOIN res_partner p ON (l.partner_id=p.id)\
                LEFT JOIN account_invoice i ON (m.id =i.move_id)\
                JOIN product_product pp ON (l.product_id=pp.id)\
                JOIN product_template pt ON (pp.product_tmpl_id=pt.id)\
                JOIN product_category pc ON (pt.categ_id=pc.id)\
                WHERE pc.id IN %s AND l.account_id IN %s""" + filters + ' GROUP BY pc.id')
            params = (tuple(categories.ids),) + (tuple(accounts.ids),) + tuple(init_where_params)
            cr.execute(sql, params)
            for row in cr.dictfetchall():
                move_lines[row.pop('categ_id')].append(row)

        sql_sort = 'l.date, l.move_id'
        if sortby == 'sort_category_product':
            sql_sort = 'pc.name,l.product_id,l.date, l.move_id, l.account_id'

        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = MoveLine._query_get()
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        filters = filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')

        # Get move lines base on sql query and Calculate the total balance of move lines
        sql = ('''SELECT l.id AS lid, pc.id as categ_id, l.date AS ldate, '[' || acc.code || ']-' || acc.name AS lcode, l.currency_id, l.amount_currency, l.ref AS lref, l.name AS lname, COALESCE(l.debit,0) AS debit, COALESCE(l.credit,0) AS credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) AS balance,\
            m.name AS move_name, c.symbol AS currency_code, p.name AS partner_name\
            FROM account_move_line l\
            JOIN account_move m ON (l.move_id=m.id)\
            LEFT JOIN res_currency c ON (l.currency_id=c.id)\
            LEFT JOIN res_partner p ON (l.partner_id=p.id)\
            JOIN product_product pp ON (l.product_id=pp.id)\
            JOIN product_template pt ON (pp.product_tmpl_id=pt.id)\
            JOIN product_category pc ON (pt.categ_id=pc.id)\
            JOIN account_account acc ON (l.account_id = acc.id) \
            WHERE pc.id IN %s AND l.account_id IN %s ''' + filters + ''' GROUP BY pc.id, l.id, acc.code, acc.name, l.date, pc.name, l.currency_id, l.amount_currency, l.ref, l.name, m.name, c.symbol, p.name ORDER BY ''' + sql_sort)
        params = (tuple(categories.ids),) + (tuple(accounts.ids),) + tuple(where_params)
        cr.execute(sql, params)

        for row in cr.dictfetchall():
            balance = 0
            for line in move_lines.get(row['categ_id']):
                balance += line['debit'] - line['credit']
            row['balance'] += balance
            move_lines[row.pop('categ_id')].append(row)

        # Calculate the debit, credit and balance for Accounts
        account_res = []
        for categ in categories:
            currency = self.env.user.company_id.currency_id
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            res['name'] = categ.name
            res['move_lines'] = move_lines[categ.id]
            for line in res.get('move_lines'):
                res['debit'] += line['debit']
                res['credit'] += line['credit']
                res['balance'] = line['balance']
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'movement' and res.get('move_lines'):
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)

        return account_res

    @api.model
    def render_html(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        init_balance = data['form'].get('initial_balance', True)
        sortby = data['form'].get('sortby', 'sort_date')
        display_account = data['form']['display_account']
        codes = []
        if data['form'].get('product_categ_ids', False):
            codes = [product_categ.name for product_categ in self.env['product.category'].search([('id', 'in', data['form']['product_categ_ids'])])]

        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        categories = self.env['product.category'].search([('id', 'in', data['form']['product_categ_ids'])])

        res = self.with_context(data['form'].get('used_context',{}), product_categ_ids=data['form']['product_categ_ids'])._get_account_move_entry(accounts, categories, init_balance, sortby, display_account)
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Categories': res,
            'print_category': codes,
        }
        return self.env['report'].render('custom_sarana.report_productledger', docargs)
