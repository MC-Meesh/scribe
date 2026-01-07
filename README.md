# Scribe

Turn your git commits into engaging #buildinpublic tweets automatically using AI.

## What is Scribe?

Scribe analyzes your git commits and generates engaging tweets for the #buildinpublic community. Stop staring at a blank tweet box trying to summarize your day's work - let AI craft multiple options that highlight what you're building, why it matters, and what you learned.

**Not just a changelog.** Scribe generates tweets that:
- Lead with your product vision, not technical details
- Frame progress as user value and business impact
- Include learnings and next steps
- Sound authentic and human
- Are designed to get engagement on Twitter/X

## Features

- Analyzes git commits from any time range
- Generates multiple tweet options to choose from
- Supports different writing styles (technical, casual, celebratory)
- Can create tweet threads for detailed updates
- Works with DeepSeek or OpenAI
- Filter by author for team repos
- Easy to install and use

## Installation

### Option 1: Install with pip

```bash
git clone https://github.com/yourusername/scribe.git
cd scribe
pip install -e .
```

### Option 2: Just clone and run

```bash
git clone https://github.com/yourusername/scribe.git
cd scribe
pip install -r requirements.txt
python -m scribe.cli
```

## Setup

### 1. Get an API Key

**DeepSeek (Recommended):**
- Sign up at [https://platform.deepseek.com](https://platform.deepseek.com)
- Get your API key from the dashboard

**OpenAI (Optional):**
- Sign up at [https://platform.openai.com](https://platform.openai.com)
- Get your API key

### 2. Configure your API key

Create a `.env` file in your project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your key:

```
DEEPSEEK_API_KEY=your_key_here
```

Or create `~/.scriberc` for global configuration:

```bash
echo "DEEPSEEK_API_KEY=your_key_here" > ~/.scriberc
```

## Usage

### Basic Usage

Generate tweets from today's commits:

```bash
scribe
```

### Time Ranges

```bash
scribe --since "yesterday"
scribe --since "2 days ago"
scribe --since "3 hours ago"
scribe --since "2024-01-01"
```

### Different Styles

```bash
scribe --style technical      # Technical and precise
scribe --style casual         # Conversational and friendly
scribe --style celebratory    # Enthusiastic and positive
```

### Tweet Threads

For more detailed updates:

```bash
scribe --thread
```

### Filter by Author

For team repositories:

```bash
scribe --author "meesh"
```

### Use Different AI Providers

```bash
scribe --provider openai
```

### Analyze Different Repos

```bash
scribe --repo ~/projects/my-app
```

### Advanced Examples

```bash
# Casual tweets from last 3 days, filtered by author
scribe --since "3 days ago" --author "meesh" --style casual

# Generate 5 options instead of 3
scribe --options 5

# Thread about yesterday's work using OpenAI
scribe --since yesterday --thread --provider openai
```

## Example Output

### Before (boring changelog):
❌ "Updated styling across multiple pages and fixed config for Vercel deployment"

### After (engaging #buildinpublic tweet):
✅ "Building a platform to connect professionals with opportunities. Today: Polished the entire user journey - from landing page to contact forms. The details matter when you're building trust. Next: Deploying to Vercel for real-world testing. 🚀"

### Full Example:

```bash
$ scribe --style casual

🔍 Analyzing commits in .
✅ Found 3 commit(s)
   1. updating styling and address and other things
   2. fixed for vercel
   3. Initial commit from Create Next App

🤖 Generating tweets using deepseek...

📝 Tweet Options (casual style):

1. Building a tool to help people navigate complex services. Today: Polished the
   entire user journey - from landing page to contact forms. The details matter
   when you're building trust. Next: Making sure it's rock-solid for our first
   users on Vercel. 🚀

2. Day 2 of building in public: Just shipped a complete visual refresh and got
   our Next.js app ready for production on Vercel. The real win? Every page now
   tells a clearer story about what we offer. Learning: CSS is a journey, not
   a destination. ✨

3. We're creating a better way for people to access professional services. Big
   step today: Revamped all our public pages and solved our first deployment
   puzzle. Watching localhost go live never gets old. Next up: Preparing for
   real user feedback!

✨ Copy and paste your favorite!
```

## Configuration Options

### Environment Variables

- `DEEPSEEK_API_KEY` - Your DeepSeek API key
- `OPENAI_API_KEY` - Your OpenAI API key (optional)

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--repo` | Path to git repository | Current directory |
| `--since` | Time range for commits | "today" |
| `--author` | Filter by author name | None |
| `--style` | Tweet style (technical/casual/celebratory) | technical |
| `--options` | Number of tweet options | 3 |
| `--thread` | Generate tweet thread | False |
| `--provider` | AI provider (deepseek/openai) | deepseek |

## Tips for #buildinpublic Success

1. **Tell a story**: Scribe frames your work as a journey, not a changelog. The AI leads with what you're building and why it matters.

2. **Multiple options**: Always generates 3+ tweet options so you can pick the one that resonates most with your audience.

3. **Styles matter**:
   - `technical` - Best for developer audiences, includes specific details
   - `casual` - Great for broader audiences, more conversational
   - `celebratory` - Perfect for milestones and wins

4. **Use threads for big days**: When you've made significant progress, use `--thread` to tell a more complete story.

5. **Team repos**: Use `--author "yourname"` to filter just your commits in team repositories.

6. **Better commits = better tweets**: Write clear commit messages that describe what AND why. Scribe uses these to understand your work.

7. **Commit often**: More granular commits give Scribe better context about your progress.

## Troubleshooting

### "Not a git repository"
Make sure you're running scribe in a git repository, or use `--repo` to specify the path.

### "API key not found"
Make sure you've set `DEEPSEEK_API_KEY` in your `.env` file or `~/.scriberc`.

### "No commits found"
Try adjusting your `--since` parameter or check if you have commits in the specified time range.

## Contributing

Pull requests welcome! This is a fast-shipping project, so keep it simple and focused.

## License

MIT

## Credits

Built by Quaternion Studios
