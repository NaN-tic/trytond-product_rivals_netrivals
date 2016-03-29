# This file is part product_rivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import urllib2
from xml.dom import minidom
from decimal import Decimal
from trytond.pool import Pool, PoolMeta

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
        pool = Pool()
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        Rivals = pool.get('product.rivals')

        values = {}
        to_create = []
        to_write = []
        template_write = []

        usock = urllib2.urlopen(self.app_uri) 
        xmldoc = minidom.parse(usock)

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
                'min_price': min_price,
                'max_price': max_price,
                }

        codes = values.keys()
        products = Product.search([
            ('code', 'in', codes),
            ])

        for p in products:
            if p.code in values:
                rivals = values[p.name]['rivals']
                product_rivals = {}
                for n in p.rivals:
                    product_rivals[n.name] = n

                for rival in rivals:
                    if rival in product_rivals: # write
                        to_write.extend(([product_rivals[rival]], {
                            'price': Decimal(rivals[rival]),
                            }))
                    else: # create
                        to_create.append({
                            'product': p,
                            'name': rival,
                            'price': Decimal(rivals[rival]),
                            })

                # min and max rivals price
                rival_prices = {}
                min_price = values[p.name]['min_price']
                if min_price:
                    rival_prices['list_price_min_rival'] = min_price
                max_price = values[p.name]['max_price']
                if max_price:
                    rival_prices['list_price_max_rival'] = max_price
                if rival_prices:
                    template_write.extend(([p.template], rival_prices))

        if to_create:
            Rivals.create(to_create)
        if to_write:
            Rivals.write(*to_write)
        if template_write:
            Template.write(*template_write)
