include .env

export $(shell sed 's/=.*//' .env)

all: help

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make init                              - Init Terraform config"
	@echo "   2. make prod                             	- Run terraform apply with workspace prod"
	@echo "   2. make dev                             	- Run terraform apply with workspace dev"
	@echo "   3. make destroy                           - Destroy terraform destroy"
	@echo "   4. make invoke                            - Invoke Lambda"

.PHONY: init
init:
	python make.py init

.PHONY: prod
prod:
	python make.py prod

.PHONY: dev
dev:
	python make.py dev

.PHONY: destroy
destroy:
	python make.py destroy

.PHONY: invoke
invoke:
	python make.py invoke
