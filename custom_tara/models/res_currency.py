from openerp import models, fields, api, _

class res_currency(models.Model):
    
    _inherit = 'res.currency'
    currency_name = fields.Char(
        string=u'Name',
    )
    
    dic = {       
        'to_19' : ('Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'),
        'tens'  : ('Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'),
        'denom' : ('', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion', 'Quintillion'),        
        'to_19_id' : ('Nol', 'Satu', 'Dua', 'Tiga', 'Empat', 'Lima', 'Enam', 'Tujuh', 'Delapan', 'Sembilan', 'Sepuluh', 'Sebelas', 'Dua Belas', 'Tiga Belas', 'Empat Belas', 'Lima Belas', 'Enam Belas', 'Tujuh Belas', 'Delapan Belas', 'Sembilan Belas'),
        'tens_id'  : ('Dua Puluh', 'Tiga Puluh', 'Empat Puluh', 'Lima Puluh', 'Enam Puluh', 'Tujuh Puluh', 'Delapan Puluh', 'Sembilan Puluh'),
        'denom_id' : ('', 'Ribu', 'Juta', 'Miliar', 'Triliun', 'Biliun')
    }
    
    @api.one
    def amount_to_text(self, amount, lang):
        amount = '%.2f' % amount
        units_name = ' ' + self.currency_name if self.currency_name else self.name + ' '
        lis = str(amount).split('.')
        start_word = self.english_amount(int(lis[0]), lang)
        end_word = self.english_amount(int(lis[1]), lang)
        cents_amount = int(lis[1])
        cents_name = (cents_amount > 1) and 'Sen' or 'sen'
        final_result_sen = start_word + units_name + end_word +' '+cents_name
        final_result = start_word + units_name
        if end_word == 'Nol' or end_word == 'Zero':
            final_result = final_result
        else:
            final_result = final_result_sen
        
        return final_result[:1].upper()+final_result[1:]
    
    def _convert_nn(self, val, lang='en'):
        tens = self.dic['tens_id']
        to_19 = self.dic['to_19_id']
        if lang == 'en':
            tens = self.dic['tens']
            to_19 = self.dic['to_19']
        if val < 20:
            return to_19[val]
        for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
            if dval + 10 > val:
                if val % 10:
                    return dcap + ' ' + to_19[val % 10]
                return dcap
    
    def _convert_nnn(self, val, lang):
        word = ''; rat = ' Ratus'; to_19 = self.dic['to_19_id']
        if lang == 'en':
            rat = ' Hundred'
            to_19 = self.dic['to_19']
        (mod, rem) = (val % 100, val // 100)
        if rem == 1:
            word = 'Seratus'
            if mod > 0:
                word = word + ' '   
        elif rem > 1:
            word = to_19[rem] + rat
            if mod > 0:
                word = word + ' '
        if mod > 0:
            word = word + self._convert_nn(mod, lang)
        return word
    
    def english_amount(self, val, lang):
        denom = self.dic['denom_id']
        if lang == 'en':
            denom = self.dic['denom']
        if val < 100:
            return self._convert_nn(val, lang)
        if val < 1000:
            return self._convert_nnn(val, lang)
        for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
            if dval > val:
                mod = 1000 ** didx
                l = val // mod
                r = val - (l * mod)
                ret = self._convert_nnn(l, lang) + ' ' + denom[didx]
                if r > 0:
                    ret = ret + ' ' + self.english_amount(r, lang)
                if lang == 'id':
                    if val < 2000:
                        ret = ret.replace("Satu Ribu", "Seribu")
                return ret