#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from .git_parser import GitParser
from .tweet_gen import TweetGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Scribe - Turn your git commits into tweets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  scribe                                    # Generate tweets from today's commits
  scribe --since "2 days ago"               # Commits from last 2 days
  scribe --style casual                     # Use casual tone
  scribe --author "meesh"                   # Filter by author
  scribe --repo ../other-project            # Analyze different repo
  scribe --thread                           # Generate a tweet thread
  scribe --provider openai                  # Use OpenAI instead of DeepSeek
        """
    )

    parser.add_argument(
        "--repo",
        default=".",
        help="Path to git repository (default: current directory)"
    )

    parser.add_argument(
        "--since",
        default="today",
        help='Time range for commits (default: "today"). Examples: "yesterday", "2 days ago", "3 hours ago", "2024-01-01"'
    )

    parser.add_argument(
        "--author",
        help="Filter commits by author name"
    )

    parser.add_argument(
        "--style",
        choices=["technical", "casual", "celebratory"],
        default="technical",
        help="Tweet style (default: technical)"
    )

    parser.add_argument(
        "--options",
        type=int,
        default=3,
        help="Number of tweet options to generate (default: 3)"
    )

    parser.add_argument(
        "--thread",
        action="store_true",
        help="Generate a tweet thread instead of single tweets"
    )

    parser.add_argument(
        "--provider",
        choices=["deepseek", "openai"],
        default="deepseek",
        help="AI provider to use (default: deepseek)"
    )

    args = parser.parse_args()

    try:
        # Parse git commits
        print(f"🔍 Analyzing commits in {args.repo}...")
        parser_obj = GitParser(args.repo)
        commits = parser_obj.get_commits(since=args.since, author=args.author)

        if not commits:
            print(f"\n❌ No commits found for the specified criteria.")
            print(f"   Time range: {args.since}")
            if args.author:
                print(f"   Author: {args.author}")
            print("\nTry adjusting your --since or --author parameters.")
            sys.exit(1)

        # Show commit summary
        print(f"\n✅ Found {len(commits)} commit(s)")
        for i, commit in enumerate(commits, 1):
            print(f"   {i}. {commit['message'][:60]}{'...' if len(commit['message']) > 60 else ''}")

        # Format for AI
        commits_text = parser_obj.format_commits_for_ai(commits)

        # Generate tweets
        print(f"\n🤖 Generating tweets using {args.provider}...")
        generator = TweetGenerator(provider=args.provider)

        if args.thread:
            tweets = generator.generate_thread(commits_text)
            print("\n📝 Tweet Thread:\n")
            for i, tweet in enumerate(tweets, 1):
                print(f"{i}. {tweet}")
                if i < len(tweets):
                    print()  # Empty line between tweets
        else:
            tweets = generator.generate_tweets(
                commits_text,
                style=args.style,
                num_options=args.options
            )
            print(f"\n📝 Tweet Options ({args.style} style):\n")
            for i, tweet in enumerate(tweets, 1):
                print(f"{i}. {tweet}\n")

        print("✨ Copy and paste your favorite!")

    except ValueError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
