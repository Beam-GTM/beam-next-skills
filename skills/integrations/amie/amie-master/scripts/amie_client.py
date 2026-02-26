#!/usr/bin/env python3
"""
Amie API Client

Shared client for Amie API (meeting notes, transcripts, action items).
Uses Personal Access Token (PAT) authentication.
"""

import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Base URL for Amie API
DEFAULT_BASE_URL = "https://calendar.amie.so/api/v1"


class AmieClient:
    """Amie API client with PAT authentication"""

    def __init__(self):
        self.api_token = None
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

        self.api_token = env_vars.get('AMIE_API_TOKEN') or os.getenv('AMIE_API_TOKEN')
        self.base_url = env_vars.get('AMIE_API_BASE_URL') or os.getenv('AMIE_API_BASE_URL') or DEFAULT_BASE_URL

        if not self.api_token:
            raise ValueError("AMIE_API_TOKEN not found in .env or environment")

    def get_headers(self):
        """Get headers for API request"""
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        """Make GET request"""
        import requests

        url = f"{self.base_url}{endpoint}"
        response = requests.get(
            url,
            headers=self.get_headers(),
            params=params,
            timeout=60
        )
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle API response"""
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except:
                return {"status": "success"}
        elif response.status_code == 401:
            raise Exception("Authentication failed - check your AMIE_API_TOKEN")
        elif response.status_code == 404:
            raise Exception(f"Not found: {response.url}")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")


def get_client():
    """Get a configured Amie client"""
    return AmieClient()
