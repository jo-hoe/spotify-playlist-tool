include help.mk

ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

.DEFAULT_GOAL := start-playlist-import 

.PHONY: init 
init: venv update ## inital setup of project

.PHONY: venv
venv:
	python -m venv ${ROOT_DIR}.venv

.PHONY: update
update: ## install all dependencies in virtual env
	git pull
	${ROOT_DIR}.venv/Scripts/pip install -r requirements.txt

.PHONY: save-dependencies
save-dependencies: ## save current dependencies
	"${ROOT_DIR}.venv/Scripts/pip" list --not-required --format=freeze | grep -v "pip" > ${ROOT_DIR}requirements.txt
	
.PHONY: start-playlist-import 
start-playlist-import: ## start import playlist with default settings
	${ROOT_DIR}.venv/Scripts/python ${ROOT_DIR}main.py import_playlist

.PHONY: get-all-commands
get-all-commands: ## get all commands
	@${ROOT_DIR}.venv/Scripts/python ${ROOT_DIR}main.py -h