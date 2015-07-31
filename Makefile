PORT = 8000
VERBOSITY = 3

COUNT_ARG = $(words $(filter-out $@,$(MAKECMDGOALS)))
PRELAST_ARG = $(shell echo $(COUNT_ARG)-1 | bc)
PREPRELAST_ARG = $(shell echo $(PRELAST_ARG)-1 | bc)

BLUE = \033[1;34m
CYAN = \033[1;36m
GREEN = \033[32m
GREENSUCCESS = \033[1;32m
ORANGE = \033[1;31m
RED = \033[31m
WHITE = \033[00m
YELLOW = \033[33m

.PHONY: clean doc fclean install_dev install_prod launch reinstall resettrans static test transall uninstall_dev uninstall_prod validate

.SILENT:

.DEFAULT:
	printf "I don't know '$<' \n\n"
	make help

$(NAME): help

help:
	printf 'List of available commands \n'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'clean' 'delete compiled and temporary files'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'db' 'synchronise database'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'doc' 'generate doc'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'fclean' 'uninstall all installed python package requirements_dev.txt rm *.mo and compileded files'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'install_dev' 'install all package list in ressources/requirements/requirements_dev.txt'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'install_prod' 'install all package list in ressources/requirements/requirements_prod.txt'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'launch' 'launch application after sync database, collectstatics, launch test and translate application'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'module' 'create architecture of modules'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'resettrans' 'delete all traductions files'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'static' 'collect statics'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'test' 'launch unit test'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'transall' 'translate applications'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'uninstall_dev' 'uninstall all package list in ressources/requirements/requirements_prod.txt'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'uninstall_prod' 'install all package list in ressources/requirements/requirements_prod.txt'
	printf '$(BLUE)%s$(WHITE)\t\t%s\n' 'validate' 'valid applications models'

module:
	$(foreach mod, $(filter-out $@, $(MAKECMDGOALS)), printf '$(BLUE)création du module $(CYAN)$(filter-out $@,$(MAKECMDGOALS))$(WHITE)\n' && python manage.py startapp $(mod) && touch $(mod)/urls.py && echo "# -*-coding:utf-8 -*-\nfrom django.conf.urls import patterns\nfrom django.conf.urls import url" >> $(mod)/urls.py)

db: validate
	printf '$(BLUE)recuperation des changements$(WHITE)\n'
	python manage.py makemigrations
	printf '$(BLUE)migration de la base de données$(WHITE)\n'
	python manage.py migrate

validate:
	printf '$(BLUE)validation de la base de données$(WHITE)\n' 
	python manage.py validate

static:
	printf '$(BLUE)suppression des anciens fichiers statics$(WHITE)\n' 
	rm -rf statics
	printf '$(BLUE)collect des nouveax fichiers statics$(WHITE)\n' 
	python manage.py collectstatic --noinput

transall:
	printf '$(BLUE)récupération des fichers de traduction$(WHITE)\n' 
	$(foreach lang, $(shell ls locale), python manage.py makemessages --verbosity=$(VERBOSITY) -l $(lang);)	
	printf '$(BLUE)compilation des fichiers de traduction$(WHITE)\n' 
	python manage.py compilemessages

resettrans:
	printf '$(BLUE)suppression des fichiers .po$(WHITE)\n'
	find . -name '*.po' -exec rm -rf {} \; 
	printf '$(BLUE)suppression des fichiers .mo$(WHITE)\n'
	find . -name '*.mo' -exec rm -rf {} \; 
	make transall

test:
	printf '$(BLUE)suppression des fichiers .mo$(WHITE)\n'
	find . -name '*.mo' -exec rm -rf {} \;
	printf '$(BLUE)lancement des tests unitaires$(WHITE)\n'
	python manage.py test --verbosity $(VERBOSITY)
	make transall

install_dev:
	printf '$(BLUE)installation du fichier ressources/requirements/requirements_dev.txt$(WHITE)\n'
	pip install -r ressources/requirements/requirements_dev.txt

install_prod:
	printf '$(BLUE)installation du fichier ressources/requirements/requirements_prod.txt$(WHITE)\n'
	pip install -r ressources/requirements/requirements_prod.txt

uninstall_dev:
	printf '$(BLUE)desinstallation du fichier ressources/requirements/requirements_dev.txt$(WHITE)\n'
	pip uninstall --yes -r ressources/requirements/requirements_dev.txt
	
uninstall_prod:
	printf '$(BLUE)desinstallation du fichier ressources/requirements/requirements_prod.txt$(WHITE)\n'
	pip uninstall --yes -r ressources/requirements/requirements_prod.txt

clean:
	printf '$(BLUE)suppression des fichiers .pyc$(WHITE)\n'
	find .. -name '*.pyc' -exec rm -rf {} \; 

fclean:
	printf '$(BLUE)suppression de tous les paquets python installé$(WHITE)\n'
	pip freeze > plop
	pip uninstall -r plop
	rm plop
	printf '$(BLUE)suppression des fichiers .mo$(WHITE)\n'
	find . -name '*.mo' -exec rm -rf {} \;
	make clean

launch: clean install static migrate validate test transall
	printf '$(BLUE)lancement du serveur$(WHITE)\n' 
	python manage.py runserver --verbosity=$(VERBOSITY) 0.0.0.0:$(PORT)
	make clean

doc: clean migrate validate static test transall
	printf '$(BLUE)génération de la documentation$(WHITE)\n'
	python -c "from ressources.gen_doc import gen_doc ; gen_doc()"
