all: help

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make init                              - Init Terraform config"
	@echo "   2. make apply                             - Run terraform apply"
	@echo "   3. make destroy                           - Destroy terraform destroy"
	@echo "   4. make invoke                            - Invoke Lambda"

.PHONY: init
init:
	python make.py init

.PHONY: apply
apply:
	python make.py apply

.PHONY: destroy
destroy:
	python make.py destroy

.PHONY: invoke
invoke:
	python make.py invoke
