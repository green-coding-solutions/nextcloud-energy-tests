# Benchmarking Nextcloud

What is Nextcloud? A safe home for all your data. Access & share your files, calendars, contacts, mail & more from any device, on your terms.

Most of the Nextcloud is based of the code supplied in <https://github.com/nextcloud/docker> please refer to this documentation for everything Nextcloud dependent.

We evaluate the two browsers Chromium and Firefox. Also the three databases MariaDB, Postgres and SQLite.

## Install nextcloud beforehand with defaults

Please note that this scenario should be run with 3600s idle and 3600s baseline durations

```bash
python3 runner.py --uri ~/Sites/green-coding/nextcloud-energy-tests --filename usage_scenario-mariadb-install-firefox.yml --dev-no-optimizations --allow-unsafe --name "Nextcloud Blue Angel - Install"
```

This will install nextcloud with the defaull apps. Currently:
- Calendar
- Contacts
- Mail
- Document editor
- Talk (Video conference & Instant Messaging)

All changes are saved in the docker volumes for *Apache* webserver and the *MariaDB* database.

## Preparation of installed Nextcloud

Nextcloud by default has a cronjob that will trigger in parallel with web requests.

This must be deactived in the Admin Dashboard under *Basic Settings*. Setting it to cron will effectively 
deactivate it if no cron job is set to trigger the *.php* file afterwards.

## Execution of the tests for the Blue Angel certification

For a proper run login via SSH to the machine and then start the process unattended.

First prepare the system to allow firefox window to open from inside docker

```bash
export DISPLAY=:0
xhost +local:docker # might also need to be done on the machine directly. Not only via ssh
```

Also configure GMT to use 60s pre-test sleep time. Idle should be at 120 s to make container energy estimation work.
Baseline can be at 0.

Then execute the scenarios via GMT
```bash
nohup bash run-tests.sh &> output.log &
disown -h %1
logout
```

## Scenarios details

Currently there are six different usage scenarios of Nextcloud, orchestrated with different databases and browsers.
All scripts will start of with creating an admin account and installing the recommended apps,  
then each case diverges from that point.
The cases are:

- Contacts:
  + TODO
- Files:
  + TODO
- Calendar:
  + TODO
- Video:
  + TODO
- Docs:
  + Login as admin and create a second user.
  + Login as admin and create a text document and then share it with second user
  + Login as both users, open the text document and edit it, making sure the other user sees the text entered
  + Delete the document and the new user after
- Talk:
  + Login as admin and create a group chat, allowing guests to join via link
  + Open the group conversation link in 5 browsers as guests
  + Each guest sends a 20KB random text message and validates the other members have received it


## Infrastructure - Apache / MariaDB

The compose file is copy pasted from <https://github.com/nextcloud/docker#base-version---apache>
We set a bogus password for `*_ROOT_PASSWORD` and `*_PASSWORD` as the GMT requires environment variables to be set.

## Running

You will need to supply the `--allow-unsafe` to the runner as it will mount volumes.

## Debugging tips


In cases where the script hangs because of a wrong locator, it might be helpful to run the usage scenario in debug mode and then attach a shell to the Playwright container.
Running `playwright codegen -o output.py` from the container and then following the actions of the script can help investigate what exactly is different.
