import os
from subprocess import call
project = os.listdir('.')

if not os.path.isdir('doc'):
    call('mkdir doc', shell=True)
    call('sphinx-quickstart', shell=True)
    f = open("doc/source/conf.py","r+")
    chaine = f.read()
    chaine.join("import django\n\nsys.path.insert(0, os.path.abspath('../..'))\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framework.settings')\ndjango.setup()")
    result = chaine.replace("html_theme = 'alabaster'", "html_theme = 'classic'").replace("#html_title = None", "html_title = None")
    f.write(result)
    f.close()

call('sphinx-apidoc -f -o doc/source/ .', shell=True)
for app in project:
    if os.path.isfile('{}/__init__.py'.format(app)) and app[0] != ('.' or '_'):
        call('sphinx-apidoc -f -o doc/source/ {}/'.format(app), shell=True)

call('cd doc && make dirhtml', shell=True)
call('cd doc && make latex', shell=True)
