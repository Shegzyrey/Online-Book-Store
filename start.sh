#!/usr/bin/env bash

docker-compose down

containers=$(docker ps -a --filter "name=rabbitmq_dashboard" --filter "name=api_db" --filter "name=order_db" --filter "name=inventory_db" --filter "name=api_service" --filter "name=order_service" --filter "name=inventory_service" --filter "name=websocket" --filter "name=client_websocket" -q)


if [ ! -z "$containers" ]; then
    docker stop $containers
    docker rm $containers
fi

images=$(docker images --filter=reference='gateway' --filter=reference='order_processor' --filter=reference='inventory_processor' --filter=reference='websocket' --filter=reference='websocket_client' -q)


if [ ! -z "$images" ]; then
    docker rmi $images
fi

volumes=$(docker volume ls --filter "name=rabbitmq_dashboard" --filter "name=api_db" --filter "name=order_db" --filter "name=inventory_db" --filter "name=api_service" --filter "name=order_service" --filter "name=inventory_service" --filter "name=websocket" --filter "name=client_websocket" -q)

if [ ! -z "$volumes" ]; then
    docker volume rm $volumes
fi

echo "Docker cleanup completed."

docker-compose up --build