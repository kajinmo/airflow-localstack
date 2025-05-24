# Airflow + LocalStack Setup

Este repositório configura um ambiente de desenvolvimento local com [Apache Airflow](https://airflow.apache.org/) e [LocalStack](https://localstack.cloud/), utilizando a CLI da Astronomer. Ideal para testes com DAGs que interagem com serviços AWS como S3, SQS, SNS e um banco PostgreSQL simulando o Redshift.

---

## Estrutura

```
.
├── dags/                           # Suas DAGs ficam aqui
├── include/                        # Dados e scripts auxiliares para o container
│ └── data/
├── scripts/                        # Pasta de scripts para rodar na máquina local
│ └── start.sh                       # Script para subir o Astronomer + rede Docker
│ └── setup_network.sh              # Script para conectar o LocalStack à rede
│ └── check_redshift_data.sh        # Consulta SQL para verificar se o              
├── docker-compose.override.yml     # Serviços adicionais: LocalStack + PostgreSQL
├── Dockerfile                      # Define a versão Astronomer e Airflow
├── requirements.txt                # Dependências das DAGs (boto3, airflow-provider-amazon, pandas, etc)
└── README.md
```

<br>

# Setup passo a passo (Windows 11 + Bash)

### Requisitos
- Docker Desktop
- uv
- Astronomer CLI
- AWS CLI
- Local Stack
- Git Bash

---
<br>

### ⚠️ ATENÇÃO: Você vai trabalhar em DUAS janelas do Bash separadas

1- Primeira janela (LocalStack)

1- Segunda janela (Airflow)

---

<br>

### 1. Criar o ambiente Local Stack
Para inicializar um container com o LocalStack, em um terminal bash:
```bash
localstack start
```

---
<br>

### 2. Criar o ambiente Airflow
Em OUTRO terminal bash:

```bash
git clone https://github.com/kajinmo/airflow-localstack
cd airflow-localstack
code .
chmod +x init.sh
bash start.sh
```

<br>

O Astronomer vai abrir uma janela do Airflow no http://localhost:8080/. No menu superior da interface do Airflow, vá em:

`Admin > Connections > (+) Add a new record`

<br>
Inserir as conexões para o s3:

```yaml
Connection Id: localstack_s3
Connection Type: Amazon Web Services
Extra:
{
  "endpoint_url": "http://localstack-main:4566",
  "region_name": "us-east-1",
  "aws_access_key_id": "test",
  "aws_secret_access_key": "test"
}
```

Inserir as conexões para o ec2:
```yaml
Connection Id: localstack_ec2
Connection Type: Amazon Web Services
Extra:
{
  "endpoint_url": "http://localstack-main:4566",
  "region_name": "us-east-1",
  "aws_access_key_id": "test",
  "aws_secret_access_key": "test"
}
```

Inserir as conexões para o fake_redshift:
```yaml
Connection Id: fake_redshift
Connection Type: Postgres
Host: fake-redshift
Database: mydatabase
Login: myuser
Password: mypassword
Port: 5432
```

Depois de configurar as conexões, reinicie o ambiente para que o Airflow reconheça as novas credenciais. No bash do Airflow:

```bash
astro dev restart
```

<br>

Agora o Airflow está pronto para rodar e testar as conexões com o AWS/LocalStack.

Na pasta /dasg tem duas dags:
- s3_ec2_redshift_connection.py: testar conexão com S3 e EC2 e Redshift
- csv_to_redshift.py: ingestão de dados a partir de um arquivo csv localizado na pasta `include/data/`