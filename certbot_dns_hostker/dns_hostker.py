""" DNS Authenticator for Hostker """

import logging
import zope.interface
import requests

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://www.hostker.com/'

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
  """Dns Authenticator for Hostker"""

  description = ('Obtain certificates using a DNS TXT record(if you are using Hostker for DNS).')

  ttl = 60

  def __init__(self, *args, **kwargs):
    super(Authenticator, self).__init__(*args, **kwargs)
    self.credentials = None
  
  @classmethod
  def add_parser_arguments(cls, add):
    super(Authenticator, cls).add_parser_arguments(add)
    add('credentials', help='Hostker credentials INI file.')

  def more_info(self):
    return 'This plugin configures a DNS TXT record to response to a dns-01 challenge using the Hostker API'

  def _setup_credentials(self):
    self.credentials = self._configure_credentials(
      'credentials',
      'Hostker credentials INI file',
      {
        'email': 'email address associated with Hostker account',
        'token': f'API token for Hostker account, obtained from {ACCOUNT_URL}'
      }
    )
  
  # add txt record
  def _perform(self, domain, validation_name, validation):
    record_name = validation_name.split(f'.{domain}')[0]
    self._get_hostker_client().add_txt_record(domain, record_name, validation, self.ttl)

  # delete txt record
  def _cleanup(self, domain, validation_name, validation):
    record_name = validation_name.split(f'.{domain}')[0]
    self._get_hostker_client().del_txt_record(domain, record_name)

  def _get_hostker_client(self):
    return HostkerClient(self.credentials.conf('email'), self.credentials.conf('token'))

class HostkerClient:
  """Encapsulates all communication with the Hostker API"""

  def __init__(self, email, token):
    self.email = email
    self.token = token
    
  
  def add_txt_record(self, domain, record_name, record_content, record_ttl):
    params = {
      'domain': domain,
      'header': record_name,
      'type': 'TXT',
      'data': record_content,
      'ttl': record_ttl,
      'email': self.email,
      'token': self.token,
    }

    r = requests.post('https://i.hostker.com/api/dnsAddRecord', data=params, headers={
      'Content-Type': 'application/x-www-form-urlencoded'
    })
    result = r.json()
    if result['success'] == 0:
      raise errors.PluginError(result['errorMessage'])
    else:
      logger.debug('Successfully add TXT record')

  def del_txt_record(self, domain, record_name):
    record_ids = self._get_record_ids(domain, record_name)
    for id in record_ids:
      r = requests.post('https://i.hostker.com/api/dnsDeleteRecord', data={
        'email': self.email,
        'token': self.token,
        'id': id
      }, headers={
      'Content-Type': 'application/x-www-form-urlencoded'
      })
      result = r.json()
      if result['success'] == 0:
        raise errors.PluginError(f'error when delete record: {result["errorMessage"]}')
      else:
        logger.debug('Successfully remove TXT record')

  def _get_record_ids(self, domain, record_name):
    r = requests.post('https://i.hostker.com/api/dnsGetRecords', data={
      'email': self.email,
      'token': self.token,
      'domain': domain
    }, headers={
      'Content-Type': 'application/x-www-form-urlencoded'
    })
    result = r.json()
    if result['success'] == 0:
      raise errors.PluginError(result['errorMessage'])
    logger.debug(result)
    records = list(filter(lambda record: record['header']==record_name and record['type'] == 'TXT', result['records']))
    return [record['id'] for record in records]
