""" Tests for certbot_dns_hostker.dns_hostker """

import unittest
import mock

from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util

from .dns_hostker import validate_domain_to_record
from .dns_hostker import sub_domain_to_tld

TOKEN = '123456'
EMAIL = 'test@codesky.me'


class UtilsTest(unittest.TestCase):
    """
    Utils for domain handler
    """
    def test_validate_domain_to_record(self):
        """
        validate domain to hostker needed record name
        """
        self.assertEqual(
            validate_domain_to_record('_acme-challenge.foo.baidu.com'), '_acme-challenge.foo'
        )
        self.assertEqual(validate_domain_to_record('google.com'), '')
        self.assertEqual(validate_domain_to_record('*.python.org'), '')

    def test_sub_domain_to_tld(self):
        """
        domain to tld
        """
        self.assertEqual(sub_domain_to_tld('tieba.baidu.com'), 'baidu.com')
        self.assertEqual(sub_domain_to_tld('google.com'), 'google.com')


class AuthenticatorTest(test_util.TempDirTestCase, dns_test_common.BaseAuthenticatorTest):
    """
    certbot hostker plugin test
    """
    def setUp(self):
        """
        init
        """
        from certbot_dns_hostker.dns_hostker import Authenticator

        super(AuthenticatorTest, self).setUp()

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write({'hostker_token': TOKEN, 'hostker_email': EMAIL}, path)

        self.config = mock.MagicMock(hostker_credentials=path, hostker_propagation_seconds=0)
        self.auth = Authenticator(self.config, 'hostker')
        self.mock_client = mock.MagicMock()
        # pylint: disable=protected-access
        self.auth._get_hostker_client = mock.MagicMock(return_value=self.mock_client)

    def test_perform(self):
        """
        add record test
        """
        self.auth.perform([self.achall])
        record_name = validate_domain_to_record(f'_acme-challenge.{DOMAIN}')
        domain = sub_domain_to_tld(DOMAIN)
        expected = [mock.call.add_txt_record(domain, record_name, mock.ANY, mock.ANY)]
        self.assertEqual(expected, self.mock_client.mock_calls)

    def test_cleanup(self):
        """
        remove record test
        """
        # pylint: disable=protected-access
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])
        record_name = validate_domain_to_record(f'_acme-challenge.{DOMAIN}')
        domain = sub_domain_to_tld(DOMAIN)
        expected = [mock.call.del_txt_record(domain, record_name)]
        self.assertEqual(expected, self.mock_client.mock_calls)


if __name__ == '__main__':
    unittest.main()
