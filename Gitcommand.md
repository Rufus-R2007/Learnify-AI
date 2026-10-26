# Git & GitHub Commands Cheat Sheet for VS Code

Use this as your personal reference while working on projects like Learnify AI. All commands below can be run in the VS Code Terminal using Git Bash, PowerShell, or Command Prompt, unless noted otherwise.

## 1. Basic Git terms

| Term              | Meaning                                                       |
| ----------------- | ------------------------------------------------------------- |
| `git`             | Tool used to track changes in your code                       |
| GitHub            | Website that hosts your Git repositories                      |
| Repository (repo) | Your project's tracked files and history                      |
| `main`            | The main branch of a project                                  |
| Branch            | A separate line of development                                |
| `origin`          | The conventional name for a remote repository, usually GitHub |
| Commit            | A saved snapshot of changes                                   |
| Push              | Upload your local commits to GitHub                           |
| Pull              | Fetch and integrate changes from GitHub                       |
| Clone             | Download a repository to your computer                        |
| Merge             | Combine changes from one branch into another                  |
| Pull Request (PR) | A request to review and merge changes on GitHub               |
| Staging           | Selecting which changes go into the next commit               |

## 2. Setup and identity

Configure your Git identity once on your computer.

| Command                                            | Purpose                                        |
| -------------------------------------------------- | ---------------------------------------------- |
| `git --version`                                    | Check whether Git is installed                 |
| `git config --global user.name "Your Name"`        | Set your Git commit name                       |
| `git config --global user.email "you@example.com"` | Set your Git commit email                      |
| `git config --global --list`                       | View global Git settings                       |
| `git config user.name`                             | Check the name used in the current repository  |
| `git config user.email`                            | Check the email used in the current repository |

Replace the example name and email with your own. Use the email associated with your GitHub account if you want commits linked to that account.

## 3. Create or download a repository

| Command                                   | Purpose                                 |
| ----------------------------------------- | --------------------------------------- |
| `git init`                                | Initialize Git in the current folder    |
| `git clone REPOSITORY_URL`                | Download a GitHub repository            |
| `git clone REPOSITORY_URL PROJECT_FOLDER` | Clone into a folder with a chosen name  |
| `cd PROJECT_FOLDER`                       | Enter a project folder                  |
| `cd ..`                                   | Move up one directory                   |
| `pwd`                                     | Show your current directory in Git Bash |
| `git status`                              | Check the current repository status     |

Example:

```
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
```

If the project already exists on GitHub, use `git clone` instead of `git init`.

## 4. Branch commands

Branches let you develop features without directly changing `main`.

| Command                     | Purpose                                    |
| --------------------------- | ------------------------------------------ |
| `git branch`                | List local branches                        |
| `git branch -a`             | List local and remote-tracking branches    |
| `git branch BRANCH_NAME`    | Create a branch                            |
| `git switch BRANCH_NAME`    | Switch to an existing branch               |
| `git switch -c BRANCH_NAME` | Create and switch to a new branch          |
| `git branch -m NEW_NAME`    | Rename the current branch                  |
| `git branch -d BRANCH_NAME` | Delete a merged local branch               |
| `git branch -D BRANCH_NAME` | Force-delete a local branch; use carefully |
| `git switch main`           | Switch to `main`                           |
| `git branch --show-current` | Show your current branch                   |

Example: create your own frontend branch

```
git switch main
git pull origin main
git switch -c feature/frontend-updates
```

This creates a branch called `feature/frontend-updates` based on the latest `main`.

## 5. Check changes and stage files

Git staging lets you choose exactly what you want to commit.

| Command                          | Purpose                                                             |
| -------------------------------- | ------------------------------------------------------------------- |
| `git status`                     | Show changed, staged, and untracked files                           |
| `git diff`                       | View unstaged changes                                               |
| `git diff --staged`              | View staged changes                                                 |
| `git add FILE_NAME`              | Stage one specific file                                             |
| `git add .`                      | Stage changes under the current directory                           |
| `git add -A`                     | Stage additions, modifications, and deletions across the repository |
| `git restore FILE_NAME`          | Discard unstaged changes in a file; use carefully                   |
| `git restore --staged FILE_NAME` | Unstage a file without discarding its changes                       |
| `git rm FILE_NAME`               | Remove a tracked file and stage its deletion                        |
| `git mv OLD_NAME NEW_NAME`       | Rename a tracked file                                               |

Example:

```
git status
git diff
git add src/styles/index.css
git diff --staged
```

Tip: Review `git status` before using `git add .`, especially if you have `.env` files, credentials, generated files, or unrelated changes.

## 6. Commit commands

A commit records your staged changes in the local repository.

| Command                               | Purpose                                                    |
| ------------------------------------- | ---------------------------------------------------------- |
| `git commit -m "MESSAGE"`             | Commit staged changes                                      |
| `git log`                             | View commit history                                        |
| `git log --oneline`                   | View compact commit history                                |
| `git log --oneline --graph --all`     | View branch and commit history graphically in the terminal |
| `git show`                            | Inspect the latest commit                                  |
| `git commit --amend -m "NEW MESSAGE"` | Change the latest commit message and/or contents           |
| `git revert COMMIT_ID`                | Create a new commit that reverses a previous commit        |

Example:

```
git add .
git commit -m "fix: resolve Tailwind CSS border-border compilation error"
```

Use clear commit prefixes when helpful:

| Prefix      | When to use                                          | Example                              |
| ----------- | ---------------------------------------------------- | ------------------------------------ |
| `feat:`     | New feature                                          | `feat: add student dashboard`        |
| `fix:`      | Bug fix                                              | `fix: resolve CSS compilation error` |
| `docs:`     | Documentation                                        | `docs: update setup instructions`    |
| `style:`    | Formatting or styling-only changes                   | `style: improve button spacing`      |
| `refactor:` | Code restructuring without intended behavior changes | `refactor: simplify login component` |
| `test:`     | Add or update tests                                  | `test: add login validation tests`   |
| `chore:`    | Maintenance tasks                                    | `chore: update development scripts`  |

## 7. Push and pull commands

These commands synchronize your local repository with GitHub.

| Command                                | Purpose                                                               |
| -------------------------------------- | --------------------------------------------------------------------- |
| `git remote -v`                        | Show configured remote URLs                                           |
| `git remote show origin`               | Show details about the `origin` remote                                |
| `git fetch origin`                     | Download remote updates without merging them                          |
| `git pull`                             | Pull from the current branch's configured upstream                    |
| `git pull origin main`                 | Pull and integrate changes from remote `main` into the current branch |
| `git push`                             | Push to the configured upstream branch                                |
| `git push origin BRANCH_NAME`          | Push a specific local branch to GitHub                                |
| `git push -u origin BRANCH_NAME`       | Push a branch and set its upstream tracking branch                    |
| `git push origin --delete BRANCH_NAME` | Delete a remote branch; use carefully                                 |

Important: `git pull origin main` integrates remote `main` into whichever branch you are currently on. To update your local `main`, switch to `main` first.

Example: push your new branch for the first time.

```
git push -u origin feature/frontend-updates
```

After setting the upstream, you can generally use `git push` and `git pull` while on that branch.

## 8. Understanding `main`, `origin`, and `origin/main`

| Name                              | What it means                                                              |
| --------------------------------- | -------------------------------------------------------------------------- |
| `main`                            | Your local main branch                                                     |
| `origin`                          | A nickname for the remote GitHub repository                                |
| `origin/main`                     | Your local reference to the latest `main` commit you fetched from `origin` |
| `origin/feature/frontend-updates` | Your local reference to the remote feature branch                          |
| `HEAD`                            | Indicates your current checkout; usually the current branch                |
| `HEAD~1`                          | The parent of the current commit, commonly the previous commit             |

Check your remote and branches:

```
git remote -v
git branch -a
git status
```

If you see `origin/main`, it does not necessarily mean it is up to date with GitHub right now. Run `git fetch origin` to refresh remote-tracking references.

## 9. Merge commands

Merge combines the changes from one branch into another.

| Command                           | Purpose                                                              |
| --------------------------------- | -------------------------------------------------------------------- |
| `git merge BRANCH_NAME`           | Merge another branch into your current branch                        |
| `git merge --abort`               | Abort a merge in progress when possible                              |
| `git diff main...BRANCH_NAME`     | Compare the branch's changes against its common ancestor with `main` |
| `git log --oneline --graph --all` | Inspect branch history                                               |

Example: merge your feature branch into your local `main`.

```
git switch main
git pull origin main
git merge feature/frontend-updates
git push origin main
```

Only push directly to `main` if your team allows it. In a collaborative project, the preferred approach is usually to create a Pull Request on GitHub, review it, and merge there.

## 10. Pull Request workflow (recommended for teams)

Step 1 — Create your branch

```
git switch main
git pull origin main
git switch -c fix/tailwind-error
```

Step 2 — Commit and push

```
git add .
git commit -m "fix: resolve Tailwind CSS error"
git push -u origin fix/tailwind-error
```

Step 3 — Create the PR

Open your repository on GitHub. Select Compare & pull request, then set:

- Base: `main`
- Compare: `fix/tailwind-error`

Step 4 — Review and merge

Test the changes, request your team's approval, resolve any conflicts, and merge once approved.

## 11. Undo and recovery commands

Use these carefully: some commands permanently discard work.

| Command                          | Purpose                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| `git restore FILE_NAME`          | Discard unstaged edits in a file                                                   |
| `git restore --staged FILE_NAME` | Remove a file from staging                                                         |
| `git reset --soft HEAD~1`        | Undo the latest commit but keep its changes staged                                 |
| `git reset HEAD~1`               | Move the branch back one commit and keep the changes in the working tree, unstaged |
| `git revert COMMIT_ID`           | Safely reverse a commit by creating a new commit                                   |
| `git stash`                      | Temporarily save tracked working changes                                           |
| `git stash -u`                   | Temporarily save tracked and untracked changes                                     |
| `git stash list`                 | List saved stashes                                                                 |
| `git stash pop`                  | Restore the latest stash and remove it from the stash list if successful           |
| `git stash apply`                | Restore the latest stash but keep it in the stash list                             |

Beginner tip: If you have already pushed a commit shared with your team, prefer `git revert` over rewriting shared history with `git reset` and force-push.

## 12. Handling merge conflicts

A conflict occurs when Git cannot automatically combine competing changes.

| Command / action                    | Purpose                                                        |
| ----------------------------------- | -------------------------------------------------------------- |
| `git status`                        | Identify conflicted files                                      |
| Open the conflicted file in VS Code | Review the conflicting sections                                |
| Accept Current Change               | Keep the version from your checked-out branch for that section |
| Accept Incoming Change              | Keep the version from the branch being merged for that section |
| Accept Both Changes                 | Keep both sections, then edit if needed                        |
| `git add FILE_NAME`                 | Mark the resolved file as resolved                             |
| `git commit`                        | Finish a merge if Git requires a merge commit                  |
| `git merge --abort`                 | Cancel the merge when possible                                 |

Don't blindly accept one side. Review the code and test the application after resolving conflicts.

## 13. `.gitignore` commands and common files

A `.gitignore` file tells Git which untracked files it should normally ignore.

| Item            | Common purpose                                   |
| --------------- | ------------------------------------------------ |
| `.gitignore`    | Defines files and folders to ignore              |
| `node_modules/` | JavaScript dependencies                          |
| `.env`          | Environment variables, which may contain secrets |
| `dist/`         | Common frontend build output                     |
| `__pycache__/`  | Python bytecode cache                            |
| `.venv/`        | Python virtual environment                       |

Example `.gitignore` for a React and Python project:

```
node_modules/
dist/
.env
.env.*
!.env.example
.venv/
__pycache__/
*.py[cod]
```

Adapt this to your repository. Keep an example environment file such as `.env.example` only if it contains safe placeholders and no real secrets.

Important: Adding a file to `.gitignore` does not automatically untrack it if it was already committed. To stop tracking a file while keeping it locally, use:

```
git rm --cached FILE_NAME
git commit -m "chore: stop tracking local configuration"
```

Never push passwords, API keys, tokens, or private credentials.

## 14. Handy Git commands

| Command                         | Purpose                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------ |
| `git status -sb`                | Compact status with branch information                                         |
| `git diff --stat`               | Summary of unstaged changes                                                    |
| `git diff --staged --stat`      | Summary of staged changes                                                      |
| `git remote -v`                 | Check where your repository pushes and fetches                                 |
| `git show COMMIT_ID`            | Inspect a specific commit                                                      |
| `git branch -vv`                | Show branches and their upstream tracking status                               |
| `git ls-files`                  | List files tracked by Git                                                      |
| `git check-ignore -v FILE_NAME` | Identify which ignore rule matches a file                                      |
| `git clean -n`                  | Preview removal of untracked files                                             |
| `git clean -fd`                 | Delete untracked files and directories; destructive, use only after previewing |

## 15. The five workflows to memorize first

Select a workflow to see the commands.

A. Save and upload my changes

B. Create a new branch

C. Update my branch with main

D. Download a GitHub project

E. Prepare my branch for a Pull Request

A. Save and upload my changes

```
git status
git add .
git commit -m "feat: describe your change"
git push
```

Use this when your branch already tracks its remote branch.

&#x20;Copy selected workflow

## 16. Quick rules to remember

- `git add` = choose changes.
- `git commit` = save changes locally.
- `git push` = upload commits to GitHub.
- `git fetch` = download remote updates without integrating them.
- `git pull` = fetch and integrate remote updates.
- `git switch` = change branches.
- `git merge` = combine branches.
- `origin` = the remote nickname, not a branch.
- Pull Request = review and merge proposal on GitHub.

For your learning folder, save this as `Git-GitHub-Cheat-Sheet.md`. You can also keep a small `practice-commands.txt` file and practice these commands in a test repository before using destructive commands in your actual project.