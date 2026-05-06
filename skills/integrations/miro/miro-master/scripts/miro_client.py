#!/usr/bin/env python3
"""
Miro API Client

Shared client for Miro REST API v2 authentication and requests.
Used by all Miro API scripts.

Uses access tokens for authentication.
"""

import os
import json
import time
from pathlib import Path
from urllib.parse import urlencode, quote


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://api.miro.com/v2"


class MiroClient:
    """Miro API client with access token support"""

    def __init__(self):
        self.access_token = None
        self._load_config()

    def _load_config(self):
        """Load configuration from .env"""
        env_vars = {}
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        env_vars[key.strip()] = value.strip().strip('"\'')

        self.access_token = env_vars.get('MIRO_ACCESS_TOKEN') or os.getenv('MIRO_ACCESS_TOKEN')

        if not self.access_token:
            raise ValueError("MIRO_ACCESS_TOKEN not found in .env or environment")

    def get_headers(self):
        """Get headers for API request"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get(self, path, params=None):
        """Make GET request to Miro API"""
        import requests

        url = f"{BASE_URL}/{path}"
        response = requests.get(
            url,
            headers=self.get_headers(),
            params=params,
            timeout=30
        )
        return self._handle_response(response, path)

    def post(self, path, data=None):
        """Make POST request to Miro API"""
        import requests

        url = f"{BASE_URL}/{path}"
        response = requests.post(
            url,
            headers=self.get_headers(),
            json=data,
            timeout=30
        )
        return self._handle_response(response, path)

    def patch(self, path, data=None):
        """Make PATCH request to Miro API"""
        import requests

        url = f"{BASE_URL}/{path}"
        response = requests.patch(
            url,
            headers=self.get_headers(),
            json=data,
            timeout=30
        )
        return self._handle_response(response, path)

    def put(self, path, data=None):
        """Make PUT request to Miro API"""
        import requests

        url = f"{BASE_URL}/{path}"
        response = requests.put(
            url,
            headers=self.get_headers(),
            json=data,
            timeout=30
        )
        return self._handle_response(response, path)

    def delete(self, path):
        """Make DELETE request to Miro API"""
        import requests

        url = f"{BASE_URL}/{path}"
        response = requests.delete(
            url,
            headers=self.get_headers(),
            timeout=30
        )
        if response.status_code == 204:
            return {"success": True}
        return self._handle_response(response, path)

    def _handle_response(self, response, path):
        """Handle Miro API response"""
        if response.status_code == 204:
            return {"success": True}

        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After', '5')
            raise MiroAPIError(
                f"Rate limited. Retry after {retry_after}s",
                path=path,
                status_code=429
            )

        if response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get('message', response.text)
            except (json.JSONDecodeError, ValueError):
                message = response.text
            raise MiroAPIError(
                message,
                path=path,
                status_code=response.status_code,
                response_text=response.text
            )

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            if response.text:
                raise MiroAPIError(
                    "Invalid JSON response",
                    path=path,
                    response_text=response.text
                )
            return {"success": True}

    def paginate(self, path, params=None, limit=None, data_key='data'):
        """Paginate through results using cursor/offset-based pagination"""
        params = params or {}
        results = []
        offset = 0
        page_size = min(limit or 50, 50)

        while True:
            params['limit'] = page_size
            params['offset'] = offset

            response = self.get(path, params)

            items = response.get(data_key, [])
            results.extend(items)

            total = response.get('total', 0)
            offset += len(items)

            if offset >= total or not items:
                break

            if limit and len(results) >= limit:
                results = results[:limit]
                break

            time.sleep(0.2)

        return results


class MiroAPIError(Exception):
    """Miro API Error with detailed information"""

    def __init__(self, message, path=None, status_code=None,
                 response_text=None):
        super().__init__(message)
        self.path = path
        self.status_code = status_code
        self.response_text = response_text

    def to_dict(self):
        """Convert error to dictionary for JSON output"""
        return {
            'error': str(self),
            'path': self.path,
            'status_code': self.status_code,
            'details': self.response_text
        }


def get_client():
    """Get a configured Miro client"""
    return MiroClient()


def encode_board_id(board_id):
    """URL-encode board IDs that contain special characters like ="""
    return quote(board_id, safe='')


ERROR_EXPLANATIONS = {
    401: 'Authentication failed - check your access token',
    403: 'Forbidden - insufficient permissions or scopes',
    404: 'Resource not found - check the ID',
    409: 'Conflict - resource already exists or was modified',
    429: 'Rate limited - too many requests, wait and retry',
}


def explain_error(status_code):
    """Get human-readable explanation for HTTP status code"""
    return ERROR_EXPLANATIONS.get(status_code, f'HTTP error: {status_code}')
