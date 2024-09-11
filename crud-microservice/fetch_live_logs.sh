for container in $(docker ps --format "{{.Names}}"); do
  gnome-terminal --tab --title="$container" -- bash -c "echo 'Following logs for container: $container'; docker logs -f $container; exec bash"
done
