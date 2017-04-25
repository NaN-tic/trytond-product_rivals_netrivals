# This file is part product_rivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import urllib2
from xml.dom import minidom
from decimal import Decimal
from trytond.pool import PoolMeta

__all__ = ['ProductAppRivals']


class ProductAppRivals:
    __name__ = 'product.app.rivals'
    __metaclass__ = PoolMeta

    @classmethod
    def get_app(cls):
        res = super(ProductAppRivals, cls).get_app()
        res.append(('netrivals', 'Netrivals'))
        return res

    def update_prices_netrivals(self):
        usock = urllib2.urlopen(self.app_uri)
        xmldoc = minidom.parse(usock)

        values = {}
        for e in xmldoc.getElementsByTagName('Product'):
            code = e.getElementsByTagName('MPN')[0].firstChild.data # code
            min_price = e.getElementsByTagName('RivalMinPrice')[0].firstChild.data
            max_price = e.getElementsByTagName('RivalMaxPrice')[0].firstChild.data
            rivals = {}
            for r in e.getElementsByTagName('Rivals')[0].getElementsByTagName('Rival'):
                rival_name = r.getElementsByTagName('Name')[0].firstChild.data
                rival_price = r.getElementsByTagName('Price')[0].firstChild.data
                rivals[rival_name] = rival_price
            values[code] = {
                'rivals': rivals,
                'min_price': Decimal(min_price),
                'max_price': Decimal(max_price),
                }

        self.create_rivals(values)
