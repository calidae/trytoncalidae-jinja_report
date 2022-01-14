import unittest

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

        # TODO: Generate those records with factories when
        # trytond_factories contain those factories
        pool = Pool()
        ActionReport = pool.get('ir.action.report')
        Model = pool.get('test.model')

        action_report, = ActionReport.create([{
            'name': 'Test Report',
            'report': 'jinja_report/tests/report_template.html',
            'report_name': 'jinja.test_report',
            'model': 'test.model',
            'extension': 'pdf',
            'template_extension': 'html',
        }])

        # GIVEN
        records = Model.create([
            {'name': 'First rec'},
            {'name': 'Second rec'},
        ])
        Report = pool.get('jinja.test_report', type='report')
        report_context = Report.get_context(
            records, None, {'some_data': 'Some data'}
        )

        # WHEN
        result = Report.render(action_report, report_context)

        # THEN
        self.assertEqual(
            result,
            '<html><body>\n First rec Second rec\nSome data\n</body></html>'
        )


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(
            JinjaReportTestCase
        )
    )
    return suite
