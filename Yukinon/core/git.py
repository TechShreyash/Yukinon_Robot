import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config

UPSTREAM_REPO = "https://github.com/TechShreyash/Yukinon_Robot"
UPSTREAM_BRANCH = "main"

def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(
        install_requirements()
    )


def git():
    REPO_LINK = UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = (
            f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
        )
    else:
        UPSTREAM_REPO = UPSTREAM_REPO
    try:
        repo = Repo()
        print(f"Git Client Found [VPS DEPLOYER]")
    except GitCommandError:
        print(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            UPSTREAM_BRANCH,
            origin.refs[UPSTREAM_BRANCH],
        )
        repo.heads[UPSTREAM_BRANCH].set_tracking_branch(
            origin.refs[UPSTREAM_BRANCH]
        )
        repo.heads[UPSTREAM_BRANCH].checkout(True)
        try:
            repo.create_remote("origin", UPSTREAM_REPO)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(UPSTREAM_BRANCH)
        try:
            nrs.pull(UPSTREAM_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -r requirements.txt")
        print(f"Fetched Updates from: {REPO_LINK}")
