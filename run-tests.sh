#!/usr/env bash

export DISPLAY=":0"
xhost +local:docker

source ~/Sites/green-coding/green-metrics-tool/venv/bin/activate

for i in {1..10}; do
   sync
   sudo /usr/sbin/sysctl -w vm.drop_caches=3
   python3 ~/Sites/green-coding/green-metrics-tool/runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-calendar-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Calendar #${i}"
done

for i in {1..10}; do
   sync
   sudo /usr/sbin/sysctl -w vm.drop_caches=3
   python3 ~/Sites/green-coding/green-metrics-tool/runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-contacts-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Contacts #${i}"
done

for i in {1..10}; do
    sync
    sudo /usr/sbin/sysctl -w vm.drop_caches=3
    python3 ~/Sites/green-coding/green-metrics-tool/runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-files-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Files #${i}"
done

for i in {1..10}; do
    sync
    sudo /usr/sbin/sysctl -w vm.drop_caches=3
    python3 ~/Sites/green-coding/green-metrics-tool/runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-docs-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Docs #${i}"
done

for i in {1..10}; do
    sync
    sudo /usr/sbin/sysctl -w vm.drop_caches=3
    python3 ~/Sites/green-coding/green-metrics-tool/runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-video-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Video #${i}"
done

for i in {1..10}; do
    sync
    sudo /usr/sbin/sysctl -w vm.drop_caches=3
    python3 ~/Sites/green-coding/green-metrics-tool/runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-talk-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Talk #${i}"
done
