# Bug Explanation

## What was the bug?
The bug was a crash (`AttributeError`) in the `Client.request` method of `app/http_client.py`. It occurred when `self.oauth2_token` was initialized as a dictionary (e.g., loaded from a cache or passed manually) instead of an instance of the `OAuth2Token` dataclass.

## Why did it happen?
The code was checking for token validity using `if not self.oauth2_token or self.oauth2_token.expired:`. If `self.oauth2_token` was a dictionary, the first part of the condition passed (since the dict is truthy), but the second part failed because dictionaries do not have an `expired` property.

## Why does your fix actually solve it?
The fix modifies the condition to:
`if not isinstance(self.oauth2_token, OAuth2Token) or self.oauth2_token.expired:`

This ensures that:
1.  If the token is missing (`None`), it refreshes.
2.  If the token is of the wrong type (like a dictionary), it's treated as invalid and triggers a refresh.
3.  If it *is* an `OAuth2Token` object, it correctly checks the `.expired` property.
By the time the code reaches the authorization header assignment, it's guaranteed that `self.oauth2_token` has been refreshed into a proper `OAuth2Token` instance.

## What’s one realistic case / edge case your tests still don’t cover?
The current tests do not cover the behavior of `refresh_oauth2` if it were to fail (e.g., network error or invalid refresh token). In a real-world scenario, the `request` method should probably handle exceptions from `refresh_oauth2` or return a clear error if authentication fails.
