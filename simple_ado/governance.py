#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""ADO governance API wrapper."""

import logging


from simple_ado.base_client import ADOBaseClient
from simple_ado.context import ADOContext
from simple_ado.exceptions import ADOHTTPException
from simple_ado.http_client import ADOHTTPClient


class ADOGovernanceClient(ADOBaseClient):
    """Wrapper class around the ADO Governance APIs.

    :param context: The context information for the client
    :param http_client: The HTTP client to use for the client
    :param log: The logger to use
    """

    def __init__(
        self, context: ADOContext, http_client: ADOHTTPClient, log: logging.Logger
    ) -> None:
        super().__init__(context, http_client, log.getChild("governance"))

    def remove_policy(self, *, policy_id: str, governed_repository_id: str) -> None:
        """Remove a policy from a repository.

        :param str policy_id: The ID of the policy to remove
        :param str governed_repository_id: The ID of the governed repository (not necessarily the same as the ADO one)

        :raises ADOHTTPException: If removing the policy failed

        :returns: The ADO response with the data in it
        """

        request_url = self.http_client.api_endpoint(
            is_default_collection=False, subdomain="governance"
        )
        request_url += "/ComponentGovernance/GovernedRepositories"
        request_url += f"/{governed_repository_id}/policyreferences"
        request_url += f"/{policy_id}?api-version=5.1-preview.1"

        response = self.http_client.delete(request_url)

        if not response.ok:
            raise ADOHTTPException(
                f"Failed to remove policy {policy_id} from {governed_repository_id}", response
            )
