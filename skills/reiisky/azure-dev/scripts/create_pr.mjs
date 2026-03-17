import { parseArgs } from 'node:util';

const args = process.argv.slice(2);

const options = {
  org: { type: 'string' },
  project: { type: 'string' },
  repo: { type: 'string' },
  pat: { type: 'string' },
  source: { type: 'string' },
  target: { type: 'string' },
  title: { type: 'string' },
  description: { type: 'string', default: '' },
  draft: { type: 'boolean', default: false },
};

const { values } = parseArgs({ args, options });

const org = values.org || process.env.AZURE_DEVOPS_ORG;
const project = values.project || process.env.AZURE_DEVOPS_PROJECT;
const repo = values.repo || process.env.AZURE_DEVOPS_REPO;
const pat = values.pat || process.env.AZURE_DEVOPS_PAT;
const source = values.source;
const target = values.target;
const title = values.title;
const description = values.description;
const draft = values.draft;

if (!org || !project || !repo || !pat || !source || !target || !title) {
  console.error("Missing required arguments. Need org, project, repo, pat, source, target, and title.");
  console.error("Usage: node create_pr.mjs --org <org> --project <project> --repo <repo> --pat <pat> --source <source_branch> --target <target_branch> --title <title> [--description <desc>] [--draft]");
  process.exit(1);
}

const formatRef = (ref) => ref.startsWith('refs/') ? ref : `refs/heads/${ref}`;

const payload = {
  sourceRefName: formatRef(source),
  targetRefName: formatRef(target),
  title: title,
  description: description,
  isDraft: draft
};

const url = `https://dev.azure.com/${org}/${project}/_apis/git/repositories/${repo}/pullrequests?api-version=7.1`;
const auth = Buffer.from(`:${pat}`).toString('base64');

async function createPR() {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${auth}`
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      console.error(`Error creating PR: ${response.status} ${response.statusText}`);
      if (data && Object.keys(data).length > 0) {
        console.error(JSON.stringify(data, null, 2));
      }
      process.exit(1);
    }

    console.log(`✅ Successfully created PR #${data.pullRequestId}`);
    console.log(`URL: ${data.repository.webUrl}/pullrequest/${data.pullRequestId}`);
    console.log(`Title: ${data.title}`);
    console.log(`Status: ${data.status}`);
  } catch (error) {
    console.error("Failed to make request:", error);
    process.exit(1);
  }
}

createPR();
