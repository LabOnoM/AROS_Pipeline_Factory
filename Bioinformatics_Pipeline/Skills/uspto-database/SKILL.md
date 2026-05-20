---
name: uspto-database
---
description: Generated skill uspto-database

---
name: uspto-database
description: Access USPTO APIs for patent/trademark data including search, examination history (PEDS), assignments, and status, facilitating IP analysis and prior art searches.
license: MIT
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

# USPTO Database

## Overview

Access USPTO APIs for comprehensive patent and trademark data retrieval, enabling tasks such as searching, retrieving examination history, tracking assignments, and monitoring trademark status. Facilitates IP analysis, prior art searches, and portfolio monitoring.

## When to Use This Skill

This skill should be used when you need to:

- **Patent Search**: Find patents by keywords, inventors, assignees, classifications (CPC/IPC), or dates.
- **Patent Details**: Retrieve full patent data including claims, abstracts, and citations.
- **Trademark Search**: Look up trademarks by serial or registration number.
- **Trademark Status**: Check trademark status, ownership, and prosecution history.
- **Examination History**: Access patent prosecution data from PEDS (Patent Examination Data System) including office actions and timelines.
- **Assignments**: Track patent/trademark ownership transfers.
- **Portfolio Analysis**: Analyze patent/trademark portfolios for companies or inventors.
- **Validate Patent Lifecycle**: Check maintenance fee status or expiration dates.

## Key Features

- **Patent Search API Client**: Modern ElasticSearch-based patent search (replaces legacy PatentsView).  Supports complex queries using JSON syntax.
- **PEDS Client**: Access to the Patent Examination Data System, providing examination history and transaction details.
- **TSDR Client**: Trademark Status & Document Retrieval for trademark data, including status, ownership, and prosecution history.
- **Assignment APIs**: Track ownership changes for both patents and trademarks.
- **Script-Oriented**: Designed for automation, batch queries, and integration into internal tools.

## USPTO API Ecosystem

The USPTO provides specialized APIs for different data needs:

### Core APIs

1.  **PatentSearch API** - Modern ElasticSearch-based patent search.
    -   Search patents by keywords, inventors, assignees, classifications, dates.
    -   **Base URL**: `https://search.patentsview.org/api/v1/`
    -   Rate Limit: 45 requests/minute.

2.  **PEDS (Patent Examination Data System)** - Patent examination history.
    -   Application status and transaction history from 1981-present.
    -   Office action dates and examination events.
    -   Use `uspto-opendata-python` Python library.

3.  **TSDR (Trademark Status & Document Retrieval)** - Trademark data.
    -   Trademark status, ownership, prosecution history.
    -   Search by serial or registration number.
    -   **Base URL**: `https://tsdrapi.uspto.gov/ts/cd/`

### Additional APIs

4.  **Patent Assignment Search** - Ownership records and transfers.
5.  **Trademark Assignment Search** - Trademark ownership changes.
6.  **Enriched Citation API** - Patent citation analysis.
7.  **Office Action Text Retrieval** - Full text of office actions.
8.  **Office Action Citations** - Citations from office actions.
9.  **Office Action Rejection** - Rejection reasons and types.
10. **PTAB API** - Patent Trial and Appeal Board proceedings.
11. **Patent Litigation Cases** - Federal district court litigation data.

## Quick Start

### Dependencies

-   Python `>=3.9`
-   `requests >=2.31.0`
-   `uspto-opendata-python >=0.3.0`

```bash
pip install requests uspto-opendata-python
```

### API Key Registration

USPTO APIs require an API key. Register at:

**https://account.uspto.gov/api-manager/**

API key for **PatentSearch API** is provided by PatentsView. Register at:

**https://patentsview.org/api-v01-information-page**

Set the API keys as environment variables:

```bash
export USPTO_API_KEY="your_uspto_api_key_here"
export PATENTSVIEW_API_KEY="your_patentsview_api_key_here"
```

### Helper Scripts

This skill includes Python scripts for common operations:

-   **`scripts/patent_search.py`** - PatentSearch API client for searching patents.
-   **`scripts/peds_client.py`** - PEDS client for examination history.
-   **`scripts/trademark_client.py`** - TSDR client for trademark data.

## Task 1: Searching Patents

### Using the PatentSearch API

The PatentSearch API uses a JSON query language for flexible searching.

#### Basic Patent Search Examples

```python
from scripts.patent_search import PatentSearchClient

client = PatentSearchClient()

# Search for machine learning patents
results = client.search_patents({
    "_text_all": {"patent_abstract": "machine learning"}
})

for patent in results['patents']:
    print(f"{patent['patent_number']}: {patent['patent_title']}")
```

**Search by inventor:**

```python
results = client.search_by_inventor("John Smith")
```

**Search by assignee/company:**

```python
results = client.search_by_assignee("Google")
```

**Search by date range:**

```python
results = client.search_by_date_range("2024-01-01", "2024-12-31")
```

**Search by CPC classification:**

```python
results = client.search_by_classification("H04N")  # Video/image tech
```

#### Advanced Patent Search

Combine multiple criteria with logical operators:

```python
results = client.advanced_search(
    keywords=["artificial", "intelligence"],
    assignee="Microsoft",
    start_date="2023-01-01",
    end_date="2024-12-31",
    cpc_codes=["G06N", "G06F"]  # AI and computing classifications
)
```

#### Direct API Usage

For complex queries, use the API directly:

```python
import requests
import os

url = "https://search.patentsview.org/api/v1/patent"
headers = {
    "X-Api-Key": os.environ.get("PATENTSVIEW_API_KEY"),
    "Content-Type": "application/json"
}

query = {
    "q": {
        "_and": [
            {"patent_date": {"_gte": "2024-01-01"}},
            {"assignee_organization": {"_text_any": ["Google", "Alphabet"]}},
            {"cpc_subclass_id": ["G06N", "H04N"]}
        ]
    },
    "f": ["patent_number", "patent_title", "patent_date", "inventor_name"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100, "page": 1}
}

response = requests.post(url, headers=headers, json=query)
results = response.json()
```

### Query Operators

-   **Equality**: `{"field": "value"}` or `{"field": {"_eq": "value"}}`
-   **Comparison**: `_gt`, `_gte`, `_lt`, `_lte`, `_neq`
-   **Text search**: `_text_all`, `_text_any`, `_text_phrase`
-   **String matching**: `_begins`, `_contains`
-   **Logical**: `_and`, `_or`, `_not`

**Best Practice**: Use `_text_*` operators for text fields (more performant than `_contains` or `_begins`)

### Available Patent Endpoints

-   `/patent` - Granted patents
-   `/publication` - Pregrant publications
-   `/inventor` - Inventor information
-   `/assignee` - Assignee information
-   `/cpc_subclass`, `/cpc_at_issue` - CPC classifications
-   `/uspc` - US Patent Classification
-   `/ipc` - International Patent Classification

### Reference Documentation

See `references/patentsearch_api.md` for complete PatentSearch API documentation.

## Task 2: Retrieving Patent Examination Data

### Using PEDS (Patent Examination Data System)

PEDS provides comprehensive prosecution history.

#### Basic PEDS Usage

```python
from scripts.peds_client import PEDSHelper

helper = PEDSHelper()

# By application number
app_data = helper.get_application("16123456")
print(f"Title: {app_data['title']}")
print(f"Status: {app_data['app_status']}")

# By patent number
patent_data = helper.get_patent("11234567")
```

**Get transaction history:**

```python
transactions = helper.get_transaction_history("16123456")

for trans in transactions:
    print(f"{trans['date']}: {trans['code']} - {trans['description']}")
```

**Get office actions:**

```python
office_actions = helper.get_office_actions("16123456")

for oa in office_actions:
    if oa['code'] == 'CTNF':
        print(f"Non-final rejection: {oa['date']}")
    elif oa['code'] == 'CTFR':
        print(f"Final rejection: {oa['date']}")
    elif oa['code'] == 'NOA':
        print(f"Notice of allowance: {oa['date']}")
```

#### Prosecution Analysis

Analyze prosecution patterns:

```python
analysis = helper.analyze_prosecution("16123456")

print(f"Total office actions: {analysis['total_office_actions']}")
print(f"Non-final rejections: {analysis['non_final_rejections']}")
print(f"Final rejections: {analysis['final_rejections']}")
print(f"Allowed: {analysis['allowance']}")
print(f"Responses filed: {analysis['responses']}")
```

### Reference Documentation

See `references/peds_api.md` for complete PEDS documentation.

## Task 3: Searching and Monitoring Trademarks

### Using TSDR (Trademark Status & Document Retrieval)

Access trademark status, ownership, and prosecution history.

#### Basic Trademark Usage

```python
from scripts.trademark_client import TrademarkClient

client = TrademarkClient()

# By serial number
tm_data = client.get_trademark_by_serial("87654321")

# By registration number
tm_data = client.get_trademark_by_registration("5678901")
```

**Get trademark status:**

```python
status = client.get_trademark_status("87654321")

print(f"Mark: {status['mark_text']}")
print(f"Status: {status['status']}")
print(f"Filing date: {status['filing_date']}")

if status['is_registered']:
    print(f"Registration #: {status['registration_number']}")
    print(f"Registration date: {status['registration_date']}")
```

**Check trademark health:**

```python
health = client.check_trademark_health("87654321")

print(f"Mark: {health['mark']}")
print(f"Status: {health['status']}")

for alert in health['alerts']:
    print(alert)

if health['needs_attention']:
    print("⚠️  This mark needs attention!")
```

### Common Trademark Statuses

-   **REGISTERED** - Active registered mark
-   **PENDING** - Under examination
-   **PUBLISHED FOR OPPOSITION** - In opposition period
-   **ABANDONED** - Application abandoned
-   **CANCELLED** - Registration cancelled

### Reference Documentation

See `references/trademark_api.md` for complete trademark API documentation.

## Task 4: Tracking Assignments and Ownership

### Patent and Trademark Assignments

Both patents and trademarks have Assignment Search APIs for tracking ownership changes.

#### Patent Assignment API

**Base URL**: `https://assignment-api.uspto.gov/patent/v1.4/`

**Search by patent number:**

```python
import requests
import xml.etree.ElementTree as ET
import os

def get_patent_assignments(patent_number, api_key):
    url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # Returns XML

# Replace "YOUR_API_KEY" with your actual API key
api_key = os.environ.get("USPTO_API_KEY")
assignments_xml = get_patent_assignments("11234567", api_key)
root = ET.fromstring(assignments_xml)

for assignment in root.findall('.//assignment'):
    recorded_date = assignment.find('recordedDate').text
    assignor = assignment.find('.//assignor/name').text
    assignee = assignment.find('.//assignee/name').text
    conveyance = assignment.find('conveyanceText').text

    print(f"{recorded_date}: {assignor} → {assignee}")
    print(f"  Type: {conveyance}\n")
```

### Common Assignment Types

-   **ASSIGNMENT OF ASSIGNORS INTEREST** - Ownership transfer
-   **SECURITY AGREEMENT** - Collateral/security interest
-   **MERGER** - Corporate merger
-   **CHANGE OF NAME** - Name change

## Task 5: Accessing Additional USPTO Data

### Office Actions, Citations, and Litigation

Multiple specialized APIs provide additional patent data.

#### Office Action Text Retrieval

Retrieve full text of office actions using application number. Integrate with PEDS to identify which office actions exist, then retrieve full text.

#### Enriched Citation API

Analyze patent citations:

-   Forward citations (patents citing this patent)
-   Backward citations (prior art cited)

#### Patent Litigation Cases API

Access federal district court patent litigation records.

#### PTAB API

Patent Trial and Appeal Board proceedings.

### Reference Documentation

See `references/additional_apis.md` for comprehensive documentation.

## Best Practices

1.  **API Key Management**
    -   Store API key in environment variables.
    -   Never commit keys to version control.

2.  **Rate Limiting**
    -   PatentSearch: 45 requests/minute.
    -   Implement exponential backoff for rate limit errors.
    -   Cache responses when possible.

3.  **Query Optimization**
    -   Use `_text_*` operators for text fields (more performant).
    -   Request only needed fields to reduce response size.
    -   Use date ranges to narrow searches.

4.  **Data Handling**
    -   Not all fields populated for all patents/trademarks.
    -   Handle missing data gracefully.
    -   Parse dates consistently.

5. **Authentication**
    - API keys for USPTO and/or PatentsView are required and should be provided via environment variables.

## Resources

### API Documentation

-   **PatentSearch API**: https://search.patentsview.org/docs/
-   **USPTO Developer Portal**: https://developer.uspto.gov/
-   **USPTO Open Data Portal**: https://data.uspto.gov/

### Python Libraries

-   **uspto-opendata-python**: https://pypi.org/project/uspto-opendata-python/

### Reference Files

-   `references/patentsearch_api.md` - Complete PatentSearch API reference
-   `references/peds_api.md` - PEDS API and library documentation
-   `references/trademark_api.md` - Trademark APIs (TSDR and Assignment)
-   `references/additional_apis.md` - Citations, Office Actions, Litigation, PTAB

### Scripts

-   `scripts/patent_search.py` - PatentSearch API client
-   `scripts/peds_client.py` - PEDS examination data client
-   `scripts/trademark_client.py` - Trademark search client