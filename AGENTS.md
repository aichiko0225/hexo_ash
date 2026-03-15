# AGENTS.md
Guidance for agents working in `/Users/ash/Desktop/Hexo/hexo_ash`.

## 1) Repository Snapshot
- Stack: Hexo `7.3.0` site.
- Theme: `themes/stellar` (git submodule from `xaoxuu/hexo-theme-stellar`).
- This is primarily a blog project; treat root Python files as historical/experimental unless a task explicitly targets them.
- Author-owned work is mainly in:
  - `source/` (posts/pages)
  - `_config.yml`
  - `_config.stellar.yml`
- Generated/deploy artifacts:
  - `public/` (generated)
  - `.deploy_git/` (deploy state)

Working rule:
- Prefer root config/content edits over theme internals.
- Edit `themes/stellar/` only when config/override cannot solve the task.

## 2) Build, Run, Lint, Test
Run from repository root unless noted.

Package manager rule:
- Use `yarn` for dependency and script management in this repo.
- Do not use `npm` commands for install/run workflows unless explicitly requested.

### 2.1 Build and local preview
```bash
yarn clean      # hexo clean
yarn build      # hexo generate
yarn server     # hexo server
yarn deploy     # hexo deploy
```

Deployment note:
- Root `_config.yml` is configured to deploy via git to the memoirs repository (see deploy config around `_config.yml:105`).

Common flow:
```bash
yarn clean && yarn build
yarn server
```

### 2.2 Linting status
- No root `lint` script found.
- No ESLint/Prettier/Stylelint/Markdownlint config found.
- Do not assume lint tooling exists.

### 2.3 Tests status
- Root project has no automated test script.
- Theme has a smoke command only:
```bash
yarn --cwd themes/stellar test
```
- Current theme test script is `echo test` (not a real test suite).

### 2.4 Running a single test (important)
Current state:
- No test runner is configured, so there is no true single-test command.

If tests are introduced later, standardize on:
```bash
yarn test <file-or-pattern>
```

Until then, validate by targeted rebuild/manual checks of affected routes.

## 3) Minimum Validation by Change Type
- Most edits: `yarn build`.
- Template/JS/CSS/theme behavior edits: `yarn server` and open affected pages.
- Config/content edits: verify front matter parses and generated links/pages render.
- Avoid claiming "tests passed" unless a real test runner was executed.

## 4) Code Style and Conventions
Follow existing file-local style; avoid reformat-only churn.

### 4.1 JavaScript (theme scripts + browser JS)
- Node-side theme scripts use CommonJS (`require`, `module.exports`).
- Keep `'use strict'` at top of Node-side script files.
- Indent with 2 spaces.
- Prefer `const`/`let`; avoid introducing new `var` unless matching nearby code.
- Use descriptive `camelCase` naming for vars/functions.
- Keep helpers small and composable.
- Use optional chaining where source data may be absent.
- Prefer `===`/`!==` for new logic unless loose checks are intentional.
- Follow local string/semicolon convention per file; do not normalize whole files.

### 4.2 Import / require organization
- Keep `require(...)` declarations near file top.
- Group builtin/dependency imports before local utilities.
- Keep import order stable; avoid cosmetic reorder-only diffs.

### 4.3 EJS templates
- Existing pattern is: compute local vars, then assemble output/partials.
- Prefer explicit template variable names (`page_type`, `article_type`, etc.).
- Reuse existing partials in `themes/stellar/layout/_partial/`.
- Keep conditionals readable; avoid deep nesting when possible.

### 4.4 Stylus / CSS
- Follow Stylus layout in `themes/stellar/source/css/`.
- Prefer config variable/customization via `_custom.styl` first.
- Keep selector naming and nesting consistent with nearby files.
- Avoid broad, global selector changes unless required.

### 4.5 YAML configs
- Use 2-space indentation.
- Keep key names compatible with Hexo/Stellar expectations.
- Do not rename existing keys without confirming theme support.
- Preserve quoting style used in surrounding config.

### 4.6 Markdown content
- Use YAML front matter (`---`) at top.
- Common fields: `title`, `date`, `tags`, `categories`.
- Keep heading levels ordered (`##` before `###`).
- Keep lists and links clean/readable.

### 4.7 Non-blog experimental scripts
- Root Python scripts are non-core for this blog and can usually be ignored.
- Do not change Python files unless the task explicitly requests it.

### 4.8 Types and language boundaries
- JS codebase is plain JavaScript (no TypeScript setup detected).
- Do not add TS syntax to `.js` files.
- If Python is touched, type hints are optional and should be minimal.

### 4.9 Error handling
- Never silently swallow exceptions.
- Log enough context to debug failures.
- Fail fast for invalid critical config.
- Gracefully degrade when optional data is missing.

## 5) High-Risk Areas / Hygiene
- `themes/stellar/` is a submodule; upstream sync can overwrite local edits.
- `public/` is generated output; avoid manual editing.
- `.deploy_git/` is deployment state; avoid manual editing.
- Root `_config.yml` and `_config.stellar.yml` can impact the full site.

## 6) Cursor / Copilot Rules Check
Checked:
- `.cursorrules`
- `.cursor/rules/`
- `.github/copilot-instructions.md`

Result:
- No Cursor or Copilot rule files found at scan time.

If these files are added later, merge their guidance into this file and treat them as higher-priority instructions.

## 7) Recommended Agent Workflow
1. Read relevant config/content/theme files before editing.
2. Make minimal localized changes.
3. Run `yarn build`.
4. For UI/template changes, run `yarn server` and verify pages manually.
5. Report exactly what changed and how it was validated.
