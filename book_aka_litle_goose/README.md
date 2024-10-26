# book

# Setup Steps
## OS
Using Ubuntu (server?) 64bit 22.04  
Recommend enabling ssh and using desktop for setup...  
  
## Apps
apt install git tmux cowsay newsboat  
//curl -fsSL https://get.docker.com -o get-docker.sh  
//sudo bash get-docker.sh  
sudo apt-get install ca-certificates curl gnupg lsb-release  
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null  
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg  
sudo apt update  
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin  
sudo usermod -aG docker $(whoami)  
reboot or log out and back in to get group changes  
  
## Elastic
Reference: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html  
Reference: https://hub.docker.com/r/arm64v8/elasticsearch/  
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.1.3  
docker pull arm64v8/elasticsearch:8.1.3 # might be ablet to omit the arch tag.  
docker network create elastic  
docker run -d --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:8.1.3  
docker exec -it elasticsearch /bin/bash  
vi cfg/elasticsearch.yml # desable xpac security  
xpack.security.enabled: false  
exit  
docker restart elasticsearch  

