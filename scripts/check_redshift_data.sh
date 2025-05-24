#!/bin/bash

docker exec -i fake-redshift psql -U myuser -d mydatabase <<EOF
-- Lista as tabelas disponíveis
\\dt

-- Conta registros na tabela
SELECT COUNT(*) FROM engagement_data;

-- Visualiza os primeiros 5 registros
SELECT * FROM engagement_data LIMIT 5;

EOF