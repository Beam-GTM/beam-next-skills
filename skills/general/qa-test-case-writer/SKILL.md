---
name: qa-test-case-writer
version: '1.0'
description: Comprehensive UI test case generation for QA teams. Use when the user
  wants to write test cases for a feature, project, or webpage. Generates happy flow,
  edge cases, and security test cases for client-facing UI (not API tests). Creates
  test cases in Notion databases following standardized format with Test Case ID,
  Title, Pre-condition, Test Steps, Expected Result, Test Data, Post-condition, Priority
  (P0-P3), and status tracking. Triggers on requests like "write test cases for [feature]",
  "create QA tests", "generate test scenarios", or when user provides feature documentation
  to test.
author: Ahsun Iqbal
category: general
tags:
- api
- notion
platform: Notion
updated: '2026-01-20'
visibility: team
---
# QA Test Case Writer

Generate comprehensive UI test cases for client-facing web applications and push them to Notion databases.

## Workflow

### Step 1: Gather Feature Information

Obtain complete feature details from the user through one of these methods:

1. **Direct prompt**: User explains the feature in conversation
2. **File upload**: User provides documentation (PRD, specs, design docs)
3. **URL reference**: User shares links to documentation

If information is incomplete, ask clarifying questions about:
- User flows and interactions
- Input fields and validation rules
- Expected behaviors and error states
- Authentication/authorization requirements
- Edge cases the user is aware of

### Step 2: Determine Test Case ID Prefix

Ask user for:
1. **Feature/Module name** for the test case prefix (e.g., "SI" for Sign In, "WS" for Workspace)
2. **Notion page URL** where test cases should be created

If user provides a Notion URL, fetch the existing database to:
- Understand the existing test case ID pattern
- Check for any existing test cases to avoid duplicates
- Verify the database schema matches expected format

### Step 3: Generate Test Cases

Create test cases covering these categories:

#### Happy Flow (P0-P1)
- Primary user journey completing successfully
- All valid inputs producing expected outputs
- Standard use cases working as designed

#### Edge Cases (P1-P2)
- Boundary values (min/max lengths, empty inputs)
- Special characters and unicode
- Concurrent actions
- Session handling (timeout, multiple tabs)
- Browser back/forward navigation
- Network interruptions during actions

#### Security Test Cases (P0-P1)
- SQL injection attempts in input fields
- XSS (Cross-Site Scripting) prevention
- CSRF token validation
- Authentication bypass attempts
- Authorization boundary testing
- Session fixation/hijacking prevention
- Sensitive data exposure in UI/console

#### Negative Test Cases (P1-P2)
- Invalid inputs and error handling
- Missing required fields
- Incorrect data formats
- Unauthorized access attempts

### Step 4: Format Test Cases

Each test case must follow this exact schema:

| Field | Description | Example |
|-------|-------------|---------|
| Test Case ID | Prefix + sequential number | SI-001, WS-015 |
| Test Case Title | Brief descriptive title | Valid login with correct credentials |
| Pre-Condition | Required state before test | User exists with verified email |
| Test Steps | Numbered steps to execute | 1) Enter email → Next 2) Enter password → Submit |
| Expected Result | What should happen | Login success → Redirect to dashboard |
| Test Data | Specific data for the test | Email: user@company.com, Pass: ValidPass@123 |
| Post Condition | State after test completes | Session active, user logged in |
| Priority | P0 (Critical) to P3 (Low) | P0 |

#### Priority Guidelines

- **P0 (Critical)**: Core functionality, security vulnerabilities, data integrity
- **P1 (High)**: Important features, major user flows, significant edge cases
- **P2 (Medium)**: Secondary features, minor edge cases, UI/UX issues
- **P3 (Low)**: Nice-to-have validations, cosmetic checks

### Step 5: Create in Notion

Use the existing Test Case Template to create test case pages efficiently.

#### Template Information
- **Template Page URL**: `https://www.notion.so/2d92cadfbbbc80659271c50ea2d52415`
- **Template Data Source**: `collection://2d92cadf-bbbc-80a5-b179-000b911e5f5e`

#### Option A: Add to Existing Feature Page (Preferred)

If user provides an existing feature page URL with an inline database:

1. **Fetch the target page** to get the inline database data source:
   ```
   Notion:notion-fetch with the page URL
   ```

2. **Get the data source URL** from the inline database (look for `data-source-url` in the response)

3. **Create test case pages** using `Notion:notion-create-pages`:
   ```json
   {
     "parent": {"data_source_id": "<data-source-id-from-step-2>"},
     "pages": [
       {
         "properties": {
           "Test Case ID": "SI-001",
           "Test Case Title": "Valid login with correct credentials",
           "Pre-Condition": "User exists with verified email",
           "Test Steps": "1) Enter whitelisted email → Next 2) Enter correct password → Submit",
           "Expected Result": "Login success → Redirect to workspace/onboarding",
           "Test Data": "Email: user@company.com, Pass: ValidPass@123",
           "Post Condition": "Session active",
           "Priority": "P0"
         }
       }
     ]
   }
   ```

#### Option B: Create New Feature Page from Template

If user needs a new feature page for test cases:

1. **Duplicate the template page** using `Notion:notion-duplicate-page`:
   ```json
   {
     "page_id": "2d92cadfbbbc80659271c50ea2d52415"
   }
   ```

2. **Rename the duplicated page** using `Notion:notion-update-page` with the feature name

3. **Fetch the new page** to get its inline database data source URL

4. **Create test case pages** in the new database using `Notion:notion-create-pages`

#### Database Schema (Exact Property Names)

| Property | Type | Values |
|----------|------|--------|
| Test Case ID | title | e.g., "SI-001" |
| Test Case Title | text | Descriptive title |
| Pre-Condition | text | Required state before test |
| Test Steps | text | Numbered steps |
| Expected Result | text | What should happen |
| Test Data | text | Specific test data |
| Post Condition | text | State after test |
| Priority | select | P0, P1, P2, P3 |
| Status by Dev | status | Not started, Failed, Passed |
| Status by QA | status | Not started, Failed, Passed |

**Important**: 
- Use exact property names: "Pre-Condition" (with hyphen, capital C), "Post Condition" (space, capital C)
- Status fields default to "Not started" - no need to set them
- Create test cases in batches of 10-20 to avoid timeouts

## Test Case Writing Guidelines

### Test Steps Format
- Use numbered steps: 1) Action → Result 2) Action → Result
- Use arrows (→) to show flow between action and immediate result
- Keep steps atomic and verifiable
- Include UI element identifiers when helpful

### Test Data Examples
- Use realistic but clearly test data: `test@company.com`, `ValidPass@123`
- For sensitive data: use placeholders like `[valid_token]`, `[user_email]`
- Include both valid and invalid examples as needed

### Security Test Patterns

Reference `references/security-tests.md` for common security test patterns including:
- SQL injection payloads
- XSS vectors
- Authentication bypass techniques

### Common UI Test Scenarios

Reference `references/ui-test-patterns.md` for:
- Form validation patterns
- Navigation flow tests
- Session management tests
- Accessibility considerations

## Example Output

For a "Password Reset" feature, generate test cases like:

| ID | Title | Pre-Condition | Test Steps | Expected Result | Test Data | Post Condition | Priority |
|----|-------|---------------|------------|-----------------|-----------|----------------|----------|
| PR-001 | Valid password reset request | User exists with verified email | 1) Click "Forgot Password" 2) Enter registered email → Submit | Success message shown, reset email sent | Email: user@company.com | Reset token generated | P0 |
| PR-002 | Reset with invalid email format | None | 1) Click "Forgot Password" 2) Enter invalid email → Submit | Validation error: "Invalid email format" | Email: invalid-email | No email sent | P1 |
| PR-003 | SQL injection in email field | None | 1) Enter malicious input in email field → Submit | Input sanitized, appropriate error shown | Email: test@company.com' OR 1=1-- | No bypass, no data leak | P0 |