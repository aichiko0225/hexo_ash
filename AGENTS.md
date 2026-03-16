# AGENTS.md
Guidance for coding agents working in `/Users/ash/Desktop/Hexo/hexo_ash`.

## 1) Repository Overview
- Project type: Hexo blog/site.
- Root Hexo version: `8.1.1` from `package.json`.
- Theme: `themes/stellar` (`1.33.1`), tracked as a git submodule.
- Primary author-owned areas:
  - `source/` for posts, notes, and pages
  - `_config.yml`
  - `_config.stellar.yml`
- Generated or deployment-managed areas:
  - `public/`
  - `.deploy_git/`
- Root Python files are historical/experimental; ignore them unless a task explicitly targets them.

## 2) Working Priorities
- Prefer editing content and root config over modifying theme internals.
- Edit `themes/stellar/` only when the change cannot be achieved via Hexo config, Stellar config, content front matter, injected scripts, or CSS overrides.
- Avoid manual edits in generated output.
- Make minimal, localized changes; do not do repo-wide cleanup unless requested.

## 3) Package Manager And Commands
Run commands from the repository root unless noted.

Package manager rule:
- Use `yarn` for install and script execution.
- Do not switch to `npm` unless the user explicitly asks.

Root scripts:
```bash
yarn clean      # hexo clean
yarn build      # hexo generate
yarn server     # hexo server
yarn deploy     # hexo deploy
```

Typical local workflow:
```bash
yarn clean && yarn build
yarn server
```

Deployment note:
- `yarn deploy` uses the git deploy target configured in `_config.yml`.
- Treat deployment as a user-facing action; do not run it unless requested.

## 4) Linting And Tests
Current repo state:
- No root `lint` script exists.
- No ESLint, Prettier, Stylelint, or Markdownlint config was found.
- No root automated test runner exists.

Theme-only test command:
```bash
yarn --cwd themes/stellar test
```

Important caveat:
- The theme `test` script is currently `echo test`; it is not a real test suite.

### Running A Single Test
- There is no real single-test command in the current repo.
- If tests are added later, standardize on:
```bash
yarn test <file-or-pattern>
```
- Until then, validate changes with targeted builds and manual checks of affected pages/routes.

## 5) Minimum Validation Expectations
- Most content/config/doc changes: run `yarn build`.
- Theme template, JS, Stylus, or injected script changes: run `yarn build`, then `yarn server` and manually verify the affected page.
- Taxonomy or navigation changes: confirm categories, tags, menus, and generated URLs render correctly.
- Do not claim tests passed unless you actually ran a real test runner.

## 6) Repository Structure Notes
- `source/_posts/`: long-form blog posts.
- `source/notes/`: notebook/wiki-like notes.
- `source/about/`: about pages.
- `themes/stellar/layout/`: EJS templates.
- `themes/stellar/scripts/`: Hexo helpers, generators, filters, and commands.
- `themes/stellar/source/css/`: Stylus styles.

## 7) Front Matter And Content Conventions
Use YAML front matter with `---` delimiters.

Common fields:
- `title`
- `date`
- `updated`
- `categories`
- `tags`
- optional theme fields such as `banner`, `cover`, `rightbar`, `type`, `wiki`

Category policy for this repo:
- Categories stay in Chinese.
- Current stable categories are:
  - `技术`
  - `AI与工具`
  - `项目实践`
  - `阅读与思考`
  - `关于世界的一切`
  - `生活记录`
  - `跑步`

Tag policy for this repo:
- Tags should be English-only.
- Prefer concise, searchable topic tags such as `React`, `Python`, `Tooling`, `Workflow`, `Reading`, `Essay`.
- Avoid adding new Chinese tags unless the user explicitly requests an exception.

Markdown/content style:
- Keep headings ordered logically.
- Keep prose and lists readable; avoid unnecessary HTML if Markdown works.
- Preserve existing author voice in posts; do not flatten personal writing into generic documentation tone.
- For notes, keep content compact and reference-oriented.

## 8) JavaScript Style
Observed style in theme scripts:
- Plain JavaScript only; no TypeScript setup exists.
- Node-side scripts use CommonJS.
- Keep `'use strict';` in Node-side theme files.
- Use 2-space indentation.
- Prefer `const` and `let`.
- Use descriptive `camelCase` names for variables and functions.
- Keep helpers small and composable.
- Prefer straightforward logic over abstraction for one-off helpers.
- Follow the local file's semicolon and quote style; do not normalize entire files.

Imports/requires:
- Keep `require(...)` calls near the top.
- Group dependency imports before local imports.
- Avoid reorder-only diffs.

Error handling:
- Do not silently swallow important failures.
- Fail fast on invalid required config.
- Gracefully handle missing optional data.
- Log enough context to debug build/runtime issues when adding new logic.

## 9) EJS Template Style
- Follow existing Stellar patterns in `themes/stellar/layout/`.
- Compute local values first, then render partials/markup.
- Prefer explicit variable names over terse aliases.
- Reuse existing partials before creating new ones.
- Keep conditions readable; avoid deep nesting when possible.
- Do not reformat unrelated EJS blocks.

## 10) Stylus/CSS Style
- Follow the structure in `themes/stellar/source/css/`.
- Prefer customization via `themes/stellar/source/css/_custom.styl` or config-driven options before editing core theme styles.
- Keep selector naming and nesting aligned with nearby files.
- Avoid broad global overrides unless required by the task.
- For visual changes, verify both desktop and mobile rendering.

## 11) YAML And Config Style
- Use 2-space indentation.
- Preserve surrounding quoting style.
- Keep keys compatible with Hexo and Stellar expectations.
- Do not rename or remove config keys without verifying theme/plugin support.
- Be cautious with `_config.yml` and `_config.stellar.yml`; small mistakes can break the whole site.

## 12) Naming And Types
- JavaScript identifiers: `camelCase`.
- Markdown filenames: follow existing naming in the relevant folder.
- Do not introduce TypeScript syntax into `.js` files.
- If Python must be touched, keep it minimal and avoid broad modernization.

## 13) High-Risk Areas
- `themes/stellar/` is a submodule; upstream updates can overwrite local changes.
- `public/` is generated output; do not hand-edit it.
- `.deploy_git/` is deploy state; do not hand-edit it.
- Taxonomy, permalink, and menu changes can affect many generated pages.

## 14) Cursor / Copilot Rules Check
Checked locations:
- `.cursorrules`
- `.cursor/rules/`
- `.github/copilot-instructions.md`

Result at scan time:
- No Cursor or Copilot rule files were present in this repository.

If any of those files are added later, treat them as higher-priority instructions and merge them into this guide.

## 15) Recommended Agent Workflow
1. Read the relevant content, config, or theme files first.
2. Prefer the smallest change that solves the task.
3. Avoid touching the theme submodule unless necessary.
4. Run `yarn build` after meaningful changes.
5. For UI/theme changes, run `yarn server` and manually inspect affected pages.
6. Report exactly what changed, where it changed, and how it was validated.
