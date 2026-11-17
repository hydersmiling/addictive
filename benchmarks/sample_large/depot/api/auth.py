"""Token check for API requests."""

import hmac


def is_authorised(given_token, expected_token):
    return hmac.compare_digest(given_token.encode(), expected_token.encode())
