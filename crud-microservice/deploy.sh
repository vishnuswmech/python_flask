#!/bin/bash
set -o allexport
source deploy.env
docker rm -f $(docker ps -aq)
docker network rm ${custom_network_name}
docker network create ${custom_network_name} --driver bridge

#frontend
docker run -dit --name ${frontend_con_name} -p ${frontend_port}:${frontend_port} -e frontend_port=${frontend_port} -e backend_con_name=${backend_con_name} -e custom_network_name=${custom_network_name} -e read_port=${read_port}  -e backend_port=${backend_port} -e read_con_name=${read_con_name} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/frontend:/root/flask ${frontend_image}
#backend
docker run -dit --name ${backend_con_name} -p ${backend_port}:${backend_port} -e backend_port=${backend_port} -e frontend_con_name=${frontend_con_name} -e custom_network_name=${custom_network_name} -e frontend_port=${frontend_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/backend:/root/flask ${backend_image}

#read
docker run -dit --name ${read_con_name} -p ${read_port}:${read_port} -e read_port=${read_port} --net ${custom_network_name} -e redis_host=${redis_con_name}.${custom_network_name} -e custom_network_name=${custom_network_name} -e frontend_con_name=${frontend_con_name} -e frontend_port=${frontend_port} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/read:/root/flask ${read_image}

#redis
docker run -dit --name ${redis_con_name} --net ${custom_network_name}  -e redis_host=${redis_con_name}.${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/redis:/data -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/redis:/usr/local/etc/redis  ${redis_image} redis-server
#update
docker run -dit --name ${update_con_name} -p ${update_port}:${update_port} -e update_port=${update_port} -e frontend_con_name=${frontend_con_name} -e custom_network_name=${custom_network_name} -e frontend_port=${frontend_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/update:/root/flask ${update_image}

#FQDN
export frontend_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${frontend_con_name})
export backend_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${backend_con_name})
export read_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${read_con_name})
export redis_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${redis_con_name})
export update_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${update_con_name})

sudo -E -- sh -c "frontend_ip=${frontend_ip} frontend_con_name=${frontend_con_name} custom_network_name=${custom_network_name} \
echo \"\${frontend_ip} \${frontend_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c "backend_ip=${backend_ip} backend_con_name=${backend_con_name} custom_network_name=${custom_network_name} \
echo \"\${backend_ip} \${backend_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c "read_ip=${read_ip} read_con_name=${read_con_name} custom_network_name=${custom_network_name} \
echo \"\${read_ip} \${read_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c "redis_ip=${redis_ip} redis_con_name=${redis_con_name} custom_network_name=${custom_network_name} \
echo \"\${redis_ip} \${redis_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c "update_ip=${update_ip} redis_con_name=${update_con_name} custom_network_name=${custom_network_name} \
echo \"\${update_ip} \${update_con_name}.\${custom_network_name}\" >> /etc/hosts"


