import os
from subprocess import call


def gen_doc():
    project = os.listdir('.')

    if not os.path.isdir('doc'):
        call('mkdir doc', shell=True)
        call('sphinx-quickstart', shell=True)
        file = "doc/source/conf.py"
        result = open(file, 'r').read().replace("html_theme = 'alabaster'", "html_theme = 'classic'").replace(
            "#html_title = None", "html_title = None").replace("#html_show_copyright = True",
                                                               "html_show_copyright = True").replace(
            "#html_last_updated_fmt = '%b %d, %Y'", "html_last_updated_fmt = '%b %d, %Y'").replace(
            "#html_show_sourcelink = True", "html_show_sourcelink = True")
        open(file, 'w').write(result)
        open(file, 'a').write(
            "\nimport django\n\nsys.path.insert(0, os.path.abspath('../..'))\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framework.settings')\ndjango.setup()")

    call('sphinx-apidoc -f -o doc/source/ .', shell=True)
    for app in project:
        if os.path.isfile('{}/__init__.py'.format(app)) and app[0] != ('.' or '_'):
            call('sphinx-apidoc -f -o doc/source/ {}/'.format(app), shell=True)

    call('cd doc && make html', shell=True)
    call('cd doc && make latex', shell=True)
