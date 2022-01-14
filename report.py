__all__ = [
    'JinjaTranslator',
    'Jinja2Report',
    'SetTranslationJinja2',
]

import jinja2
from trytond.pool import Pool, PoolMeta
from trytond.report.report import TranslateFactory


class JinjaTranslator(object):

    def __init__(self, method):
        self.gettext = method
        self.ngettext = method
        self.ugettext = method
        self.ungettext = method


class Jinja2Report(metaclass=PoolMeta):

    JINJA_EXTENSIONS = [
        'jinja2.ext.i18n',
        'jinja2.ext.do',
        'jinja2.ext.loopcontrols',
    ]

    @classmethod
    def render(cls, action, context):
        env = cls.get_environ()
        template = env.from_string(action.report_content.decode())
        return template.render(**context)

    @classmethod
    def get_environ(cls):
        env = jinja2.Environment(extensions=cls.JINJA_EXTENSIONS)
        translations = cls.get_translations()
        env.install_gettext_translations(translations)
        return env

    @classmethod
    def get_translations(cls):
        translate = TranslateFactory(
            cls.__name__,
            Pool().get('ir.translation'),
        )
        return JinjaTranslator(lambda text: translate(text))


class SetTranslationJinja2(metaclass=PoolMeta):

    __name__ = 'ir.translation.set'

    def extract_report_html(self, content):
        try:
            yield from super().extract_report_html(content)
        except Exception:
            # Because trytond tries to manage any (x|ht)ml report
            # content with the picky genshi translation extractor,
            # the set-translations process will fail in presence of
            # reports tailored for other template languages like jinja2.
            env = jinja2.Environment(extensions=['jinja2.ext.i18n'])
            for _, _, str_ in env.extract_translations(content.decode()):
                if str_:
                    yield str_


def register():
    Pool.register(SetTranslationJinja2, module='jinja_report', type_='wizard')
