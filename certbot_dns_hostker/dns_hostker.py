""" DNS Authenticator for Hostker """

import logging
import zope.interface
import requests

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from ker import Ker
from ker import HostkerRequestError

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://www.hostker.com/'


def validate_domain_to_record(domain):
  domain_list = domain.split('.')[:-2]
  if len(domain_list) > 0 and domain_list[-1] == '*':
    domain_list = domain_list[:-1]
  return '.'.join(domain_list)

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
    record_name = validate_domain_to_record(validation_name)
    self._get_hostker_client().add_txt_record(domain, record_name, validation, self.ttl)

  # delete txt record
  def _cleanup(self, domain, validation_name, validation):
    record_name = validate_domain_to_record(validation_name)
    self._get_hostker_client().del_txt_record(domain, record_name)

  def _get_hostker_client(self):
    return HostkerClient(self.credentials.conf('email'), self.credentials.conf('token'))

class HostkerClient:
  """Encapsulates all communication with the Hostker API"""

  def __init__(self, email, token):
    self.ker = Ker(email, token)
    
  
  def add_txt_record(self, domain, record_name, record_content, record_ttl):
    try:
      self.ker.dns.add(domain=domain, header=record_name, record_type='TXT', data=record_content, ttl=record_ttl)
    except HostkerRequestError as err:
      raise errors.PluginError(str(err))
    else:
      logger.debug('Successfully add TXT record')

  def del_txt_record(self, domain, record_name):
    record_ids = self._get_record_ids(domain, record_name)
    for unique_id in record_ids:
      try:
        self.ker.dns.delete(unique_id)
      except HostkerRequestError as err:
        raise errors.PluginError(str(err))
      else:
        logger.debug('Successfully remove TXT record')

  def _get_record_ids(self, domain, record_name):
    try:
      result = self.ker.dns.list(domain)
    except HostkerRequestError as err:
      raise errors.PluginError(str(err))
    else:
      logger.debug(result)
      records = list(filter(lambda record: record['header']==record_name and record['type'] == 'TXT', result['records']))
      return [record['id'] for record in records]
