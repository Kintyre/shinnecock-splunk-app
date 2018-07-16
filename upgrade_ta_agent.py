#!/usr/bin/env python

import sys
import os
import re
import shutil
from subprocess import call, Popen, PIPE
from io import open

PKG="kintyre-speedtest-agent"
TARGET = os.path.join("kintyre-speedtest-TA", "bin", "lib")
REQUIREMENTS = os.path.join(TARGET, "requirements.txt")

try:
    # Python 3.3+
    from shlex import quote
except ImportError:
    quote = repr


def RUN(cmd, mode, *args, **kwargs):
    print("RUN {!r}".format(" ".join([quote(a) for a in cmd])))
    proc = Popen(cmd, *args, **kwargs)
    if mode == "call":
        return proc.wait()
    elif mode == "check":
        if proc.wait():
            raise CalledProcessError("{} exited with error code {}".format(cmd[0], proc.returncode))
    elif mode == "proc":
        return proc


def abort_on_git_change():
    if RUN(["git", "diff-index", "--quiet", "HEAD", "--"], "call"):
        print("Local changes detected.   Aborting script!\n")
        # Show the user what changed
        RUN(["git", "status"], "call")
        sys.exit(1)


def pip_install(packages):
    # Use '--no-deps' here because we don't want to install the request library (with all
    # depenencies).  The TA version of the agent dumps output to standard out not HEC and there's
    # no need for external conf files for interactive use case several libraries are unnecessary.
    cmd = ["pip", "install", "--upgrade", "--no-deps", "--target", TARGET ] + packages
    proc = RUN(cmd, "proc", stdout=PIPE)
    (stdout, __) = proc.communicate()
    stdout = stdout.decode("utf-8")
    print(stdout)
    if proc.returncode != 0:
        return False
    # Example 'pip install' output:
    #   ...
    #   Installing collected packages: kintyre-speedtest-agent, speedtest-cli, ifcfg
    #   Successfully installed ifcfg-0.17 kintyre-speedtest-agent-0.3.6 speedtest-cli-2.0.2
    mo = re.search(r"Successfully installed ([^\r\n]+)", stdout)
    if not mo:
        raise ValueError("Unknown output format.")
    packages = mo.group(1)
    print("DEBUG:  Found package info:  {}".format(packages))
    for mo in re.finditer(r"\b(?P<package>[a-zA-Z][a-z0-9_-]+)"
                          r"-(?P<version>[0-9]+\.[0-9]+[^ ]+)\b", packages):
        yield mo.groupdict()


def write_requirements(packages):
    with open(REQUIREMENTS, "w", encoding="utf-8") as req:
        req.write("# Requirements file for {}\n\n".format(PKG))
        for pkg in packages:
            req.write("{package}=={version}\n".format(**pkg))
    print("Wrote requirements file:  {}".format(REQUIREMENTS))


def git_commit(packages):
    pkgs = { d["package"] : d["version"] for d in packages }

    commit_subject = "Upgrade {} to {}".format(PKG, pkgs[PKG])
    commit_body = "Installed latest supporting python packages from PyPI.  Packages:"
    commit_message = commit_subject + "\n\n" + commit_body + "\n\n"
    for package in packages:
        commit_message +="     {package} ({version})\n".format(**package)
    RUN(["git", "add", TARGET], "check")
    print("Commit message: \n{}".format(commit_message))
    env = dict(os.environ)
    #env["SKIP"] = "trailing-whitespace,end-of-file-fixer"
    proc = RUN(["git", "commit", "-m", commit_message, "--no-verify"], "proc",
                 env=env )
    print("Return code: {}".format(proc.wait()))


def main():
    abort_on_git_change()
    shutil.rmtree(TARGET)
    pkgs = list(pip_install([ PKG, "ifcfg", "speedtest-cli"]))
    write_requirements(pkgs)
    git_commit(pkgs)



if __name__ == "__main__":
    main()
