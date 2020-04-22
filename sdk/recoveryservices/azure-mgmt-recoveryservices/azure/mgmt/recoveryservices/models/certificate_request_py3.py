# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CertificateRequest(Model):
    """Details of the certificate to be uploaded to the vault.

    :param properties:
    :type properties: ~azure.mgmt.recoveryservices.models.RawCertificateData
    """

    _attribute_map = {
        'properties': {'key': 'properties', 'type': 'RawCertificateData'},
    }

    def __init__(self, *, properties=None, **kwargs) -> None:
        super(CertificateRequest, self).__init__(**kwargs)
        self.properties = properties