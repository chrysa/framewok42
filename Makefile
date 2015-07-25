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

.SILENT:

.DEFAULT:
	printf ''

module: 
	printf '$(BLUE)ajout du/des module(s) $(CYAN)$(filter-out $@,$(MAKECMDGOALS))$(WHITE)\n' 
	$(foreach mod, $(filter-out $@, $(MAKECMDGOALS)), python manage.py startapp $(mod))

migrate: validate
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
	make trans

install:
	printf '$(BLUE)installation du fichier requirements.txt$(WHITE)\n'
	pip install -r requirements.txt
	
uninstall:
	printf '$(BLUE)desinstallation du fichier requirements.txt$(WHITE)\n'
	pip uninstall --yes -r requirements.txt

reinstall: uninstall install clean

clean:
	printf '$(BLUE)suppression des fichiers .pyc$(WHITE)\n'
	find .. -name '*.pyc' -exec rm -rf {} \; 
	printf '$(BLUE)suppression des fichiers ~$(WHITE)\n'
	find .. -name '*~' -exec rm -rf {} \; 

fclean:
	printf '$(BLUE)suppression de tous les paquets python installé$(WHITE)\n'
	pip freeze > plop
	pip uninstall -r plop
	rm plop
	make clean

launch: clean install static migrate validate test transall
	printf '$(BLUE)lancement du serveur$(WHITE)\n' 
	python manage.py runserver --verbosity=$(VERBOSITY) 0.0.0.0:$(PORT)
	make clean

doc: clean migrate validate static test transall
	printf '$(BLUE)génération de la documentation$(WHITE)\n'
	python -c "from ressources.gen_doc import gen_doc ; gen_doc()"