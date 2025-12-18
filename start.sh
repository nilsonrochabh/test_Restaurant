#!/bin/bash
# start.sh

echo "=== Iniciando Django com Docker ==="

# Para containers existentes
docker-compose down

# Remove volume antigo se persistir erro
read -p "Remover volume do banco? (s/n): " remove
if [[ $remove == "s" || $remove == "S" ]]; then
    docker-compose down -v
    echo "Volume removido!"
fi

# Reconstrói
echo "Construindo containers..."
docker-compose build --no-cache

# Inicia
echo "Iniciando serviços..."
docker-compose up -d

# Aguarda banco ficar pronto
echo "Aguardando PostgreSQL..."
sleep 15

# Executa migrações
echo "Executando migrações..."
docker-compose exec web python manage.py migrate

# Cria superusuário se não existir
echo "Deseja criar superusuário? (s/n): "
read criar
if [[ $criar == "s" || $criar == "S" ]]; then
    docker-compose exec web python manage.py createsuperuser
fi

echo "=== Aplicação rodando em http://localhost:8000 ==="
echo "Logs: docker-compose logs -f web"