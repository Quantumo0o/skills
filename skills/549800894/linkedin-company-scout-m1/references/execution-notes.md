# Execution Notes

Use these notes when you need the bundled script to run successfully rather than just describing the workflow.

## Preconditions

- macOS with the normal Google Chrome app installed at `/Applications/Google Chrome.app`
- Python 3 with `selenium` available
- Network access to LinkedIn, the target websites, and Google Maps
- A LinkedIn account that can access company search results

## Script Behavior

- The script starts or reuses Google Chrome with a remote debugging port.
- Selenium attaches to that Chrome session instead of using a headless browser.
- The script visits LinkedIn company search pages, opens company pages, fetches website pages over HTTP, and uses Google Maps only as an email fallback.
- Website email discovery is best-effort. It checks the homepage plus a small set of likely contact pages.
- On exit, the script stops the ChromeDriver service instead of intentionally closing the Chrome app.

## Important Limits

- LinkedIn page structure changes often, so selectors may need maintenance.
- Google Maps rarely exposes email directly; fallback success will vary by listing.
- If Chrome is already running without a debugging port, the script may need to start a debuggable Chrome session before Selenium can attach.
- The first Selenium attachment may trigger a ChromeDriver download through Selenium Manager.

## Maintenance Targets

When the script stops extracting fields correctly, inspect these stages first:

- LinkedIn search result extraction in `linkedin_company_search`
- LinkedIn company field extraction in `parse_linkedin_company_page`
- Website email extraction in `find_email_on_website`
- Google Maps fallback in `search_google_maps_for_email`
