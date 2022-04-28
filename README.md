# book

# Setup Steps
## OS
Using 64 bit Raspberry Pi OS Lite
Recommend enabling ssh and using desktop for setup...
## Apps
apt install git tmux cowsay newsboat
curl -fsSL https://get.docker.com -o get-docker.sh
sudo bash get-docker.sh
sudo usermod -aG docker $(whoami)
reboot
## Elastic
Reference: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.1.3
docker network create elastic
