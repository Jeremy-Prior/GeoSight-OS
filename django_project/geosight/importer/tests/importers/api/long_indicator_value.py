# coding=utf-8
"""
GeoSight is UNICEF's geospatial web-based business intelligence platform.

Contact : geosight-no-reply@unicef.org

.. note:: This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

"""
__author__ = 'irwan@kartoza.com'
__date__ = '13/06/2023'
__copyright__ = ('Copyright 2023, Unicef')

import responses

from core.settings.utils import ABS_PATH
from geosight.importer.exception import ImporterDoesNotExist
from geosight.importer.importers import IndicatorValueApiLongFormat
from geosight.importer.importers.base.indicator_value import (
    ImporterTimeDataType, AdminLevelType
)
from geosight.importer.models import Importer, ImportType, InputFormat
from geosight.importer.models.log import LogStatus
from ._base import BaseApiIndicatorValueTest


class ApiLongFormatIndicatorValueTest(BaseApiIndicatorValueTest):
    """Test for Importer : Api Long Format Indicator Value."""

    def setUp(self):
        """To setup tests."""
        super().setUp()
        self.importer = Importer.objects.create(
            import_type=ImportType.INDICATOR_VALUE,
            input_format=InputFormat.API_WITH_GEOGRAPHY_LONG,
            reference_layer=self.reference_layer
        )
        self.attributes.update({
            'key_administration_code': 'geom_code',
            'indicator_data_type': 'Data Driven',
            'indicator_data_field': 'indicator_shortcode',
            'date_time_data_type': ImporterTimeDataType.BY_VALUE,
            'date_time_data_value': '2010-01-01',
            'admin_level_type': AdminLevelType.BY_VALUE,
            'admin_level_value': 1,
            'key_value': 'value',
        })

    def test_error_importer(self):
        """Test if correct importer."""
        with self.assertRaises(ImporterDoesNotExist):
            Importer.objects.create(
                import_type=ImportType.INDICATOR_VALUE,
                input_format='test',
                reference_layer=self.reference_layer
            )

    def test_correct_importer(self):
        """Test if correct importer."""
        self.assertEqual(self.importer.importer, IndicatorValueApiLongFormat)

    @responses.activate
    def test_run_error_attributes(self):
        """Test if error attributes importer."""
        filepath = ABS_PATH(
            'geosight', 'importer', 'tests', 'importers',
            '_fixtures', 'excel_long_indicator_value_error.xlsx'
        )
        self.file_response(filepath)
        # by value but no date value
        attributes = {
            **self.attributes, **{
                'date_time_data_type': ImporterTimeDataType.BY_VALUE,
                'date_time_data_value': None
            }
        }
        self.importer.save_attributes(attributes, {})

        self.importer.run()
        self.assertEqual(
            self.importer.importerlog_set.all().first().status,
            LogStatus.FAILED
        )

        # data driven but no data value
        attributes = {
            **self.attributes, **{
                'date_time_data_type': ImporterTimeDataType.DATA_DRIVEN
            }
        }
        self.importer.save_attributes(attributes, {})
        self.importer.run()

        self.assertEqual(
            self.importer.importerlog_set.all().first().status,
            LogStatus.FAILED
        )

        # The list not found
        attributes = {
            **self.attributes, **{
                'key_feature_list': 'feature_error'
            }
        }
        self.importer.save_attributes(attributes, {})
        self.importer.run()

        self.assertEqual(
            self.importer.importerlog_set.all().first().status,
            LogStatus.FAILED
        )

    @responses.activate
    def test_run_error(self):
        """Test if correct importer."""
        filepath = ABS_PATH(
            'geosight', 'importer', 'tests', 'importers',
            '_fixtures', 'excel_long_indicator_value_error.xlsx'
        )
        self.file_response(filepath)

        attributes = self.attributes
        self.importer.save_attributes(attributes, {})
        self.importer.run()

        log = self.importer.importerlog_set.all().last()
        self.assertEqual(log.status, 'Failed')

    @responses.activate
    def test_run(self):
        """Test if correct importer."""
        filepath = ABS_PATH(
            'geosight', 'importer', 'tests', 'importers',
            '_fixtures', 'excel_long_indicator_value.xlsx'
        )
        self.file_response(filepath)

        attributes = self.attributes
        self.importer.save_attributes(attributes, {})
        self.assertImporter(self.importer)

    @responses.activate
    def test_run_using_date_time_field(self):
        """Test if correct importer."""
        filepath = ABS_PATH(
            'geosight', 'importer', 'tests', 'importers',
            '_fixtures', 'excel_long_indicator_value.xlsx'
        )
        self.file_response(filepath)

        attributes = {
            **self.attributes, **{
                'date_time_data_type': ImporterTimeDataType.DATA_DRIVEN,
                'date_time_data_field': 'date_time'
            }
        }
        self.importer.save_attributes(attributes, {})

        self.assertImporter(self.importer)

    @responses.activate
    def test_run_using_admin_type_data(self):
        """Test if correct importer."""
        filepath = ABS_PATH(
            'geosight', 'importer', 'tests', 'importers',
            '_fixtures', 'excel_long_indicator_value.xlsx'
        )
        self.file_response(filepath)

        attributes = {
            **self.attributes, **{
                'admin_level_type': 'Data Driven',
                'admin_level_field': 'admin_level'
            }
        }
        self.importer.save_attributes(attributes, {})
        self.assertImporterLevelByData(self.importer)
