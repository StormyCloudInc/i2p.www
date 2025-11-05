#!/usr/bin/env python3
"""
Scrape research papers from https://geti2p.net/en/papers/
and convert to Hugo markdown format.
"""

import requests
from bs4 import BeautifulSoup
import re

def scrape_bibtex():
    """Scrape BibTeX entries from the bibtex page"""
    url = "https://geti2p.net/en/papers/bibtex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    bibtex_dict = {}

    # Find all BibTeX entries
    for pre in soup.find_all('pre', class_='bibtex'):
        # Get the anchor name from the preceding anchor tag
        anchor = pre.find_previous('a', {'name': True})
        if anchor:
            key = anchor['name']
            bibtex_text = pre.get_text().strip()
            bibtex_dict[key] = bibtex_text

    return bibtex_dict

def scrape_papers():
    url = "https://geti2p.net/en/papers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    papers_by_year = {}

    # Find all year sections
    for year_section in soup.find_all('h3'):
        year_link = year_section.find('a', {'name': True})
        if not year_link:
            continue

        year = year_link.get('name')
        if not re.match(r'^\d{4}$', year):
            continue

        papers_by_year[year] = []

        # Find the next ul element with class 'expand'
        ul_elem = year_section.find_next('ul', class_='expand')
        if not ul_elem:
            continue

        # Find all paper entries
        for entry in ul_elem.find_all('p', class_='entry'):
            paper = {}

            # Extract title
            title_span = entry.find('span', class_='title')
            if title_span:
                # Check if there's a link in the title span
                title_link = title_span.find('a', href=True, class_='title')
                if title_link and title_link['href'].startswith('http'):
                    paper['pdf_url'] = title_link['href']

                # Get the anchor tag with name attribute for bibtex key
                title_anchor = title_span.find('a', {'name': True})
                if title_anchor:
                    paper['bibtex_key'] = title_anchor['name']
                    paper['title'] = title_anchor.get_text().strip()
                else:
                    paper['title'] = title_span.get_text().strip()

            # Extract authors
            author_span = entry.find('span', class_='author')
            if author_span:
                author_text = author_span.get_text().strip()
                # Remove "by " prefix if present
                if author_text.startswith('by '):
                    author_text = author_text[3:]
                paper['authors'] = author_text.rstrip('.')

            # Extract venue
            biblio_span = entry.find('span', class_='biblio')
            if biblio_span:
                paper['venue'] = biblio_span.get_text().strip()

            # Check for PDF link in availability span
            avail_span = entry.find('span', class_='availability')
            if avail_span:
                pdf_link = avail_span.find('a', href=lambda x: x and not x.startswith('./bibtex'))
                if pdf_link:
                    paper['pdf_url'] = pdf_link['href']

            papers_by_year[year].append(paper)

    return papers_by_year

def generate_html_entry(paper, year, bibtex_dict):
    """Generate HTML entry for a paper"""
    title = paper.get('title', 'Untitled')
    authors = paper.get('authors', 'Unknown')
    venue = paper.get('venue', '')
    pdf_url = paper.get('pdf_url', '')
    bibtex_key = paper.get('bibtex_key', '')
    bibtex_content = bibtex_dict.get(bibtex_key, f'BibTeX key: {bibtex_key}')

    # Make title clickable if PDF exists
    if pdf_url:
        title_html = f'<a href="{pdf_url}" target="_blank">{title}</a>'
        pdf_button = f'''<a href="{pdf_url}" target="_blank" class="paper-link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke-width="2"/>
                <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" stroke-width="2"/>
            </svg>
            PDF
        </a>'''
    else:
        title_html = f'<span class="no-link">{title}</span>'
        pdf_button = ''

    # Clean up authors and venue for data attributes
    authors_clean = re.sub(r'<[^>]+>', '', authors).strip()
    title_clean = re.sub(r'<[^>]+>', '', title).strip()

    html = f'''<div class="paper-entry" data-year="{year}" data-title="{title_clean}" data-authors="{authors_clean}">
    <div class="paper-title">{title_html}</div>
    <div class="paper-authors">{authors}</div>
    <div class="paper-venue">{venue}</div>
    <div class="paper-actions">
        {pdf_button}
        <div class="bibtex-wrapper">
            <button class="bibtex-toggle">Show BibTeX</button>
            <div class="bibtex-content">{bibtex_content}</div>
        </div>
    </div>
</div>
'''

    return html

def main():
    print("Fetching BibTeX entries...")
    bibtex_dict = scrape_bibtex()
    print(f"Found {len(bibtex_dict)} BibTeX entries")

    print("Fetching papers...")
    papers_by_year = scrape_papers()

    # Generate markdown content
    content = '''---
title: "Research Papers"
description: "Academic research and publications about I2P anonymity network"
layout: "papers"
type: "papers"
aliases:
  - /en/papers/
  - /papers/
---

'''

    # Sort years in reverse order (newest first)
    for year in sorted(papers_by_year.keys(), reverse=True):
        papers = papers_by_year[year]
        if not papers:
            continue

        content += f'\n<h2 class="paper-year" data-year="{year}">{year}</h2>\n'

        for paper in papers:
            content += generate_html_entry(paper, year, bibtex_dict)

    # Write to file
    output_path = '/Users/dustinfields/git/i-2-p-www-v-2/hugo-site/content/en/papers.html'
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Generated papers.html with {sum(len(p) for p in papers_by_year.values())} papers")
    for year in sorted(papers_by_year.keys(), reverse=True):
        print(f"  {year}: {len(papers_by_year[year])} papers")

if __name__ == '__main__':
    main()
