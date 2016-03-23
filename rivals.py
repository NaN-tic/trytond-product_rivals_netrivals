# This file is part product_rivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import urllib2
from xml.dom import minidom
from decimal import Decimal
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool

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
        Product = pool.get('product.product')
        Rivals = pool.get('product.rivals')

        #~ TODO el precio que quiero saber es el precio mas bajo "RivalMinPrice"
        
        values = {}
        to_create = []
        to_write = []

        usock = urllib2.urlopen(self.app_uri) 
        xmldoc = minidom.parse(usock)

        for e in xmldoc.getElementsByTagName('Product'):
            name = e.getElementsByTagName('Title')[0].firstChild.data
            min_price = e.getElementsByTagName('RivalMinPrice')[0].firstChild.data
            rivals = {}
            for r in e.getElementsByTagName('Rivals')[0].getElementsByTagName('Rival'):
                rival_name = r.getElementsByTagName('Name')[0].firstChild.data
                rival_price = r.getElementsByTagName('Price')[0].firstChild.data
                rivals[rival_name] = rival_price
            values[name] = rivals

        names = values.keys()
        products = Product.search([
            ('name', 'in', names),
            ])
    
        for p in products:
            if p.name in values:
                rivals = values[p.name]
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

        # TODO min_price

        if to_create:
            Rivals.create(to_create)
        if to_write:
            Rivals.write(*to_write)
