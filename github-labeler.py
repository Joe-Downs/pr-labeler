#!/usr/bin/env python3

"""

The script applies a label and milestone in the form "Target: {branchName}. If
necessary, it removes labels and milestones in the same form, but NOT for the
target branch. For instance, if someone edited the target branch from v4.0.x to
v5.0.x

"""

import re
import os
import sys

from github import Github

# ==============================================================================

GITHUB_BASE_REF = os.environ.get('GITHUB_BASE_REF')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
PR_NUM = os.environ.get('PR_NUM')

# Sanity check
if (GITHUB_BASE_REF is None or
    GITHUB_TOKEN is None or
    GITHUB_REPOSITORY is None or
    PR_NUM is None):
    print("Error: this script is designed to run as a Github Action")
    exit(1)

# ==============================================================================

targetPrefix = "Target: "

# Given a pullRequest object and list of existing labels or milestones, the
# function checks which are currently on the pull request and if , removes any
# matching the form "Target: {branch}" (if {branch} is not the current target
# branch), and adds the correct label or milestone.
#
# Because the GH API automatically creates a label when applying it (if it
# doesn't exist), we try to get a label object to check if the label has been
# created before we add (and create) it ourselves.

def ensureLabels(pullRequest, repo):
    needsLabel = True
    targetLabel = f"{targetPrefix}{GITHUB_BASE_REF}"
    try:
        repo.get_label(targetLabel)
    except:
        print(f"Label '{targetLabel}' not found")
        return None
    for label in pullRequest.get_labels():
        if label.name.startswith(targetPrefix):
            if label.name == targetLabel:
                needsLabel = False
            else:
                print(f"Removing label '{label.name}'")
                pullRequest.remove_from_labels(label)
    if needsLabel:
        print(f"Adding label '{targetLabel}'")
        pullRequest.add_to_labels(targetLabel)
    return None

def ensureMilestones(pullRequest, repo):
    targetVersion = re.search(r"v\d.\d.", GITHUB_BASE_REF).group(0)
    for milestone in repo.get_milestones(state="open"):
        if milestone.title.startswith(targetVersion):
            print(f"Setting milestone to '{milestone.title}'")
            pullRequest.edit(milestone=milestone)
    return None


# ==============================================================================

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)
prNum = int(PR_NUM)
pr = repo.get_pull(prNum)
issue = repo.get_issue(prNum)
ensureLabels(pr, repo)
ensureMilestones(issue, repo)
