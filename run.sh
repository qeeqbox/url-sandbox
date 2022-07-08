#!/bin/bash 

echo -e "\nQeeqBox URL-Sandbox v$(jq -r '.version' info) starter script -> https://github.com/qeeqbox/url-sandbox"
echo -e "Open-Source URL Sandbox\n"

if [[ $EUID -ne 0 ]]; then
   echo -e "\nYou have to run this script with higher privileges\n" 
   exit 1
fi

setup_requirements () {
	apt update -y
	if ! command -v docker &> /dev/null
	then
			echo "Installing Docker"
			apt install -y linux-headers-$(uname -r) docker.io
	fi
	if ! command -v jq &> /dev/null
	then
			echo "Installing jq"
			apt install -y jq
	fi
	if ! command -v xdg-open &> /dev/null
	then
			echo "Installing xdg-utils"
			apt install -y xdg-open
	fi
	if ! command -v docker-compose &> /dev/null
	then
			echo "Installing docker-compose"
			curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
			chmod +x /usr/local/bin/docker-compose
	fi
}

wait_on_web_interface () {
until $(curl --silent --head --fail http://127.0.0.1:8000 --output /dev/null); do
sleep 5
done
xdg-open http://127.0.0.1:8000/url/
}

test_project () {
	docker-compose -f docker-compose-test.yml up --build
}

dev_project () {
	docker-compose -f docker-compose-dev.yml up --build
}

stop_containers () {
	docker-compose -f docker-compose-test.yml down -v 2>/dev/null
	docker-compose -f docker-compose-dev.yml down -v 2>/dev/null
	docker stop $(docker ps | grep url-sandbox_ | awk '{print $1}') 2>/dev/null
	docker kill $(docker ps | grep url-sandbox_ | awk '{print $1}') 2>/dev/null
} 

deploy_aws_project () {
	echo "Will be added later on"
}

auto_configure_test () {
	stop_containers
	wait_on_web_interface & 
	setup_requirements
	test_project
	stop_containers 
	kill %% 2>/dev/null
}

auto_configure () {
	stop_containers
	wait_on_web_interface & 
	setup_requirements
	dev_project
	stop_containers 
	kill %% 2>/dev/null
}

if [[ "$1" == "auto_test" ]]; then
	auto_configure_test
fi

if [[ "$1" == "auto_configure" ]]; then
	auto_configure
fi

kill %% 2>/dev/null

while read -p "`echo -e '\nChoose an option:\n1) Setup requirements (docker, docker-compose)\n2) Test the project (All servers and Sniffer)\n8) Run auto configuration\n9) Run auto test\n>> '`"; do
	case $REPLY in
		"1") setup_requirements;;
		"2") test_project;;
		"8") auto_configure;;
		"9") auto_configure_test;;
		*) echo "Invalid option";;
	esac
done
