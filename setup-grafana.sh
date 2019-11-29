wget https://dl.grafana.com/oss/release/grafana_6.2.2_armhf.deb 
sudo dpkg -i grafana_6.2.2_armhf.deb
sudo apt-get update
sudo apt-get install grafana
sudo service grafana-server start
sudo update-rc.d grafana-server defaults

