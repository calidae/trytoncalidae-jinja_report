# Jinja Reports module

jinja_reports is a [jinja2](https://jinja.palletsprojects.com) extension developed to work with [Tryton ERP](https://www.tryton.org/).
We can create our own reports based on jinja2 with html templates.

## How does it work?

Steps to use Jinja Reports:
1. Inherit the base Jinja2Report class.
2. Define the meta model name.
3. Create an html template.
4. Create an action report pointing to template path and model name.

## Example

Here's a an example of a report which contains three files.

1. Python class that must be registered to the Tryton Pool.

```python
from trytond.modules.jinja_report.report import Jinja2Report
from trytond.pool import Pool

class MyReport(Jinja2Report):
    __name__ = 'my_module.my_report'

def register():
    Pool.register(MyReport, module='your_module', type_='report')
```

2. The html template of your report

```html
<html>
    <body>
        {% for record in records %}
            {{ record.name }}
        {% endfor %}
        {{ data.get('some_data') }}
    </body>
</html>
```

3. The action report registered as xml:

```xml
        <record model="ir.action.report" id="my_report_action">
            <field name="name">Title of my report</field>
            <field name="report">path/to/my/report.html</field>
            <field name="report_name">my_module.my_report</field>
            <field name="model">party.party</field>
            <field name="extension">pdf</field>
            <field name="template_extension">html</field>
        </record>
```
