import argparse
import commit_processing



def main():
    parser = argparse.ArgumentParser(description='CLI tool to share a quick standup message from you git commits and git diff')

    parser.add_argument('--days', type=int, help='How many days of history should be consider ?')
    #parser.add_argument('v',required=False, help='verborse flag will display the git commit hash, LLms raw response')


    args = parser.parse_args()
    data = commit_processing.get_git_commits(days=args.days)
    for commit in data:
        print(commit)



if __name__ == '__main__':
    main()









