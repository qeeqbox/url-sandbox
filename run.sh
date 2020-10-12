echo -e "\nQeeqBox URL-Sandbox v$(jq -r '.version' info) starter script -> https://github.com/qeeqbox/url-sandbox"
echo -e "Free URL Sandbox \n"\

setup_requirements () {
	sudo apt update -y
	sudo apt install -y linux-headers-$(uname -r) docker.io jq xdg-utils curl
	sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
	which docker-compose && echo "Good"
	which docker && echo "Good"
}

wait_on_web_interface () {
echo ''
until $(curl --silent --head --fail http://127.0.0.1:8000 --output /dev/null); do
echo -ne "\n\n[\033[47m\033[0;31mInitializing project in progress..\033[0m]\n\n"
sleep 5
done
echo ''
xdg-open http://127.0.0.1:8000/url/
}

test_project () {
	sudo docker-compose -f docker-compose-test.yml up --build
}

dev_project () {
	sudo docker-compose -f docker-compose-dev.yml up --build
}

stop_containers () {
	sudo docker stop $(sudo docker ps -aq)
} 

deploy_aws_project () {
	echo "Will be added later on"
}

auto_configure_test () {
	setup_requirements
	test_project
}

auto_configure () {
	setup_requirements
	dev_project
}

if [[ "$1" == "auto_test" ]]; then
	stop_containers
	wait_on_web_interface & 
	auto_configure_test
	stop_containers 
fi

if [[ "$1" == "auto_configure" ]]; then
	stop_containers
	wait_on_web_interface & 
	auto_configure
	stop_containers 
fi