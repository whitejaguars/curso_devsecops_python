#!/bin/bash
echo "Start the Deploy process:"
echo "Stop API Gunicorn Supervisor"
sudo systemctl stop wj-demo
msg=$(sudo systemctl status wj-demo 2>&1)
if [[ $msg == *found* ]];
then
    echo "Not installed, installing"
    echo "Create folder structure"
    sudo mkdir -p /opt/wj-demo/
    echo "[!] Add python virtual environment"
    sudo python3 -m venv /opt/wj-demo/venv/
    pythonpip="/opt/wj-demo/venv/bin/pip"
    if [[ -f "$pythonpip" ]]; then
        echo "[!] Virtual environment created"
    else
        echo "[X] Unable to create the virtual environment, aborting"
        exit 1
    fi
    sudo /opt/wj-demo/venv/bin/pip install -r requirements.txt
    sudo /opt/wj-demo/venv/bin/pip install gunicorn
    sudo touch /etc/systemd/system/wj-demo.service
    echo "[Unit]
    Description=Gunicorn instance to serve WhiteJaguars Demo
    After=network.target
    After=syslog.target

    [Service]
    User=root
    Group=root
    WorkingDirectory=/opt/wj-demo/
    Environment=\"PATH=/opt/wj-demo/venv/bin\"
    ExecStart=/opt/wj-demo/venv/bin/gunicorn --workers 3 wsgi:application -b $1:8000 --access-logfile /var/log/wj-demo/access.log --error-logfile /var/log/wj-demo/error.log --log-level=error

    [Install]
    WantedBy=multi-user.target
    " | sudo tee -a /etc/systemd/system/wj-demo.service
fi

sudo rm -rf /opt/wj-demo/static
sudo rm -rf /opt/wj-demo/*.py
sudo rm -rf /opt/wj-demo/application
echo "Move application Files"
sudo mv -f *.py /opt/wj-demo/
sudo mv -f application /opt/wj-demo/
echo "Deploy static content"
sudo mv -f static /opt/wj-demo/

echo "Start API Gunicorn Supervisor"
sudo systemctl start wj-demo
echo "Deploy Completed"
sleep 3
echo "Sanity Check"
msg="$(nc -vz $1 8000 2>&1)"
if [[ $msg == *succeeded* ]];
then
        echo "Gunicorn listening on port 8000: Pass"
else
        echo "Gunicorn listening on port 8000: Failed"
        exit 1
fi
msg="$(curl --max-time 5 http://$1:8000/ 2>&1)"
if [[ $msg == *WhiteJaguars* ]]; then
        echo "Site Available: Pass"
        exit 0
else
        echo "Site Available: Failed"
        exit 1
fi
