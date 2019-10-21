# CertBot DNS Hostker

[![Build Status](https://travis-ci.com/csvwolf/certbot-dns-hostker.svg?branch=master)](https://travis-ci.com/csvwolf/certbot-dns-hostker)

### Install
```
pip install certbot-dns-hostker
```

### Usage
```
certbot certonly --authenticator certbot-dns-hostker:dns-hostker --certbot-dns-hostker:dns-hostker-credentials [configfile-path] -d [your-domain]
```

### config.ini
```
certbot_dns_hostker:dns_hostker_email=[your email]
certbot_dns_hostker:dns_hostker_token=[your token]
```

### Help
#### Why I can't run successful?

f-string is a feature in Python3.6+, please ensure your python version.

#### How about the Dockerfile?
If you don't understand, do not use it.