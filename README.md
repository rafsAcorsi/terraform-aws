# Pré-requisitos

- [Terraform](https://www.terraform.io/downloads.html)
---
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)

Passos pós instalaçāo do AWS CLI, obs: somente executar em caso de primeira instalaçāo

####Iniciar o AWS CLI

- `aws configure` e  inserir o AWS Access Key ID e AWS Secret Access Key

Feito isso será criado um diretorio no root de credentials`~/.aws/credentials`


---

- [Criar usuário ADM no IAM (marcar a opçāo "Programmatic access")](https://console.aws.amazon.com/iam/home#/users$new?step=details)
- Setar permissoes abaixo:

Policy Name| 
| -------------             |
|AdministratorAccess        |
---


Copiar e renomear o arquivo [security-sample.tfvars](terraform/aws/security-sample.tfvars) para security.tfvars e editar as variaveis
