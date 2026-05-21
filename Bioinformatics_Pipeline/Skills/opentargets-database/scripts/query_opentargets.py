#!/usr/bin/env python3
# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Queries the Open Targets Platform GraphQL API.

This script provides reusable functions for querying the Open Targets Platform
GraphQL API, including target, disease, drug, and association data. It also
provides a command-line interface to query various endpoints of the Open Targets
GraphQL API, including GWAS studies, QTL credible sets, L2G predictions,
target druggability, and disease/target associations.

Dependencies: science-skills-common (for robust HTTP client with QPS limiting)
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "science-skills-common",
# ]
# [tool.uv.sources]
# science-skills-common = { path = "../../science_skills_common" }
# ///

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional

from science_skills.science_skills_common import http_client


# API endpoint
BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"
_CLIENT = http_client.HttpClient(BASE_URL, qps=1.0)

def execute_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute a GraphQL query against the Open Targets Platform API.

    Args:
        query: GraphQL query string
        variables: Optional dictionary of variables for the query

    Returns:
        Dictionary containing the API response data

    Raises:
        Exception if the API request fails or returns errors
    """
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        # Use the robust _CLIENT from science_skills_common
        response_data = _CLIENT.post(json=payload)

        if "errors" in response_data:
            raise Exception(f"GraphQL errors: {response_data['errors']}")

        return response_data.get("data", {})

    except Exception as e: # Catching generic Exception as _CLIENT might raise its own types
        raise Exception(f"API request failed: {str(e)}")

def normalize_variant_id(variant_id: str) -> str:
  """Normalize variant I

def search_entities(query_string: str, entity_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Search for targets, diseases, or drugs by name or identifier.

    Args:
        query_string: Search term (e.g., "BRCA1", "alzheimer", "aspirin")
        entity_types: Optional list to filter by entity type ["target", "disease", "drug"]

    Returns:
        List of search results with id, name, entity type, and description
    """
    query = """
      query search($queryString: String!, $entityNames: [String!]) {
        search(queryString: $queryString, entityNames: $entityNames, page: {size: 10}) {
          hits {
            id
            entity
            name
            description
          }
        }
      }
    """

    variables = {"queryString": query_string}
    if entity_types:
        variables["entityNames"] = entity_types

    result = execute_query(query, variables)
    return result.get("search", {}).get("hits", [])

def get_target_info(ensembl_id: str, include_diseases: bool = False) -> Dict[str, Any]:
    """
    Retrieve comprehensive information about a target gene.

    Args:
        ensembl_id: Ensembl gene ID (e.g., "ENSG00000157764")
        include_diseases: Whether to include top associated diseases

    Returns:
        Dictionary with target information including tractability, safety, expression
    """
    disease_fragment = """
      associatedDiseases(page: {size: 10}) {
        rows {
          disease {
            id
            name
          }
          score
          datatypeScores {
            componentId
            score
          }
        }
    """