from typing import Optional
import json
import re

import httpx
import trafilatura
import lxml.html


def _fetch_html(url: str, timeout: float = 20.0) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    with httpx.Client(follow_redirects=True, headers=headers, timeout=timeout) as client:
        resp = client.get(url)
        resp.raise_for_status()
        ctype = resp.headers.get("content-type", "")
        if "html" not in ctype.lower():
            return ""
        return resp.text


def _extract_from_json_ld(tree: lxml.html.HtmlElement) -> dict:
    """Try to find a JobPosting object inside JSON-LD script tags using lxml."""
    scripts = tree.xpath('//script[@type="application/ld+json"]/text()')
    for script_text in scripts:
        try:
            data = json.loads(script_text or "")
        except Exception:
            continue
        candidates = data if isinstance(data, list) else [data]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            if item.get("@graph"):
                graph = item.get("@graph")
                for node in (graph if isinstance(graph, list) else [graph]):
                    if isinstance(node, dict) and node.get("@type") and "JobPosting" in str(node.get("@type", "")):
                        return node
            if item.get("@type") and "JobPosting" in str(item.get("@type", "")):
                return item
    return {}


def _clean_text(s: Optional[str]) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\r\n|\r", "\n", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def extract_job_from_url(url: str) -> str:
    """Fetch a LinkedIn job URL and return a plain-text job summary.

    Strategy:
    - Fetch the page HTML with a realistic User-Agent.
    - Try to parse structured data (JSON-LD) for JobPosting fields.
    - Fall back to `trafilatura` extraction for the full description and use <title>/meta tags for basic fields.

    Returns a human-readable plain text string containing Title, Company, Location and Description.
    """
    html = _fetch_html(url)
    if not html:
        return ""

    # Parse with lxml
    try:
        tree = lxml.html.fromstring(html)
    except Exception:
        # fallback: let trafilatura handle broken HTML
        tree = lxml.html.fromstring("<html></html>")

    # 1) Try JSON-LD JobPosting first (most reliable when present)
    job_ld = _extract_from_json_ld(tree)

    title = None
    company = None
    location = None
    description = None

    if job_ld:
        title = job_ld.get("title") or job_ld.get("name")
        hiring = job_ld.get("hiringOrganization") or job_ld.get("hiringOrg")
        if isinstance(hiring, dict):
            company = hiring.get("name")
        elif isinstance(hiring, str):
            company = hiring

        job_loc = job_ld.get("jobLocation") or job_ld.get("jobLocationType")
        if isinstance(job_loc, dict):
            address = job_loc.get("address") or {}
            if isinstance(address, dict):
                location = ", ".join(filter(None, [address.get("addressLocality"), address.get("addressRegion"), address.get("addressCountry")]))
        elif isinstance(job_loc, list):
            parts = []
            for jl in job_loc:
                addr = (jl.get("address") if isinstance(jl, dict) else {}) or {}
                parts.append(", ".join(filter(None, [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")])) )
            location = "; ".join([p for p in parts if p])
        else:
            location = job_ld.get("jobLocationType") or job_ld.get("workLocation")

        raw_desc = job_ld.get("description")
        description = _clean_text(raw_desc)

    # 2) Fallbacks for title/company/location using lxml
    if not title:
        title_nodes = tree.xpath('//meta[@property="og:title"]/@content | //meta[@name="og:title"]/@content')
        if title_nodes:
            title = title_nodes[0]
        else:
            title_el = tree.find('.//title')
            if title_el is not None and title_el.text:
                title = title_el.text

    if not company:
        org_meta_nodes = tree.xpath('//meta[@property="og:site_name"]/@content | //meta[@name="twitter:creator"]/@content')
        if org_meta_nodes:
            company = org_meta_nodes[0]
        else:
            org_el = tree.xpath('//*[@data-test-topcard-organizations-link] | //a[contains(@class, "topcard__org-name") or contains(@class, "ember-view")]')
            if org_el:
                company = org_el[0].text_content().strip()

    if not location:
        full_text = " ".join(tree.xpath('//text()'))
        m = re.search(r"\b[\w\-\. ]+,\s*[A-Za-z]{2,}\b", full_text)
        if m:
            location = m.group(0).strip()

    # 3) Description fallback: use trafilatura extract which is resilient
    if not description:
        try:
            extracted = trafilatura.extract(html, include_tables=False, include_comments=False)
        except Exception:
            extracted = None
        description = _clean_text(extracted or "")

    # Final assembly
    parts = []
    if title:
        parts.append(f"Title: {title.strip()}")
    if company:
        parts.append(f"Company: {company.strip()}")
    if location:
        parts.append(f"Location: {location.strip()}")
    if description:
        parts.append("\nDescription:\n" + description.strip())

    result = "\n".join(parts).strip()

    # Heuristic: if the page looked like a LinkedIn login gate, warn in the returned text
    login_text_snippets = ["sign in", "join now", "see more jobs", "linkedin"]
    lower_html = html[:2000].lower()
    if any(sn in lower_html for sn in login_text_snippets) and (not description or len(description) < 200):
        result += "\n\n[Note] The page may be behind LinkedIn's login gate; results are best-effort."

    return result
