#!/bin/bash
set -o allexport
source deploy.env
docker rm -f $(docker ps -aq)

random_sha_full=$(date +%s%N | sha256sum | awk '{print $1'})
random_sha=${random_sha_full:0:5}

custom_network_name=${custom_network_name}-${random_sha}
export network_status=false
echo "Creating docker network ${custom_network_name}"
docker network create ${custom_network_name} --driver bridge
network_items_raw=$(docker network ls | awk '{print $2}')
network_items=$(echo $network_items_raw | sed "s/ /,/g")
for item in ${network_items}
 do
 echo $item
 if [[ "$item" == *"$custom_network_name"* ]]
 then
export network_status=true

  else
  export network_status=false
 fi
 done
if [ $network_status = true ]
then
 echo "$custom_network_name network created successfully, We are good to proceed"
else
echo "$custom_network_name network creation failed,exiting now"
exit 1

fi
echo ""
 echo "Proceeding with Container creation"
echo ""


echo "Proceeding with Home container creation"
#home
docker run -dit --name ${home_con_name} -h ${home_con_name} -p ${home_port}:${home_port} -e home_port=${home_port} -e create_con_name=${create_con_name} -e custom_network_name=${custom_network_name} -e read_port=${read_port}  -e create_port=${create_port} -e read_con_name=${read_con_name} -e update_con_name=${update_con_name} -e update_port=${update_port} -e delete_con_name=${delete_con_name} -e delete_port=${delete_port} --net ${custom_network_name} -v ${host_volume_mount_path}/home:/root/flask ${home_image}
echo ""

echo "Proceeding with Create container creation"

#create
docker run -dit --name ${create_con_name} -h ${create_con_name} -p ${create_port}:${create_port} -e create_port=${create_port} -e home_con_name=${home_con_name} -e custom_network_name=${custom_network_name} -e home_port=${home_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e update_con_name=${update_con_name} -e update_port=${update_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v ${host_volume_mount_path}/create:/root/flask ${create_image}
echo ""

echo "Proceeding with Read container creation"

#read
docker run -dit --name ${read_con_name} -h ${read_con_name} -p ${read_port}:${read_port} -e read_port=${read_port} --net ${custom_network_name} -e redis_host=${redis_con_name}.${custom_network_name} -e custom_network_name=${custom_network_name} -e read_con_name=${read_con_name} -e read_port=${read_port} -e create_con_name=${create_con_name} -e create_port=${create_port} -e home_con_name=${home_con_name} -e home_port=${home_port} -v ${host_volume_mount_path}/read:/root/flask ${read_image}
echo ""

echo "Proceeding with Redis container creation"

#redis
docker run -dit --name ${redis_con_name} --net ${custom_network_name} -h ${redis_con_name} -e redis_host=${redis_con_name}.${custom_network_name} -v ${host_volume_mount_path}/redis:/data -v ${host_volume_mount_path}/redis:/usr/local/etc/redis  ${redis_image} redis-server
echo ""

echo "Proceeding with Update container creation"

#update
docker run -dit --name ${update_con_name} -p ${update_port}:${update_port} -h ${update_con_name} -e update_con_name=${update_con_name} -e update_port=${update_port} -e home_con_name=${home_con_name} -e custom_network_name=${custom_network_name} -e home_port=${home_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e create_con_name=${create_con_name} -e create_port=${create_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v ${host_volume_mount_path}/update:/root/flask ${update_image}
echo ""

echo "Proceeding with Delete container creation"

#delete
docker run -dit --name ${delete_con_name} -h ${delete_con_name} -p ${delete_port}:${delete_port} -e delete_con_name=${delete_con_name} -e delete_port=${delete_port} -e home_con_name=${home_con_name} -e custom_network_name=${custom_network_name} -e home_port=${home_port} -e read_con_name=${read_con_name} -e read_port=${read_port} -e redis_host=${redis_con_name}.${custom_network_name} --net ${custom_network_name} -v ${host_volume_mount_path}/delete:/root/flask ${delete_image}
echo ""

echo "Checking container status"
for con in ${home_con_name} ${create_con_name} ${redis_con_name} ${update_con_name} ${delete_con_name}
do
if [ $(docker ps | grep $con | wc -l) -eq "0" ]; then echo "$con not running,kindly check"; else echo " $con running fine,proceeding with FQDN update";
fi
done
echo ""

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

echo "The FQDN entry successful"
echo "You can access the UI using this URL http://${home_con_name}.${custom_network_name}:${home_port}"


