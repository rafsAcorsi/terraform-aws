all: help

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make apply                             - Run terraform apply"
	@echo "   2. make destroy                           - Destroy terraform destroy"
	@echo "   3. make invoke                            - Invoke Lambda"
	@echo "   3. make zip                            	- Zip lambda function"


.PHONY: apply
apply:
	terraform apply

.PHONY: destroy
destroy:
	terraform destroy

.PHONY: invoke
invoke:
	aws lambda invoke --function-name log_watcher --profile acorsi --log-type Tail --payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' response.json | jq .LogResult | sed 's/"//g' | base64 --decode

.PHONY: zip
zip:
	zip -j main.zip lambda/main.py
