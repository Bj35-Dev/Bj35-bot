#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: https://github.com/cg8-5712
Date: 2025-02-19
Copyright (c) 2025 Dong Zhicheng G2-13
All rights reserved.

This file is part of the Bj35-Robot-Project.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import hashlib
import hmac
import base64
import time
import uuid
import logging

import aiohttp

from settings import settings
from utils.exceptions import UpdateTokenError

logger = logging.getLogger(__name__)

# Function to generate signature
def generate_signature(params, access_key_secret):
    """This function generates the signature for the request parameters."""
    # Sort request parameters in dictionary order
    sorted_params = sorted(params.items())

    logger.debug("Sorted request parameters: %s", sorted_params)

    # Construct canonical request string
    canonical_string = "&".join(["%s=%s" % (key, value) for key, value in sorted_params])
    logger.debug("Canonical request string: %s", canonical_string)

    # Construct HMAC-SHA1 signature to sign
    message = canonical_string.encode('utf-8')
    key = (access_key_secret + "&").encode('utf-8')
    signature = hmac.new(key, message, hashlib.sha1).digest()
    logger.debug("message: %s", message)
    logger.info("HMAC signature: %s", base64.b64encode(signature).decode('utf-8'))

    # Base64 encode the signature
    return base64.b64encode(signature).decode('utf-8')


async def get_access_token(access_key_id, access_key_secret):
    """This function sends a request to obtain an accessToken from YunJi."""
    # Current timestamp
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())

    logger.info("Current timestamp: %s", timestamp)

    # Unique signatureNonce
    signature_nonce = str(uuid.uuid4())

    logger.debug("Signature nonce: %s", signature_nonce)

    # Request parameters
    params = {
        # "signature": "",
        "signatureNonce": signature_nonce,
        "accessKeyId": access_key_id,
        "timestamp": timestamp,
    }

    # Generate signature
    signature = generate_signature(params, access_key_secret)

    # Add signature to request parameters
    params["signature"] = signature

    params = {
        "signature": signature,
        "signatureNonce": signature_nonce,
        "accessKeyId": access_key_id,
        "timestamp": timestamp,
    }

    logger.debug("Request parameters: %s", params)

    # Send request to get accessToken
    url = "https://open-api.yunjiai.cn/v3/auth/accessToken"

    # Parse response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as response:
            response_json = await response.json()
            if response_json["code"] == 0:
                logger.debug("Obtained accessToken: %s", response_json)
                logger.info("Obtained accessToken: %s", response_json["data"]["accessToken"])
                logger.info("Token expiration time: %s", response_json["data"]["expiration"])
                return response_json
            raise UpdateTokenError(f"Failed to obtain accessToken: {response_json['msg']}")

async def update_access_token():
    """This function updates the accessToken and expiration time."""
    access_key_id = settings.YUNJI_ACCESS_KEY_ID
    access_key_secret = settings.YUNJI_SECRET_KEY
    data = await get_access_token(access_key_id, access_key_secret)
    if data["code"] == 0:
        access_token = data["data"]["accessToken"]
        expiration = data["data"]["expiration"]

        return access_token, expiration

    raise UpdateTokenError(f"Failed to obtain accessToken: {data['msg']}")
