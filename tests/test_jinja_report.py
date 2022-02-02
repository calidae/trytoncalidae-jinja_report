
import unittest
import trytond_factories

from trytond.pool import Pool
import trytond.tests.test_tryton
from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import with_transaction

from report import Jinja2Report


class JinjaReportTestCase(ModuleTestCase):
    'Test Jinja Report module'
    module = 'jinja_report'

    class TestReport(Jinja2Report):
        __name__ = 'jinja.test_report'

    @classmethod
    def setUpClass(cls):
        Pool.register(cls.TestReport, module='jinja_report', type_='report')
        activate_module(['tests', 'jinja_report'])

    @with_transaction()
    def test_jinja_report(self):
        # GIVEN
        report = trytond_factories.Report.create(
            model='test.model',
            report_name='jinja.test_report',
            extension='html',
            template_extension='html',
            report_content_custom=(
                b"{{ record.name }} {{ data.get('data') }}"
            ),
        )

        record = trytond_factories.TestModel.create(name='R3C0RD')

        # WHEN
        Report = Pool().get(report.report_name, type='report')
        (_, report_data, _, _) = Report.execute(
            [record.id], data={'data': 'D4T4'}
        )

        # THEN
        self.assertEqual(report_data, 'R3C0RD D4T4')

    @with_transaction()
    def test_jinja_report_attachment(self):
        # GIVEN
        record = trytond_factories.TestModel.create()
        trytond_factories.DataAttachment.create(
            resource=record,
            name='example.png',
            data=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00'
            b'\x00\x00\x02\x08\x02\x00\x00\x00\xfd\xd4\x9as\x00\x00\x00\x01'
            b'sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f'
            b'\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3'
            b'\x01\xc7o\xa8d\x00\x00\x00\x15IDAT\x18Wcxgd\xf5VN\x8d\x01\x88'
            b'\xdf\xdb\xb9\x02\x00&\xc4\x05/C\xee\xb8\xc6\x00\x00\x00\x00'
            b'IEND\xaeB`\x82',
        )
        report = trytond_factories.Report.create(
            model='test.model',
            report_name='jinja.test_report',
            extension='html',
            template_extension='html',
            report_content_custom=(
                b"{{ attachments(record, 'example.png') | b64encode }}"
            ),
        )
        Report = Pool().get(report.report_name, type='report')

        # WHEN
        (_, report_data, _, _) = Report.execute(ids=[record.id], data={})

        # THEN
        self.assertEqual(
            report_data,
            (
                "b'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAAXNSR0IArs"
                "4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAVSU"
                "RBVBhXY3hnZPVWTo0BiN/buQIAJsQFL0PuuMYAAAAASUVORK5CYII='"
            )
        )


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(
            JinjaReportTestCase
        )
    )
    return suite
