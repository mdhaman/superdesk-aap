# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import os
import unittest

from xml.etree import ElementTree
from aap.io.feed_parsers.ReutersNewsMLTwoFeedParser import ReutersNewsMLTwoFeedParser


class BaseNewMLTwoTestCase(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fixture = os.path.normpath(os.path.join(dirname, '../fixtures', self.filename))
        provider = {'name': 'Test'}
        with open(fixture, 'rb') as f:
            self.parser = ReutersNewsMLTwoFeedParser()
            self.xml = ElementTree.parse(f)
            self.item = self.parser.parse(self.xml.getroot(), provider)


class ReutersTestCase(BaseNewMLTwoTestCase):
    filename = 'tag:reuters.com,0000:newsml_L4N1FL0N0:1132689232'

    def test_content(self):
        self.assertEqual(self.item[0].get('headline'), "PRECIOUS-Gold rises as Trump policy fuels safe haven demand")
        self.assertEqual(self.item[0].get('guid'), 'tag:reuters.com,0000:newsml_L4N1FL0N0:1132689232')
        self.assertEqual(self.item[0].get('uri'), 'tag:reuters.com,0000:newsml_L4N1FL0N0')
        self.assertEqual(self.item[0].get('firstcreated').isoformat(), '2017-01-31T03:47:29')
        self.assertTrue(self.item[0].get('body_html').startswith('<p>(Adds comments, detail)</p>'))

    def test_can_parse(self):
        self.assertTrue(ReutersNewsMLTwoFeedParser().can_parse(self.xml.getroot()))


class ReutersResultsTestCase(BaseNewMLTwoTestCase):
    filename = 'tag:reuters.com,0000:newsml_ISS149709:1618095828'

    def test_results(self):
        self.assertTrue(self.item[0].get('body_html').startswith(
            '<p>Jan 30 (Gracenote) - Results and standings from the Turkish championship matches on Monday <br/>'))


class ReutersOptaTestCase(BaseNewMLTwoTestCase):
    filename = 'tag:reuters.com,2018:newsml_MTZXEE13ZXCZES:2'

    def test_body(self):
        self.assertTrue(self.item[0].get('body_html').startswith('<pre>Jan 3 (OPTA) - Results and fixtures for the '
                                                                 'Primeira'))


class ReutersWithLineBreaks(BaseNewMLTwoTestCase):
    filename = 'tag:reuters.com,2018:newsml_L3N1X604Z:536317572'

    def test_body(self):
        self.assertTrue(self.item[0].get('body_html').startswith('<p>* MSCI Asia Ex-Japan -0.06 pct</p>\n<p>* Amazon'
                                                                 ', Alphabet earnings disappoint</p>\n<p>* Euro '
                                                                 'falls '))
        self.assertTrue('<p>SHANGHAI, Oct 26 (Reuters) - Asian shares wobbled in early Friday trade, struggling' in
                        self.item[0].get('body_html'))
