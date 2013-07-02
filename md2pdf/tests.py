# -*- coding: utf-8 -*-

import unittest
from md2pdf.core import md2pdf
from md2pdf.exceptions import ValidationError

class TestMarkdownToPDF(unittest.TestCase):

    def test_md2pdf(self):

        # no markdown content should raise a ValidationError
        self.assertRaises(ValidationError, md2pdf, 'foo.pdf')


if __name__ == '__main__':
    unittest.main()
