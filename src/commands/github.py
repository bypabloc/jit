class GitHubController:
    def __init__(self, bot):
        self.bot = bot

    def execute(self, command):
        if command == "issues":
            return self.issues()
        elif command == "pulls":
            return self.pulls()
        elif command == "repos":
            return self.repos()
        elif command == "help":
            return self.help()
        else:
            return self.help()
