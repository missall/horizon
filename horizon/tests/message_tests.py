# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django import http
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from horizon import messages
from horizon import middleware
from horizon import test
from horizon.openstack.common import jsonutils


class MessageTests(test.TestCase):
    def test_middleware_header(self):
        req = self.request
        string = _("Giant ants are attacking San Francisco!")
        expected = ["error", force_unicode(string)]
        self.assertTrue("async_messages" in req.horizon)
        self.assertItemsEqual(req.horizon['async_messages'], [])
        req.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        messages.error(req, string)
        self.assertItemsEqual(req.horizon['async_messages'], [expected])
        res = http.HttpResponse()
        res = middleware.HorizonMiddleware().process_response(req, res)
        self.assertEqual(res['X-Horizon-Messages'],
                         jsonutils.dumps([expected]))
