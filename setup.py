from setuptools import setup
from setuptools import find_packages

setup(
  name='certbot-dns-hostker',
  version='0.0.1',
  description='Certbot for Hostker DNS',
  author='SkyAo',
  author_email='csvwolf@qq.com',
  url='https://www.codesky.me',
  packages=find_packages(),
  entry_points={
    'certbot.plugins': [
      'dns-hostker = certbot_dns_hostker.dns_hostker:Authenticator'
    ]
  }
)