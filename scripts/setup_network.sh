#!/bin/bash

# Cria a rede externa se não existir
NETWORK_NAME="astro_localstack_net"

if ! docker network ls | grep -q "$NETWORK_NAME"; then
  echo "Criando a rede externa '$NETWORK_NAME'..."
  docker network create "$NETWORK_NAME"
else
  echo "Rede '$NETWORK_NAME' já existe."
fi

# Conecta o LocalStack à rede, se ainda não estiver conectado
CONTAINER_NAME="localstack-main"
if ! docker network inspect "$NETWORK_NAME" | grep -q "$CONTAINER_NAME"; then
  echo "Conectando $CONTAINER_NAME à rede '$NETWORK_NAME'..."
  docker network connect "$NETWORK_NAME" "$CONTAINER_NAME"
else
  echo "$CONTAINER_NAME já está conectado à rede '$NETWORK_NAME'."
fi
