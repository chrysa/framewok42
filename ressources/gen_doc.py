import fnmatch
import os
from subprocess import call


def locate(pattern):
    for root, dirs, files in os.walk('..'):
        for filename in fnmatch.filter(files, pattern):
            return os.path.join(root, filename)

AUTHOR = 'agreau'
VERSION = 2
RELEASE = 2
PROJECT_NAME = os.path.dirname(os.path.abspath(locate('settings.py'))).split('/')[-1]
IMPORT_DJANGO = "\nimport django"
IMPORT_DJANGO += "\n\nsys.path.insert(0, os.path.abspath('../..'))"
IMPORT_DJANGO += "\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings')".format(PROJECT_NAME)
IMPORT_DJANGO += "\ndjango.setup()"


def gen_doc():
    project = os.listdir('.')
    if not os.path.isdir('doc'):
        call('mkdir doc', shell=True)
        cmd = "sphinx-quickstart --dot='.' --suffix='.rst' --sep --language=en --master='index' --epub --project={} --author={} -v {} --release={} --ext-autodoc --ext-doctest --ext-intersphinx --ext-todo --ext-coverage --ext-pngmath --ext-mathjax --ext-ifconfig --ext-viewcode --makefile --batchfile".format(PROJECT_NAME, AUTHOR, VERSION, RELEASE)
        call(cmd, shell=True)
        conf = locate('conf.py')
        result = open(conf, 'r').read().replace("html_theme = 'alabaster'", "html_theme = 'classic'").replace("#html_title = None", "html_title = None").replace("#html_show_copyright = True", "html_show_copyright = True").replace("#html_last_updated_fmt = '%b %d, %Y'", "html_last_updated_fmt = '%b %d, %Y'").replace("#html_show_sourcelink = True", "html_show_sourcelink = True")
        open(conf, 'w').write(result)
        open(conf, 'a').write(IMPORT_DJANGO)
    call('sphinx-apidoc -f -o doc/source/ .', shell=True)
    for app in project:
        if os.path.isfile('{}/__init__.py'.format(app)) and app[0] != ('.' or '_'):
            call('sphinx-apidoc -f -o doc/source/ {}/'.format(app), shell=True)
    call('cd doc && make html', shell=True)

if __name__ == '__main__':
    gen_doc()
