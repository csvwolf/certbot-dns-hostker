""" DNS Authenticator for Hostker """

import logging
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

ACCOUNT_URL = ''

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interface.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
  """Dns Authenticator for Hostker"""

  description = ('Obtain certificates using a DNS TXT record(if you are using Hostker for DNS).')

  ttl = 120

  def __init__(self, *args, **kwargs):
    super(Authenticator, self).__init__(*args, **kwargs)
    self.credentials = None
  
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
        'key': f'API key for Hostker account, obtained from {ACCOUNT_URL}'
      }
    )
  
  # add txt record
  def _perform(self, domain, validation_name, validation):
    pass

  # delete txt record
  def _cleanup(self, domain, validation_name, validation):
    pass

  def _get_hostker_client(self):
    pass

class HostkerClient:
  pass