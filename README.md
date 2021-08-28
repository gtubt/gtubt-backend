# INSTALLATION GUIDE
This installation guide is for Debian based Linux distributions.
## REQUIREMENTS
- Python 3.8
- PostgreSQL
- Git
### Steps
- Upgrade the operating system and install packages
  - `sudo apt update -y`
  - `sudo apt upgrade -y`
  - `python3 -V`
  - ```
    Output
    Python 3.8.10
    ```
  - `sudo apt install -y python3-pip`
  - `sudo apt install -y build-essential libssl-dev libffi-dev python3-dev postgresql postgresql-contrib git vim`
- Install a virtual environment tool
  - `pip3 install virtualenvwrapper`
- Open the `~/.bashrc` file with your favorite text editor.
  - `vim ~/.bashrc`
  - Add lines below to the `.bashrc` file
    - `export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3`
    - `export WORKON_HOME=$HOME/.virtualenvs` You can change `.virtualenvs` folder which is for virtual environments.
    - `export VIRTUALENVWRAPPER_VIRTUALENV=$HOME/.local/bin/virtualenv`
    - `source ~/.local/bin/virtualenvwrapper.sh`
- Create a virtual environment
  - `mkvirtualenv test`
- Install project based requirements
  - `workon test`
  - `pip install -r requirements.txt`
- Edit `pg_hba.conf`
  - ```
    $ find / -name "pg_hba.conf" 2>/dev/null
    /etc/postgresql/12/main/pg_hba.conf
    ```
  - Edit the file `sudo vim /etc/postgresql/12/main/pg_hba.conf` and change `peer` with `trust` as shown below. Also don't forget to add the referred line.
    - ```
      local all postgres peer  #find this line  
      local all postgres trust #change peer with trust

      #AND

      host all postgres 127.0.0.1/32 trust #add this line BEFORE the line below
      host all all 127.0.0.1/32 md5
      ```
    - `sudo systemctl restart postgresql@12-main`
- Create a database for project
  - `sudo -i -u postgres`
  - `createdb gtubt`
- Go to project directory and run this code
  - `python manage.py migrate`
- Run project
  - `python manage.py runserver`