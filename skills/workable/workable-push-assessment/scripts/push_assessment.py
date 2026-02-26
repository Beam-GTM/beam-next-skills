#!/usr/bin/env python3
"""
Workable Push Assessment Script
Searches for a candidate by name and posts an assessment comment to their profile.

Usage:
    python3 push_assessment.py --candidate "Sarah Chen" --assessment "assessment text"
    python3 push_assessment.py --candidate "Sarah Chen" --file assessment.md
    python3 push_assessment.py --candidate-id abc123 --assessment "assessment text"
    python3 push_assessment.py --search "Sarah"  # search only, don't post
    python3 push_assessment.py --list-jobs        # list open jobs
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path


def get_config():
    """Load Workable API config from environment or .env file."""
    api_key = os.environ.get("WORKABLE_API_KEY")
    subdomain = os.environ.get("WORKABLE_SUBDOMAIN")

    if not api_key or not subdomain:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key == "WORKABLE_API_KEY" and not api_key:
                        api_key = value
                    elif key == "WORKABLE_SUBDOMAIN" and not subdomain:
                        subdomain = value

    if not api_key:
        print("❌ WORKABLE_API_KEY not set. Add it to your .env file:")
        print("   WORKABLE_API_KEY=your_api_key_here")
        print("\n   Get your key from: Workable → Settings → Integrations → Apps → Generate API token")
        sys.exit(1)

    if not subdomain:
        print("❌ WORKABLE_SUBDOMAIN not set. Add it to your .env file:")
        print("   WORKABLE_SUBDOMAIN=your_subdomain")
        print("\n   Your subdomain is the part before .workable.com in your Workable URL")
        sys.exit(1)

    return api_key, subdomain


def api_request(method, endpoint, api_key, subdomain, data=None):
    """Make a request to the Workable API v3."""
    url = f"https://{subdomain}.workable.com/spi/v3{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ API Error {e.code}: {e.reason}")
        if error_body:
            try:
                err = json.loads(error_body)
                print(f"   {json.dumps(err, indent=2)}")
            except json.JSONDecodeError:
                print(f"   {error_body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Connection error: {e.reason}")
        sys.exit(1)


def api_request_url(method, full_url, api_key, data=None):
    """Make a request to a full Workable API URL (for pagination)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(full_url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ API Error {e.code}: {e.reason}")
        if error_body:
            try:
                err = json.loads(error_body)
                print(f"   {json.dumps(err, indent=2)}")
            except json.JSONDecodeError:
                print(f"   {error_body}")
        return None
    except urllib.error.URLError as e:
        print(f"❌ Connection error: {e.reason}")
        return None


def search_candidates(name, api_key, subdomain, months_back=12):
    """Search for candidates by name across all jobs with pagination."""
    print(f"\n🔍 Searching for candidates matching '{name}'...")

    from datetime import datetime, timedelta
    created_after = (datetime.now() - timedelta(days=months_back * 30)).strftime("%Y-%m-%d")

    base = f"https://{subdomain}.workable.com/spi/v3"
    matches = []
    name_lower = name.lower()
    next_url = f"{base}/candidates?limit=100&created_after={created_after}"
    pages = 0
    max_pages = 20

    while next_url and pages < max_pages:
        result = api_request_url("GET", next_url, api_key)
        if not result:
            break
        candidates = result.get("candidates", [])
        pages += 1

        for c in candidates:
            full_name = c.get("name", f"{c.get('firstname', '')} {c.get('lastname', '')}").strip()
            if name_lower in full_name.lower():
                matches.append({
                    "id": c.get("id"),
                    "name": full_name,
                    "email": c.get("email", ""),
                    "job": c.get("job", {}).get("title", "Unknown"),
                    "stage": c.get("stage", "Unknown"),
                    "shortcode": c.get("job", {}).get("shortcode", ""),
                    "profile_url": c.get("profile_url", ""),
                })

        next_link = result.get("paging", {}).get("next", "")
        next_url = next_link if next_link and candidates else None

    if not matches:
        print(f"   No candidates found matching '{name}' (searched last {months_back} months, {pages} pages).")
        print("   Tip: Try first name only, or use --candidate-id if you have the ID from Workable.")
        return []

    seen_ids = set()
    unique_matches = []
    for m in matches:
        if m["id"] not in seen_ids:
            seen_ids.add(m["id"])
            unique_matches.append(m)

    print(f"   Found {len(unique_matches)} match(es):\n")
    for i, m in enumerate(unique_matches, 1):
        print(f"   {i}. {m['name']} — {m['job']} ({m['stage']})")
        print(f"      Email: {m['email']} | ID: {m['id']}")
        if m.get("profile_url"):
            print(f"      URL: {m['profile_url']}")

    return unique_matches


def get_member_id(api_key, subdomain):
    """Get the current user's member ID for posting comments."""
    result = api_request("GET", "/members?limit=100", api_key, subdomain)
    members = result.get("members", [])

    if not members:
        print("⚠️  No members found. Comment will be posted without member attribution.")
        return None

    if len(members) == 1:
        return members[0]["id"]

    jonas_match = None
    for m in members:
        name = m.get("name", "").lower()
        email = m.get("email", "").lower()
        if "jonas" in name or "jbd" in email or "diezun" in name:
            jonas_match = m
            break

    if jonas_match:
        return jonas_match["id"]

    return members[0]["id"]


def post_comment(candidate_id, body, member_id, api_key, subdomain):
    """Post a comment/assessment to a candidate's profile."""
    print(f"\n📝 Posting comment to candidate {candidate_id}...")

    payload = {
        "member_id": member_id,
        "comment": {
            "body": body,
        },
    }

    result = api_request("POST", f"/candidates/{candidate_id}/comments", api_key, subdomain, data=payload)
    print("✅ Comment posted successfully!")
    return result


def post_review(candidate_id, body, grade, member_id, api_key, subdomain):
    """Post a formal evaluation/review to a candidate's profile.

    Grade is on the thumbs scale: 0=no, 1=maybe, 2=yes.
    Only one review per member per stage is allowed.
    """
    print(f"\n📝 Posting review to candidate {candidate_id} (grade={grade})...")

    payload = {
        "member_id": member_id,
        "comment": body,
        "grade": grade,
    }

    result = api_request("POST", f"/candidates/{candidate_id}/ratings", api_key, subdomain, data=payload)
    print("✅ Review posted successfully!")
    return result


def list_jobs(api_key, subdomain):
    """List open jobs."""
    print("\n📋 Open jobs:\n")
    result = api_request("GET", "/jobs?state=published&limit=50", api_key, subdomain)

    jobs = result.get("jobs", [])
    if not jobs:
        print("   No open jobs found.")
        return

    for j in jobs:
        title = j.get("title", "Unknown")
        shortcode = j.get("shortcode", "")
        department = j.get("department", "")
        location = j.get("location", {}).get("city", "Remote")
        print(f"   • {title} [{shortcode}] — {department} | {location}")

    return jobs


def format_assessment_for_workable(assessment_text):
    """Format the assessment nicely for Workable's comment field.
    
    Workable comments support basic HTML, so we convert markdown-style
    formatting to something that renders well.
    """
    lines = assessment_text.strip().split("\n")
    formatted = []

    for line in lines:
        if line.startswith("# "):
            formatted.append(f"<h3>{line[2:]}</h3>")
        elif line.startswith("## "):
            formatted.append(f"<h4>{line[3:]}</h4>")
        elif line.startswith("### "):
            formatted.append(f"<b>{line[4:]}</b>")
        elif line.startswith("- "):
            formatted.append(f"• {line[2:]}")
        elif line.startswith("**") and line.endswith("**"):
            formatted.append(f"<b>{line[2:-2]}</b>")
        elif line.strip() == "---":
            formatted.append("—" * 40)
        elif line.strip() == "":
            formatted.append("")
        else:
            formatted.append(line)

    return "\n".join(formatted)


def main():
    parser = argparse.ArgumentParser(description="Push interview assessments to Workable")
    parser.add_argument("--candidate", help="Candidate name to search for")
    parser.add_argument("--candidate-id", help="Candidate ID (skip search)")
    parser.add_argument("--assessment", help="Assessment text to post")
    parser.add_argument("--file", help="Path to assessment file (.md or .txt)")
    parser.add_argument("--search", help="Search for candidate by name (don't post)")
    parser.add_argument("--list-jobs", action="store_true", help="List open jobs")
    parser.add_argument("--raw", action="store_true", help="Don't format assessment (post as-is)")
    parser.add_argument("--review", action="store_true", help="Post as formal review/evaluation instead of comment")
    parser.add_argument("--grade", type=int, choices=[0, 1, 2], help="Review grade: 0=no, 1=maybe, 2=yes (required with --review)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()
    api_key, subdomain = get_config()

    if args.list_jobs:
        list_jobs(api_key, subdomain)
        return

    if args.search:
        matches = search_candidates(args.search, api_key, subdomain)
        if args.json:
            print(json.dumps(matches, indent=2))
        return

    if not args.candidate and not args.candidate_id:
        print("❌ Provide --candidate 'Name' or --candidate-id 'ID'")
        sys.exit(1)

    if not args.assessment and not args.file:
        print("❌ Provide --assessment 'text' or --file path/to/assessment.md")
        sys.exit(1)

    assessment_text = args.assessment
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        assessment_text = file_path.read_text()

    if not args.raw:
        assessment_text = format_assessment_for_workable(assessment_text)

    candidate_id = args.candidate_id
    if not candidate_id:
        matches = search_candidates(args.candidate, api_key, subdomain)
        if not matches:
            sys.exit(1)
        if len(matches) == 1:
            candidate_id = matches[0]["id"]
            print(f"\n   → Using: {matches[0]['name']} ({matches[0]['job']})")
        else:
            print("\n   Multiple matches found. Please specify with --candidate-id")
            print("   Or narrow down the name.")
            sys.exit(1)

    member_id = get_member_id(api_key, subdomain)

    if args.review:
        if args.grade is None:
            print("❌ --grade is required with --review (0=no, 1=maybe, 2=yes)")
            sys.exit(1)
        result = post_review(candidate_id, assessment_text, args.grade, member_id, api_key, subdomain)
    else:
        result = post_comment(candidate_id, assessment_text, member_id, api_key, subdomain)

    if args.json and result:
        print(json.dumps(result, indent=2))

    print("\n🎯 Done! Assessment is now visible on the candidate's Workable profile.")


if __name__ == "__main__":
    main()
