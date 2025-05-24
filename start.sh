#!/bin/bash

# 1. Cria e ativa o ambiente virtual com Python 3.12
uv venv --python 3.12
uv init

# 2. Ativa o ambiente virtual
source .venv/Scripts/activate

# 3. Instala awscli-local
uv add awscli-local

# 4. Inicializa o projeto Astronomer automaticamente
astro dev init --yes

# 5. Torna o script de rede executável e o executa
chmod +x setup_network.sh
bash setup_network.sh

# 6. Torna o script de validação de ingestão de dados executável
chmod +x check_redshift_data.sh

# 6. Sobe o Airflow com Astronomer
astro dev start

