#!/bin/bash

# 1. Cria e ativa o ambiente virtual com Python 3.12
uv sync

# 2. Ativa o ambiente virtual
source .venv/Scripts/activate

# 3. Instala awscli-local
uv add awscli-local

# 5. Torna o script de rede executável e o executa
chmod +x scripts/setup_network.sh
bash scripts/setup_network.sh

# 6. Sobe o Airflow com Astronomer
astro dev start
