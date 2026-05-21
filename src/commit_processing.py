from datetime import timezone, datetime, timedelta

import git



def get_git_commits(days,all_repos = False):
    commits_list = []
    try:
        repo = git.Repo(search_parent_directories=True)

        # calculates date from which user want the data
        from_date = datetime.now(timezone.utc) - timedelta(days=days)

        for commit in repo.iter_commits("HEAD"):

            commit_date = datetime.fromtimestamp(commit.committed_date,timezone.utc)

            # for older than days our for days commits
            if commit_date < from_date:
                break

            commit_info = f"Commit: {commit.hexsha} | Message: {commit.message.strip()}"
            commits_list.append(commit_info)


        return commits_list


    except git.exc.InvalidGitRepositoryError:
        return None





