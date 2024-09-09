#!/bin/bash
set -o allexport
source deploy.env
docker rm -f $(docker ps -aq)
docker network rm ${custom_network_name}
docker network create ${custom_network_name} --driver bridge


#home
docker run -dit --name ${home_con_name} -h ${home_con_name} -p ${home_port}:${home_port} -e home_port=${home_port} -e create_con_name=${create_con_name} -e custom_network_name=${custom_network_name} -e read_port=${read_port}  -e create_port=${create_port} -e read_con_name=${read_con_name} -e update_con_name=${update_con_name} -e update_port=${update_port} -e delete_con_name=${delete_con_name} -e delete_port=${delete_port} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/home:/root/flask ${home_image} /bin/bash

#frontend
#docker run -dit --name ${frontend_con_name} -h ${frontend_con_name} -p ${frontend_port}:${frontend_port} -e frontend_port=${frontend_port} -e create_con_name=${create_con_name} -e custom_network_name=${custom_network_name} -e read_port=${read_port}  -e create_port=${create_port} -e read_con_name=${read_con_name} -e update_con_name=${update_con_name} -e update_port=${update_port} -e delete_con_name=${delete_con_name} -e delete_port=${delete_port} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/frontend:/root/flask ${frontend_image} /bin/bash
#create
docker run -dit --name ${create_con_name} -h ${create_con_name} -p ${create_port}:${create_port} -e create_port=${create_port} -e home_con_name=${home_con_name} -e custom_network_name=${custom_network_name} -e home_port=${home_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e update_con_name=${update_con_name} -e update_port=${update_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/create:/root/flask ${create_image} /bin/bash

#read
docker run -dit --name ${read_con_name} -h ${read_con_name} -p ${read_port}:${read_port} -e read_port=${read_port} --net ${custom_network_name} -e redis_host=${redis_con_name}.${custom_network_name} -e custom_network_name=${custom_network_name} -e read_con_name=${read_con_name} -e read_port=${read_port} -e home_con_name=${home_con_name} -e home_port=${home_port} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/read:/root/flask ${read_image} /bin/bash

#redis
docker run -dit --name ${redis_con_name} --net ${custom_network_name} -h ${redis_con_name} -e redis_host=${redis_con_name}.${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/redis:/data -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/redis:/usr/local/etc/redis  ${redis_image} redis-server
#update
docker run -dit --name ${update_con_name} -p ${update_port}:${update_port} -h ${update_con_name} -e update_con_name=${update_con_name} -e update_port=${update_port} -e home_con_name=${home_con_name} -e custom_network_name=${custom_network_name} -e home_port=${home_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/update:/root/flask ${update_image} /bin/bash

#delete
docker run -dit --name ${delete_con_name} -h ${delete_con_name} -p ${delete_port}:${delete_port} -e delete_con_name=${delete_con_name} -e delete_port=${delete_port} -e home_con_name=${home_con_name} -e custom_network_name=${custom_network_name} -e home_port=${home_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v /home/vishnu/workspace/new-flask/python_flask/crud-microservice/delete:/root/flask ${delete_image} /bin/bash


#FQDN
export home_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${home_con_name})
#export frontend_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${frontend_con_name})
export create_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${create_con_name})
export read_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${read_con_name})
export redis_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${redis_con_name})
export update_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${update_con_name})
export delete_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${delete_con_name})


sudo -E -- sh -c " \
echo \"\${home_ip} \${home_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c "\
echo \"\${create_ip} \${create_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c " \
echo \"\${read_ip} \${read_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c " \
echo \"\${redis_ip} \${redis_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c " \
echo \"\${update_ip} \${update_con_name}.\${custom_network_name}\" >> /etc/hosts"
sudo -E -- sh -c " \
echo \"\${delete_ip} \${delete_con_name}.\${custom_network_name}\" >> /etc/hosts"


