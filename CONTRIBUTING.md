# Contributing guidelines

This document contains the basic information on what the different branches of
the project mean and what they are used for. Also, it covers the basic contributing
guidelines.

## Branching model

- The `main` branch contains the latest production version of the project. Normally,
this branch should not be tampered with unless there is some kind of problem.
- The `development` branch contains the latest changes. It is periodically merged
into the `main` branch (once a week).
- The `type/issue-XXX-description` are work in progress branches that will
be merged into `development` once they are finished.

## Rules for commit messages

1. Write meaningul commit messages using the present tense. For instance, if you
have created a new function that computes the sum of two numbers, your commit
message should look something like this: "Create a function that computes the
sum of two numbers".

## How to contribute

When you are assigned an issue or you assign it to yourself, you have to follow
a set of rules in order to correctly close it.

First, create a branch from the `development` branch following this pattern:
`type/issue-XXX-short-description`. The `type` part can be either
**feature** or **bug**.

Once you have your branch is created, move the associated issue to `In Progress`
in the Kanban and work locally on it. **Never** directly upload
files to the GitHub page. In order to create the branch, run the following command:

```
$ git checkout -b type/issue-XXX-description
```

In order create a branch on GitHub from your local branch and to track any change
on it, run the following command:

```
$ git push -u origin type/issue-XXX-description
```

Before creating a PR, merge the `development` branch into it so that it has the
latest changes. Solve the conflicts, if any, and upload the changes. You can also
rebase the branch with `development` so that you don't have merge commits. This last
strategy is a bit harder if your are not used to it, but it yields a cleaner
history. Keep in mind that if you do this, you will have to run a `git push -f`
**on your branch**, so that the history is rewritten.

When you have finished working on that issue, create a PR pointing at the
`development` branch and fill the template accordingly. Add as reviewers people
who you know that might have knowledge on that area and move the issue `In Review`
if it has not been moved automatically.

Once your PR is accepted and passed the tests (if there are any), it can be merged.
When it's merged, move the task to the `Done` column.

