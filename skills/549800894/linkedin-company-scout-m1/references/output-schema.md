# Output Schema

Use this schema for every collected company row.

## Required Fields

| field | requirement | notes |
| --- | --- | --- |
| `keyword` | required | Original keyword that produced the company |
| `company_name` | required | Public company name |
| `company_website` | required | Official website URL when found |
| `company_intro` | required | Short company summary from LinkedIn or website |
| `industry` | required | Industry label from LinkedIn or official source |
| `location` | required | City, state, region, or country shown publicly |
| `linkedin_url` | required | Direct LinkedIn company page URL |
| `email` | required | Contact email if found, else blank |
| `email_source` | required | `official_website`, `google_maps`, or `not_found` |
| `notes` | optional | Missing-field reason, ambiguity note, or validation note |

## Preferred JSON Shape

```json
{
  "keyword": "industrial design",
  "company_name": "Example Studio",
  "company_website": "https://example.com",
  "company_intro": "Industrial design consultancy focused on consumer electronics and wearables.",
  "industry": "Design Services",
  "location": "San Francisco, California, United States",
  "linkedin_url": "https://www.linkedin.com/company/example-studio/",
  "email": "hello@example.com",
  "email_source": "official_website",
  "notes": ""
}
```

## Acceptance Checklist

- The company is relevant to the active keyword.
- The company is not located in China.
- The LinkedIn URL points to a company page.
- The website is an official company website, not a directory or social profile.
- The email source value matches the place where the email was actually found.
