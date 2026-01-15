# Git from the Terminal — Practical Guide

A complete, terminal-first guide to using Git: repositories, branches, commits, undoing mistakes, syncing with remotes, and pull requests.

---

## Table of Contents

- Quick Setup
- Core Concepts
- Starting a Repository
- Daily Workflow
- Branching
- Committing
- Undoing & Fixing Mistakes
- Syncing with Remote (Push / Pull / Fetch)
- Pull Requests (PRs)
- Merging & Rebasing
- Stashing
- Tags & Releases
- Logs, Diffs & Inspection
- Useful Aliases
- Common “Oh No” Scenarios
- Quick Cheatsheet

---

## Quick Setup

Check Git installation:
git --version

Set your identity (one-time setup):
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

Set default branch name:
git config --global init.defaultBranch main

Optional helpful defaults:
git config --global pull.rebase false
git config --global fetch.prune true
git config --global rerere.enabled true

---

## Core Concepts

- Working directory: your actual files
- Staging area (index): files prepared for commit
- Commit: a snapshot of staged changes
- Branch: a pointer to a sequence of commits
- Remote: a server copy of the repository (often called "origin")

---

## Starting a Repository

Initialize a new repository:
git init

Clone an existing repository:
git clone https://github.com/ORG/REPO.git

Add a remote manually:
git remote add origin https://github.com/ORG/REPO.git
git remote -v

---

## Daily Workflow

Typical development loop:
git status
git pull
(edit files)
git add -A
git commit -m "Describe the change"
git push

---

## Branching

List branches:
git branch
git branch -r
git branch -a

Create and switch to a new branch:
git switch -c feature/my-change

Switch branches:
git switch main

Rename a branch:
git branch -m old-name new-name

Delete a local branch:
git branch -d feature/my-change
git branch -D feature/my-change

Delete a remote branch:
git push origin --delete feature/my-change

---

## Committing

Check status and changes:
git status
git diff
git diff --staged

Stage files:
git add file.txt
git add folder/
git add -A

Stage parts of a file interactively:
git add -p

Create a commit:
git commit -m "Add feature X"

Amend the last commit:
git add -A
git commit --amend

---

## Undoing & Fixing Mistakes

Unstage a file:
git restore --staged file.txt

Discard changes in a file (dangerous):
git restore file.txt

Discard all local changes (dangerous):
git restore .

Undo last commit but keep changes staged:
git reset --soft HEAD~1

Undo last commit and unstage changes:
git reset HEAD~1

Undo last commit and discard changes (dangerous):
git reset --hard HEAD~1

Safely undo a commit that was already shared:
git revert COMMIT_HASH

Recover lost commits:
git reflog
git switch -c recovery-branch COMMIT_HASH

---

## Syncing with Remote (Push / Pull / Fetch)

Fetch remote updates:
git fetch

Pull (fetch + merge):
git pull

Push current branch:
git push

Push new branch and set upstream:
git push -u origin feature/my-change

Clean up deleted remote branches:
git fetch --prune

View remotes:
git remote -v

---

## Pull Requests (PRs)

Typical PR workflow:
1. Create a branch
2. Commit your changes
3. Push the branch
4. Open a PR on GitHub/GitLab/Bitbucket

Example:
git switch -c feature/my-change
git add -A
git commit -m "Implement my change"
git push -u origin feature/my-change

(Optional, GitHub CLI)
gh pr create --fill
gh pr view --web

---

## Merging & Rebasing

Merge main into your branch:
git fetch origin
git merge origin/main

Rebase your branch onto main:
git fetch origin
git rebase origin/main

Continue rebase after fixing conflicts:
git add FILES
git rebase --continue

Abort a rebase:
git rebase --abort

Force push after rebase (safer option):
git push --force-with-lease

---

## Stashing

Stash changes:
git stash

Stash with a message:
git stash push -m "WIP work"

List stashes:
git stash list

Apply stash:
git stash apply

Apply and remove stash:
git stash pop

Drop a stash:
git stash drop stash@{0}

---

## Tags & Releases

Create a lightweight tag:
git tag v1.0.0

Create an annotated tag:
git tag -a v1.0.0 -m "Release 1.0.0"

Push a tag:
git push origin v1.0.0
git push origin --tags

---

## Logs, Diffs & Inspection

View log:
git log
git log --oneline --graph --decorate --all

Show a specific commit:
git show COMMIT_HASH

Diff between branches:
git diff main..feature/my-change

Blame a file:
git blame file.txt

---

## Useful Aliases

Create aliases:
git config --global alias.st status
git config --global alias.co switch
git config --global alias.br branch
git config --global alias.cm "commit -m"
git config --global alias.lg "log --oneline --graph --decorate --all"

Usage:
git st
git lg

---

## Common “Oh No” Scenarios

Committed to main by mistake:
git switch -c feature/oops
git switch main
git reset --hard HEAD~1

Safely undo shared commit:
git revert HEAD
git push

Branch behind main:
git fetch origin
git merge origin/main
or
git rebase origin/main

Undo last pushed commit (history rewrite):
git reset --hard HEAD~1
git push --force-with-lease

---

## Quick Cheatsheet

git status
git add -A
git commit -m "message"
git switch -c feature/name
git push -u origin feature/name
git pull
git fetch --prune
git log --oneline --graph --decorate --all
git revert COMMIT_HASH
git reset --soft HEAD~1
git reset --hard HEAD~1
