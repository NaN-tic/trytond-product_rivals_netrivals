# This file is part product_rivals_netrivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .rivals import *

def register():
    Pool.register(
        ProductAppRivals,
        module='product_rivals_netrivals', type_='model')
