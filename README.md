# Pré-requisitos

- [Docker para rodar localmente](https://docs.docker.com/get-docker/)
- [Terraform](https://www.terraform.io/downloads.html)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)
- [Criar usuário ADM no IAM (marcar a opçāo "Programmatic access")](https://console.aws.amazon.com/iam/home#/users$new?step=details)
- Setar permissoes abaixo:

Policy Name| 
| -------------             |
|AdministratorAccess        |

Passos pós instalaçāo CLI, somente executar em caso de primeira instalaçāo

Iniciar o AWS CLI

- `aws configure` e  inserir o AWS Access Key ID e AWS Secret Access Key

Feito isso será criado um diretorio no root de credentials`~/.aws/credentials`

[Altere esse arquivo e coloque o nome do seu profile criado, linha:2](main.tf)