all: help

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make init                              - Init Terraform config"
	@echo "   2. make apply                             - Run terraform apply"
	@echo "   3. make destroy                           - Destroy terraform destroy"
	@echo "   4. make invoke                            - Invoke Lambda"
	@echo "   5. make zip                               - Zip lambda function"

.PHONY: init
init:
	terraform init terraform/aws

.PHONY: apply
apply:
	terraform apply -var-file=terraform/aws/security.tfvars terraform/aws

.PHONY: destroy
destroy:
	terraform destroy -var-file=terraform/aws/security.tfvars terraform/aws

.PHONY: invoke
invoke:
	aws lambda invoke --function-name log_watcher --profile acorsi --log-type Tail --payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' response.json | jq .LogResult | sed 's/"//g' | base64 --decode

.PHONY: zip
zip:
	zip -j lambda/main.zip lambda/main.py
