# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from pymsn.service.SOAPService import SOAPService, url_split
from pymsn.service.SOAPUtils import XMLTYPE
from pymsn.service.SingleSignOn import *

from pymsn.gnet.protocol import ProtocolFactory

__all__ = ['Storage']

# Get the DP
# - GetProfile
# - GetDocument on the photo RID
# - HTTP request

# Change the Display Name and Personal Message
# - UpdateProfile

# Change the DP
# - DeleteRelationship /UserTiles between the CID and the photo RID
# - DeleteRelationship between Expression profile and the photo RID
# - CreateDocument between CID and the new photo, get the new RID
# - CreateRelationship between the Expression profile and the photo RID

class Storage(SOAPService):

    def __init__(self, sso, proxies=None):
        self._sso = sso
        self._tokens = {}
        SOAPService.__init__(self, "SchematizedStore", proxies)

    @RequireSecurityTokens(LiveService.CONTACTS)
    def GetProfile(self, callback, errback, scenario, cid, profile_rid, 
                   p_date_modified, expression_rid, e_date_modified, 
                   display_name, dn_last_modified, personal_status, 
                   ps_last_modified, user_tile_url, photo, flags):
        self.__soap_request(self._service.GetProfile, scenario,
                 (cid, 
                  XMLTYPE.bool.encode(profile_rid),
                  XMLTYPE.bool.encode(p_date_modified),
                  XMLTYPE.bool.encode(expression_rid),
                  XMLTYPE.bool.encode(e_date_modified),
                  XMLTYPE.bool.encode(display_name),
                  XMLTYPE.bool.encode(dn_last_modified),
                  XMLTYPE.bool.encode(personal_status),
                  XMLTYPE.bool.encode(ps_last_modified),
                  XMLTYPE.bool.encode(user_tile_url),
                  XMLTYPE.bool.encode(photo),
                  XMLTYPE.bool.encode(flags)),
                 callback, errback)

    def _HandleGetProfileResponse(self, callback, errback, response, user_date):
        profile_rid = response.findtext('./st:ResourceID')        
        
        profile = response.find('./st:ExpressionProfile')
        display_name = profile.findtext('./st:DisplayName')
        personal_msg = profile.findtext('./st:PersonalStatus')
        
        callback[0](profile_rid, display_name, personal_msg, *callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def UpdateProfile(self, callback, errback, scenario, profile_rid,
                      display_name, personal_status, flags):
        self.__soap_request(self._service.UpdateProfile, scenario,
                            (profile_rid, display_name, personal_status, flags),
                            callback, errback)

    def _HandleUpdateProfileResponse(self, callback, errback, response, user_date):
        callback[0](*callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def CreateRelationships(self, callback, errback):
        pass

    def _HandleCreateRelationshipsResponse(self, callback, errback, response, user_date):
        pass

    @RequireSecurityTokens(LiveService.CONTACTS)
    def DeleteRelationships(self, callback, errback):
        pass

    def _HandleDeleteRelationshipsResponse(self, callback, errback, response, user_date):
        pass

    @RequireSecurityTokens(LiveService.CONTACTS)
    def CreateDocument(self, callback, errback):
        pass

    def _HandleCreateDocumentResponse(self, callback, errback, response, user_date):
        pass

    @RequireSecurityTokens(LiveService.CONTACTS)
    def FindDocuments(self, callback, errback):
        pass

    def _HandleFindDocumentsResponse(self, callback, errback, response, user_date):
        pass

    def __soap_request(self, method, scenario, args, callback, errback):
        token = str(self._tokens[LiveService.CONTACTS])   

        http_headers = method.transport_headers()
        soap_action = method.soap_action()
        
        soap_header = method.soap_header(scenario, token)
        soap_body = method.soap_body(*args)

        method_name = method.__name__.rsplit(".", 1)[1]
        self._send_request(method_name, 
                           self._service.url, 
                           soap_header, soap_body, soap_action, 
                           callback, errback, http_headers)

#     def get_display_picture(self, url, callback, errback):
#         scheme, host, port, resource = url_split(url)
#         print "scheme=%s;host=%s;port=%s;resource=%s" % (scheme, host, port, resource)
#         http_headers = {}
#         http_headers["Accept"] = "*/*"
#         http_headers["Proxy-Connection"] = "Keep-Alive"
#         http_headers["Connection"] = "Keep-Alive"
        
#         proxy = self._proxies.get(scheme, None)
#         transport = ProtocolFactory(scheme, host, 80, proxy=proxy)
#         transport.connect("response-received", self._dp_callback)
#         transport.connect("request-sent", self._request_handler)
#         transport.connect("error", self._dp_errback)

#         transport.request(resource, http_headers, method='GET')
