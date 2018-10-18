from odoo import api, fields, models, _
import datetime
import calendar
import time

MARFOR_STATES = [('new', 'New'), ('validated', 'Validated'), ('finalized', 'Finalized')]

class MarketingForecast(models.Model):
    _name = 'marketing_forecast.marfor'

    doc_number = fields.Char(String="Document Number", required=True)
    from_date = fields.Date(required=True, default=lambda self: self._get_1st_day_of_the_month())
    to_date = fields.Date(required=True, default=lambda self: self._get_last_day_of_the_month())


    product_ids = fields.One2many(
        'marketing_forecast.marfor_detail', 'marketing_forecast_id', string='Detail')

    remain_ids = fields.One2many(
        'marketing_forecast.remain', 'marketing_forecast_id', string='Remain Forecast')

    forecast_qty_detail_ids = fields.One2many(
        'marketing_forecast.forecast_qty_detail', 'marketing_forecast_id', string='Forecast Qty Detail')

    forecast_qty_ids = fields.One2many(
        'marketing_forecast.forecast_qty', 'marketing_forecast_id', string='Forecast Qty Header')

    state = fields.Selection(string="State", selection=MARFOR_STATES, required=True, readonly=True, default=MARFOR_STATES[0][0])

    @api.model
    def _get_1st_day_of_the_month(self):
        todayDate = datetime.date.today()
            # if todayDate.day > 25:
            #     todayDate += datetime.timedelta(7)
        return todayDate.replace(day=1)

    @api.model
    def _get_last_day_of_the_month(self):
        todayDate = datetime.date.today()
        return todayDate.replace(day=calendar.monthrange(todayDate.year, todayDate.month)[1])

    @api.multi
    def btn_show_table(self):
        for record in self:
            # cat_marfor = self.env['product.category'].search([('marketing_forecast_flag', '=', True)])
            # cat_marfor_ids = [{cat_data.id} for cat_data in cat_marfor]
            #
            # product = self.env['product.template'].search([('categ_id', 'in', cat_marfor_ids),('active', '=', True)])

            product = self.env['product.template'].search([('marketing_forecast_flag', '=', True),('active', '=', True)])

            attr_data = [{'product_id':attr.id} for attr in product]
            self.product_ids = [(0, 0, data) for data in attr_data]

    @api.multi
    def action_state_validate(self):
        self.state = MARFOR_STATES[1][0]

        self.insert_forecast_remain()

    @api.multi
    def action_state_finalize(self):
       self.state = MARFOR_STATES[2][0]
       self.insert_forecast_finalize()

    @api.multi
    def action_state_new(self):
        self.state = MARFOR_STATES[0][0]

    def insert_forecast_remain(self):
        # insert data to table marketing_forecast_remain
        for record in self:
            product_categ_ids = []
            for data in self.product_ids:
                product_categ_ids.append(
                    {
                        data.product_id.categ_id.id
                    })

                orang_tua_category = data.product_id.categ_id.parent_id.id
                if orang_tua_category != False:
                    done = True
                    while (done == True):
 #                       print orang_tua_category
                        product_categ_ids.append({orang_tua_category})
                        orang_tua_category = self.env['product.category'].search([('id', '=', orang_tua_category)]).parent_id.id
                        if orang_tua_category == False:
                            done = False

            product_in_category_ids = self.env['product.category.detail'].search([('category_bom_id', 'in', product_categ_ids)])

#            print product_in_category_ids

            data_detail = [
                {
                    'qty': data.product_qty,
                    'product_id': data.product_id.id,
                    'categ_id': data.product_id.categ_id.id
                }

                for data in product_in_category_ids
            ]

#            print data_detail

            data_remain = []
            for data_detail_loop in data_detail:
 #               print 'masuk'
                for detail_marfor in self.product_ids:
                    if \
                                            bool(data_detail_loop['categ_id'] == detail_marfor.categ_id.id) \
                                    != \
                                            bool(data_detail_loop['categ_id'] == detail_marfor.categ_id.parent_id.id):

                        check_data_existing = self.env['marketing_forecast.forecast_qty'].search(
                            [('product_id', '=', data_detail_loop['product_id'])]
                        )

                        qty_remain = data_detail_loop['qty'] * detail_marfor.diff_qty
                        qty_sisa = 0
                        if check_data_existing.id != False:
                            if check_data_existing.qty >= qty_remain:
                                qty_sisa = check_data_existing.qty - qty_remain
                                qty_remain = 0
                            else:
                                qty_remain = qty_remain - check_data_existing.qty
                                qty_sisa = 0

                            if check_data_existing.qty != qty_sisa:
                                #insert data to marketing_forecast_forecast_qty_detail
                                MarforQtyDetailInsert = self.env['marketing_forecast.forecast_qty_detail'].create(
                                    {
                                        'marketing_forecast_id': self.id,
                                        'marketing_forecast_detail_id': detail_marfor.id,
                                        'product_id': data_detail_loop['product_id'],
                                        'qty': (check_data_existing.qty - qty_sisa) * -1,
                                        'categ_id': data_detail_loop['categ_id']
                                    }
                                )

                                print {
                                        'marketing_forecast_id': self.id,
                                        'marketing_forecast_detail_id': detail_marfor.id,
                                        'product_id': data_detail_loop['product_id'],
                                        'qty': (check_data_existing.qty - qty_sisa) * -1,
                                        'categ_id': data_detail_loop['categ_id']
                                    }

                                #update value qty in marketing_forecast_forecast_qty table
                                MarforQtyUpdate = self.env['marketing_forecast.forecast_qty'].browse(
                                    check_data_existing.id)
                                MarforQtyUpdate.write(
                                    {
                                        'qty': qty_sisa
                                    }
                                )

                        data_remain.append(
                            {
                                'marketing_forecast_id': self.id,
                                'marketing_forecast_detail_id': detail_marfor.id,
                                'qty': qty_remain,
                                'product_id': data_detail_loop['product_id']
                            }
                        )

  #          print data_remain

        self.remain_ids = [(0, 0, data) for data in data_remain]

    def insert_forecast_finalize(self):
        # insert data to table marketing_forecast_qty
        for record in self:
            product_categ_ids = []
            for data in self.product_ids:
                product_categ_ids.append(
                    {
                        data.product_id.categ_id.id
                    })

                orang_tua_category = data.product_id.categ_id.parent_id.id
                if orang_tua_category != False:
                    done = True
                    while (done == True):
                        #                        print orang_tua_category
                        product_categ_ids.append({orang_tua_category})
                        orang_tua_category = self.env['product.category'].search(
                            [('id', '=', orang_tua_category)]).parent_id.id
                        if orang_tua_category == False:
                            done = False

            product_in_category_ids = self.env['product.category.detail'].search(
                [('category_bom_id', 'in', product_categ_ids)])

            #            print product_in_category_ids

            data_detail = [
                {
                    'qty': data.product_qty,
                    'product_id': data.product_id.id,
                    'categ_id': data.product_id.categ_id.id
                }

                for data in product_in_category_ids
                ]

            #            print data_detail

            data_remain = []
            grouping_product_qty = [] #create dictionary to store data for forecast qty
            print "=========================================================================================="
            for data_detail_loop in data_detail:
                tmp_product_id = tmp_qty = ""
                for detail_marfor in self.product_ids:
                    if \
                                    bool(data_detail_loop['categ_id'] == detail_marfor.categ_id.id) \
                                    != \
                                    bool(data_detail_loop['categ_id'] == detail_marfor.categ_id.parent_id.id):

                        data_remain.append(
                            {
                                'marketing_forecast_id': self.id,
                                'marketing_forecast_detail_id': detail_marfor.id,
                                'qty': data_detail_loop['qty'] * detail_marfor.diff_qty,
                                'product_id': data_detail_loop['product_id']
                            }
                        )

                        check_data_existing = self.env['marketing_forecast.forecast_qty'].search(
                            [('product_id', '=', data_detail_loop['product_id'])]
                        )

                        # print "Debug ucok ", check_data_existing
                        # print "Debug ucok ID", check_data_existing.id

                        if check_data_existing.id != False:
                            MarforQtyUpdate = self.env['marketing_forecast.forecast_qty'].browse(check_data_existing.id)
                            print "id yang di update = ", check_data_existing.id, " Qty nya = ", check_data_existing.qty, " Menjadi =" , (data_detail_loop['qty'] * detail_marfor.diff_qty) + check_data_existing.qty

                            MarforQtyUpdate.write(
                                {
                                    'qty': (data_detail_loop['qty'] * detail_marfor.diff_qty) + check_data_existing.qty,
                                    'product_id': data_detail_loop['product_id']
                                }
                            )

                        elif tmp_product_id == data_detail_loop['product_id']:
                            for d in grouping_product_qty:
                                d.update(('qty', (d['qty']+(data_detail_loop['qty'] * detail_marfor.diff_qty))) for k,v in d.iteritems() if k == "product_id" and v == data_detail_loop['product_id'])

                        else:
                            grouping_product_qty.append(
                                {
                                    'qty': data_detail_loop['qty'] * detail_marfor.diff_qty,
                                    'product_id': data_detail_loop['product_id'],
                                }
                            )

                        tmp_product_id = data_detail_loop['product_id']
                        tmp_qty = data_detail_loop['product_id']

                    print grouping_product_qty
            print "============================================================================================="

        self.forecast_qty_detail_ids = [(0, 0, data) for data in data_remain]
        self.forecast_qty_ids = [(0, 0, data) for data in grouping_product_qty]

    def execute_sql(self,query):
        self._cr.execute(query)
        _hasil = self._cr.dictfetchall()
        return _hasil

class MarketingForecastDetail(models.Model):
    _name = 'marketing_forecast.marfor_detail'
    marketing_forecast_id = fields.Many2one(
        'marketing_forecast.marfor', 'Header',
        index=True, ondelete='cascade')

    state = fields.Selection(String="State", related='marketing_forecast_id.state', selection=MARFOR_STATES)

    product_id = fields.Many2one(
        'product.template', 'Product',
        index=True, ondelete='cascade')

    name = fields.Char(related='product_id.name', store=True)
    default_code = fields.Char(String='Internal Reference', related='product_id.default_code', store=True)
    categ_id = fields.Many2one('product.category', 'Internal Category',related='product_id.categ_id', store=True)

    qty_forecast = fields.Float()
    qty_produce = fields.Float()
    diff_qty = fields.Float(compute="_diff_qty", string="Diff Qty", store=True)

    @api.depends('qty_forecast', 'qty_produce')
    def _diff_qty(self):
        for detail in self:
            detail.diff_qty = detail.qty_forecast - detail.qty_produce

    @api.multi
    def _validate_qty_produce(self):
        for data in self:
            if data.qty_produce > data.qty_forecast:
                return False
            return True

    _constraints = [
        (_validate_qty_produce, 'Qty Produce must be less than Qty Forecast', [])
    ]

class ProductCategoryInherit(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    marketing_forecast_flag = fields.Boolean(string="Marketing Forecast", store=True)

class ForecastRemain(models.Model):
    _name = 'marketing_forecast.remain'

    marketing_forecast_id = fields.Many2one(
        'marketing_forecast.marfor', 'Marketing Forecast',
        index=True, ondelete='cascade')

    marketing_forecast_detail_id = fields.Many2one(
        'marketing_forecast.marfor_detail', 'Marketing Forecast Detail',
        index=True, ondelete='cascade')

    product_id = fields.Many2one(
        'product.template', 'Product',
        index=True, ondelete='cascade')

    qty = fields.Float()

    categ_id = fields.Many2one('product.category', 'Internal Category',related='product_id.categ_id', store=True)




class ForecastQty(models.Model):
    _name = 'marketing_forecast.forecast_qty'

    product_id = fields.Many2one(
        'product.template', 'Product',
        index=True, ondelete='cascade')

    qty = fields.Float()

    marketing_forecast_id = fields.Many2one(
        'marketing_forecast.marfor', 'Marketing Forecast',
        index=True, ondelete='cascade', store=True)



class ForecastQtyDetail(models.Model):
    _name = 'marketing_forecast.forecast_qty_detail'

    marketing_forecast_id = fields.Many2one(
        'marketing_forecast.marfor', 'Marketing Forecast',
        index=True, ondelete='cascade')

    marketing_forecast_detail_id = fields.Many2one(
        'marketing_forecast.marfor_detail', 'Marketing Forecast Detail',
        index=True, ondelete='cascade')

    product_id = fields.Many2one(
        'product.template', 'Product',
        index=True, ondelete='cascade')

    qty = fields.Float()

    categ_id = fields.Many2one('product.category', 'Internal Category',related='product_id.categ_id', store=True)

