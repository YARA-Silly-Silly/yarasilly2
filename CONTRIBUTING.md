# Contributing

YaraSilly2 is a GPL GNU3 Licensed project and uses the standard GitHub pull requests process to review and accept contributions.

There are several areas of **YaraSilly2** that you could help the project to contribute. This is just in the initial state of the project and together **WE** can make it large.

You don't have to be a developer to contribute to this project, you can be a **security researcher**, **malware analyst**, **coder** or anyone who are interested in this project can contribute by sharing **feature enhancement ideas**, **code quality enhancement**, **adding test cases**, **adding new features** etc.

- If you are a first-time contributor, please see [Steps to Contribute](#steps-to-contribute).
- If you would like to suggest features to be added to **YaraSilly2**, please go ahead and [create a new issue](https://github.com/YARA-Silly-Silly/yarasilly2/issues/new) describing your requirement and why you think that it will be need on this project.
- If you would like to work on something more involved, please connect with us.
- If you would like to make code contributions, all your commits should be signed with **Developer Certificate of Origin**. See [Sign your work](#sign-your-work).

## Steps to Contribute

**Python3 is required.**

0. Clone the git repository and enter into the folder

```
git clone https://github.com/YARA-Silly-Silly/yarasilly2.git
cd yarasilly2
```

1. Create and activate a virtual environment:

`Linux`

```
python -m venv venv
source venv/bin/activate
```

`Windows`

```
python -m venv venv
.\venv\Scripts\activate.bat
```

2. Install **ssdeep** according to your **OS** from

[https://python-ssdeep.readthedocs.io/en/latest/installation.html#installation](https://python-ssdeep.readthedocs.io/en/latest/installation.html#installation)

**Example Ubuntu 20.04**

```
sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip libfuzzy-dev
```

3. Install the package inside the environment:

```
pip3 install -r requirements.txt
```

4. Create a new branch `git checkout -b MY_BRANCH_NAME`

- Find an issue to work on or create a new issue. The issues are maintained at [YARA-Silly-Silly/yarasilly2](https://github.com/YARA-Silly-Silly/yarasilly2/issues). You can pick up from a list of [good-first-issues](https://github.com/YARA-Silly-Silly/yarasilly2/good%20first%20issue).
- Claim your issue by commenting your intent to work on it to avoid duplication of efforts.
- Fork the repository on **GitHub**.
- Create a branch from where you want to base your work (usually master).
- Make your changes.
- Commit your changes by making sure the commit messages convey the need and notes about the commit.
- Push your changes to the branch in your fork of the repository.
- Submit a pull request to the original repository. See [Pull Request checklist](#pull-request-checklist)

## Pull Request Checklist

- Rebase to the current master branch before submitting your pull request.
- Commits should be as small as possible. Each commit should follow the checklist below:

  - Commit header (first line) should convey what changed
  - Commit body should include details such as why the changes are required and how the proposed changes
  - **DCO** Signed

## Sign your work

We use the **Developer Certificate of Origin** (**DCO**) as an additional safeguard for the **YaraSilly2** project. This is a well established and widely used mechanism to assure that contributors have confirmed their right to license their contribution under the project's license. Please add a line to every git commit message:

```
  Signed-off-by: Random Developer <random@developer.example.org>
```

Use your real name (sorry, no pseudonyms or anonymous contributions). The email id should match the email id provided in your **GitHub profile**.

If you set your `user.name` and `user.email` in **git config**, you can sign your commit automatically with `git commit -s`.

You can also use git [aliases](https://git-scm.com/book/tr/v2/Git-Basics-Git-Aliases) like `git config --global alias.ci 'commit -s'`. Now you can commit with `git ci` and the commit will be signed.
