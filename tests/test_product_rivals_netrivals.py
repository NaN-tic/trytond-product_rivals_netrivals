# This file is part product_rivals_netrivals module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class ProductRivalsNetrivalsTestCase(ModuleTestCase):
    'Test Product Rivals Netrivals module'
    module = 'product_rivals_netrivals'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductRivalsNetrivalsTestCase))
    return suite
