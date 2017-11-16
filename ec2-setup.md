# Code Deploy setup
```
sudo yum -y update
sudo yum install -y ruby
cd /home/ec2-user
sudo curl -O https://aws-codedeploy-ap-northeast-1.s3.amazonaws.com/latest/install
sudo chmod +x ./install
sudo ./install auto
```

# Code Setup
```
sudo yum install git
git clone https://github.com/kozenumezawa/causalvis-server.git
```

# Install Libraries
```
wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda3-4.0.0-Linux-x86_64.sh
bash Anaconda3-4.0.0-Linux-x86_64.sh
export PATH="$HOME/miniconda3/bin:$PATH"
source .bashrc
pip install falcon
```

# Server Setup
```
sudo yum install nginx
sudo chkconfig nginx on
sudo service nginx start
sudo vim /etc/nginx/conf.d/falcon_app.conf
```

```falcon_app.conf
server {
    listen 80;
    server_name localhost;
    client_max_body_size 50M;

    location / {
        if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST,PUT,OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        return 204;
         }
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://localhost:3000; #(if your project is running in port 3000)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST,PUT,OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
    }
}
```
sudo vim /etc/nginx/nginx.conf
```
- listen       80 default_server;
- listen       [::]:80 default_server;
+ listen       81 default_server;
+ listen       [::]:81 default_server;
```
```
sudo service nginx restart
```

# Run
```
nohup python main.py &
ps u
sudo kill process id
```