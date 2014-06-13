#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pymongohashrec
----------------------------------

Tests for `pymongohashrec` module.
"""

import unittest

from pymongohashrec import *

class TestPymongoHashrec(unittest.TestCase):

    def setUp(self):
        pass

    def test_record_digest(self):
        self.assertEqual(record_digest({"foo": 1}), "8b9a9a1cf2b331258d4dfb4f46d49d7501db1fd7")
        self.assertEqual(record_digest({"a": 1, "b": 2, "c": 3}), "e20096b15530bd66a35a7332619f6666e2322070")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
