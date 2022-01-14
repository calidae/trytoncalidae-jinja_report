
from trytond.pool import Pool

__all__ = ['register']
from .report import SetTranslationJinja2


def register():
    Pool.register(SetTranslationJinja2, module='jinja_report', type_='wizard')
