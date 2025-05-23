### init.sh
# Cria a rede externa se ela ainda não existir
docker network inspect astro_localstack_net >/dev/null 2>&1 || \
  docker network create astro_localstack_net

# Sobe o Astronomer
astro dev start