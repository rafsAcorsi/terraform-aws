# Pré-requisitos
Todo o script foi feito usando um macOS

- [Python3.7>~](https://www.python.org/downloads/)
- [Terraform](https://www.terraform.io/downloads.html)
- [Conta na AWS](https://console.aws.amazon.com/)
---
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)

Passos pós instalaçāo do AWS CLI, obs: somente executar em caso de primeira instalaçāo

#### Iniciar o AWS CLI

- `aws configure` e  inserir o AWS Access Key ID e AWS Secret Access Key

Feito isso será criado um diretório no root de credentials`~/.aws/credentials`


---

- [Criar usuário ADM no IAM (marcar a opçāo "Programmatic access")](https://console.aws.amazon.com/iam/home#/users$new?step=details)
- Setar permissões abaixo:

Policy Name|
| -------------             |
|AdministratorAccess        |
---

## Variáveis de ambiente

Exportar variáveis abaixo

|                    |                          |
|--------------------|--------------------------|
|aws_profile         | <nome_do_seu_profile>    |
|db_name             | <database_name>          |
|db_user_name        | <db_username>            |
|db_user_password    | <db_user_password>       |
|bucket_name         | <bucket_name>            |

---

## Scripts Makefile
No diretório root da aplicação digite `make` e veja todos scripts possíveis

