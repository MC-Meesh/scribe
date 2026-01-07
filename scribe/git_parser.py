import git
from datetime import datetime, timedelta
from pathlib import Path


class GitParser:
    def __init__(self, repo_path="."):
        """Initialize parser with a git repository path"""
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a git repository: {repo_path}")

    def get_commits(self, since="today", author=None):
        """
        Get commits from the repository

        Args:
            since: Time range (e.g., "today", "yesterday", "2 days ago", "2024-01-01")
            author: Filter by author name (optional)

        Returns:
            List of commit objects with metadata
        """
        # Parse the since parameter
        if since == "today":
            since_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif since == "yesterday":
            since_date = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif "days ago" in since:
            days = int(since.split()[0])
            since_date = datetime.now() - timedelta(days=days)
        elif "hours ago" in since:
            hours = int(since.split()[0])
            since_date = datetime.now() - timedelta(hours=hours)
        else:
            # Try to parse as date
            try:
                since_date = datetime.fromisoformat(since)
            except ValueError:
                raise ValueError(f"Invalid since format: {since}")

        # Get commits
        commits = []
        for commit in self.repo.iter_commits(since=since_date.isoformat()):
            # Filter by author if specified
            if author and author.lower() not in commit.author.name.lower():
                continue

            commit_data = {
                "hash": commit.hexsha[:7],
                "message": commit.message.strip(),
                "author": commit.author.name,
                "email": commit.author.email,
                "date": commit.committed_datetime,
                "files_changed": [],
                "stats": {
                    "insertions": 0,
                    "deletions": 0,
                    "files": 0
                }
            }

            # Get file changes
            if commit.parents:
                diffs = commit.parents[0].diff(commit)
                for diff in diffs:
                    if diff.a_path:
                        commit_data["files_changed"].append(diff.a_path)
                    elif diff.b_path:
                        commit_data["files_changed"].append(diff.b_path)

                # Get stats
                stats = commit.stats.total
                commit_data["stats"]["insertions"] = stats.get("insertions", 0)
                commit_data["stats"]["deletions"] = stats.get("deletions", 0)
                commit_data["stats"]["files"] = stats.get("files", 0)

            commits.append(commit_data)

        return commits

    def _infer_project_context(self, commits):
        """Infer what kind of project this is from files and commits"""
        all_files = []
        for commit in commits:
            all_files.extend(commit['files_changed'])

        # Look for indicators
        context_clues = []

        # Framework detection
        if any('next.config' in f or 'app/page' in f or 'pages/' in f for f in all_files):
            context_clues.append("Next.js app")
        elif any('vite.config' in f for f in all_files):
            context_clues.append("Vite app")
        elif any('package.json' in f for f in all_files):
            context_clues.append("JavaScript/Node.js project")

        # Tech stack hints
        if any('.tsx' in f or '.jsx' in f for f in all_files):
            context_clues.append("React")
        if any('.vue' in f for f in all_files):
            context_clues.append("Vue")
        if any('.svelte' in f for f in all_files):
            context_clues.append("Svelte")
        if any('tailwind' in f.lower() for f in all_files):
            context_clues.append("Tailwind CSS")

        # Deployment/infrastructure
        if any('vercel' in f.lower() for f in all_files):
            context_clues.append("Vercel deployment")
        if any('docker' in f.lower() for f in all_files):
            context_clues.append("Docker")

        # App type hints
        if any('auth' in f.lower() or 'login' in f.lower() for f in all_files):
            context_clues.append("authentication features")
        if any('api/' in f or 'routes/' in f for f in all_files):
            context_clues.append("API endpoints")
        if any('db' in f.lower() or 'database' in f.lower() or 'prisma' in f.lower() for f in all_files):
            context_clues.append("database layer")

        return context_clues

    def format_commits_for_ai(self, commits):
        """Format commits into a readable text for AI processing"""
        if not commits:
            return "No commits found for the specified time range."

        text_parts = []

        # Add project context
        context_clues = self._infer_project_context(commits)
        if context_clues:
            text_parts.append(f"PROJECT CONTEXT (inferred from files): {', '.join(context_clues)}\n")

        text_parts.append(f"COMMITS ({len(commits)} total):\n")

        for i, commit in enumerate(commits, 1):
            text_parts.append(f"\n{i}. Commit: {commit['message']}")
            text_parts.append(f"   Files changed: {commit['stats']['files']} (+{commit['stats']['insertions']} -{commit['stats']['deletions']})")

            if commit['files_changed']:
                # Group files by type for better context
                key_files = commit['files_changed'][:8]  # Show more files
                text_parts.append(f"   Modified: {', '.join(key_files)}")

        return "\n".join(text_parts)
