---
description: Create a high-quality git commit from staged changes
---

# Create Good Commit

Generates a descriptive, well-structured commit message from staged changes, ensuring it meets quality standards. This is designed to be used in conjunction with (and typically after) `/review-changes`.

CRITICAL RULE: NEVER modify git state without explicit user approval. This includes but is not limited to: commits, checkout/merge/rebases/pulls, create/delete/rename branches, adding/removing remotes, (force) pushing to the remote.


CRITICAL RULE: NEVER perform any write action on GitHub without explicit user permission. This includes but is not limited to: submitting PR reviews, posting comments, creating/merging pull requests, pushing commits, creating branches, or creating issues. Always draft the content locally and present it to the user for review and approval BEFORE publishing anything to GitHub.

## When to Use

- When the user asks to "commit", "create a commit", "commit changes", or invokes `/create-commit`.
- After the user has reviewed and approved the output of `/review-changes` and wishes to finalize the changes in git.

## Steps

### 1. Verification of Staged Changes

First, verify what is currently staged for commit and review the changes:

```bash
// turbo
git status -s
```

```bash
// turbo
git diff --cached
```

- If **no changes are staged**, ask the user which files they would like to stage (e.g., `git add .` or specific files) before proceeding.
- If **changes are staged but there are also unstaged changes**, confirm with the user if they want to proceed with only the staged changes, or if they want to stage the remaining changes first.

### 2. Pre-Commit Check

- If `/review-changes` was not run prior to this, perform a quick sanity check on the staged diff:
  - Check for accidentally included files (like large binaries or `.env` files).
  - Check for placeholder text, debugging `print()` statements, or `TODO`s.
- If the diff looks suspicious, recommend the user run `/review-changes` first to ensure quality.

### 3. Draft the Commit Message

Analyze the `git diff --cached` and draft a high-quality commit message based on the following formatting rules:

**Commit Message Structure:**
1. **Subject Line**:
   - Use the **imperative, present tense** (e.g., "Add feature" not "Added feature" or "Adds feature").
   - Maximum of **50 characters**.
   - Capitalize the first letter.
   - Do not end with a period.
   - Use Conventional Commits formatting if it fits the project style (e.g., `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
2. **Blank Line**: Separate subject from body with a single blank line.
3. **Message Body** (Required for non-trivial changes):
   - Wrap text at **72 characters**.
   - Explain **why** the change was made and **what** problem it solves, rather than strictly detailing *how* the code changed (the diff shows the *how*).
   - Note any side effects or important architectural implications.

### 4. Present for User Approval

**CRITICAL**: NEVER commit without explicit user approval. 

Present the drafted commit message to the user cleanly:

```markdown
I have reviewed the staged changes. Here is the proposed commit message:

\`\`\`gitcommit
feat: Update OCR extraction prompt to exclude author names

Previously, the LLM was extracting author names along with the definitions.
This rule updates the global prompt to explicitly exclude any trailing author
attributions, ensuring cleaner bilingual sentence pairs.
\`\`\`

Would you like me to proceed with this commit, or do you want to make any adjustments?
```

### 5. Execute the Commit

Only **after** the user explicitly approves the drafted message, execute the commit. For multiline commit messages, it is safest to create a temporary file:

```bash
// turbo
cat << 'EOF' > .git/COMMIT_MSG_TMP
<subject line>

<message body>
EOF
git commit -F .git/COMMIT_MSG_TMP
rm .git/COMMIT_MSG_TMP
```