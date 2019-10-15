import io

from setuptools import setup
from setuptools import find_packages

setup(
    name='certbot-dns-hostker',
    version='0.0.2',
    description='Certbot for Hostker DNS',
    author='SkyAo',
    author_email='csvwolf@qq.com',
    url='https://www.codesky.me',
    packages=find_packages(),
    long_description=io.open('README.md', encoding='utf-8').read(),
    entry_points={
        'certbot.plugins': [
            'dns-hostker = certbot_dns_hostker.dns_hostker:Authenticator'
        ]
    }
)
