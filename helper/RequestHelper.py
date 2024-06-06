#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2023/01/20 00:00
# Create User: NB-Dragon
import certifi
import urllib3


class RequestHelper(object):
    def __init__(self):
        self._user_token = None
        self._accept_response_code = [200, 201, 202, 203, 204, 205, 206]

    def set_user_token(self, user_token):
        self._user_token = user_token

    def _get_request_header(self):
        user_agent = self._generate_user_agent()
        request_header = {"user-agent": user_agent, "content-type": "application/json", "b": 690}
        if self._user_token is not None:
            request_header["t"] = self._user_token
        return request_header

    def request_get_method(self, request_link):
        try:
            request_header = self._get_request_header()
            pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=30)
            response = pool_manager.request("GET", request_link, preload_content=False, headers=request_header)
            content, status = response.data, response.status
            response.close()
            return content if status in self._accept_response_code else None
        except Exception as e:
            print("[GET] 请求异常，异常信息为: {}".format(str(e)))
            return None

    def request_post_method(self, request_link, request_data):
        try:
            request_header = self._get_request_header()
            pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=30)
            response = pool_manager.request("POST", request_link, fields=request_data, headers=request_header)
            content, status = response.data, response.status
            response.close()
            return content if status in self._accept_response_code else None
        except Exception as e:
            print("[POST] 请求异常，异常信息为: {}".format(str(e)))
            return None

    @staticmethod
    def _generate_user_agent():
        user_agent_list = list()
        user_agent_list.append("Mozilla/5.0 (X11; Linux x86_64)")
        user_agent_list.append("AppleWebKit/537.36 (KHTML, like Gecko)")
        user_agent_list.append("MicroMessenger/8.0.21.2120(0x2800153B)")
        user_agent_list.append("MiniProgramEnv/android")
        return " ".join(user_agent_list)
