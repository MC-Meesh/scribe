from openai import OpenAI
from .config import get_api_key, get_base_url, get_model


class TweetGenerator:
    def __init__(self, provider="deepseek"):
        """Initialize tweet generator with specified provider"""
        self.provider = provider
        self.api_key = get_api_key(provider)
        self.base_url = get_base_url(provider)
        self.model = get_model(provider)

        # Initialize OpenAI client (works for both OpenAI and DeepSeek)
        if self.base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = OpenAI(api_key=self.api_key)

    def generate_tweets(self, commits_text, style="technical", num_options=3):
        """
        Generate tweet options from commits

        Args:
            commits_text: Formatted commits text
            style: Tweet style (technical, casual, celebratory)
            num_options: Number of tweet options to generate

        Returns:
            List of tweet text options
        """
        style_prompts = {
            "technical": "Technical but accessible - explain what was built and why it matters",
            "casual": "Conversational and story-driven - share the journey and learnings",
            "celebratory": "Enthusiastic and milestone-focused - highlight wins and progress"
        }

        style_instruction = style_prompts.get(style, style_prompts["technical"])

        prompt = f"""You are a developer building in public on Twitter/X. Your audience wants to follow your JOURNEY, not just see a changelog.

Analyze these git commits and generate {num_options} engaging tweet options for the #buildinpublic community:

COMMITS:
{commits_text}

TWEET FORMULA - Use this structure:
1. START with what you're building (the product/vision) - NOT technical details
2. TODAY'S PROGRESS - Specific wins framed as user value or business impact
3. INSIGHT or next step - What you learned or what's next

STYLE: {style_instruction}

GOOD EXAMPLES (all under 260 chars):
✓ "Building a legal case tool. Shipped a client portal today - lawyers can share updates in real-time. No more 'what's my status?' calls. Notifications next 🚀" (157 chars)

✓ "Day 12 of #buildinpublic: Deployed my SaaS to Vercel in 20 mins. Localhost → production feels amazing. Learning DevOps the hard way. Auth next week!" (149 chars)

✓ "Solved offline mode today. Rewrote our sync logic and tested on airplane mode - it just works. This polish will set us apart." (128 chars)

BAD EXAMPLES (Don't do this):
✗ "Updated styling across multiple pages and fixed config for Vercel deployment"
✗ "Just shipped styling improvements and Vercel fixes for my Next.js app"
✗ "Next.js project update: Fixed Vercel deployment issues, updated multiple page components"

REQUIREMENTS:
- CRITICAL: Keep under 260 characters (aim for 240-260 to be safe)
- Lead with WHAT you're building, not how
- Frame technical work as user/business value
- Be concise - every word must earn its place
- Sound human - use "I" and "we", share learnings
- Emojis are fine but don't overdo it (1-2 max)
- Avoid generic words like "updated", "improved", "fixed" without context

Generate {num_options} different tweet options, each on its own line, numbered 1., 2., 3., etc.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that turns git commits into engaging tweets for developers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )

            # Parse response into individual tweets
            response_text = response.choices[0].message.content.strip()
            tweets = []

            for line in response_text.split('\n'):
                line = line.strip()
                # Remove numbering like "1.", "2.", etc.
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Strip leading number/bullet and period/dash
                    tweet = line.lstrip('0123456789.-) ').strip()
                    if tweet:
                        tweets.append(tweet)

            return tweets if tweets else [response_text]

        except Exception as e:
            raise Exception(f"Error generating tweets: {str(e)}")

    def generate_thread(self, commits_text):
        """Generate a tweet thread for more detailed updates"""
        prompt = f"""You are a developer building in public on Twitter/X. Create a tweet thread that tells the STORY of today's work.

Analyze these git commits and create an engaging thread for the #buildinpublic community:

COMMITS:
{commits_text}

THREAD STRUCTURE:
Tweet 1 (HOOK): What you're building + today's big win. Make people want to read more.
Tweet 2-3 (DETAILS): Expand on the journey - what you built, challenges solved, learnings
Tweet 4 (CLOSE): What's next or key insight

GOOD THREAD EXAMPLE (each under 260 chars):
1/ "Shipped client portal for my legal SaaS. Lawyers share updates in real-time, clients stop calling for status. #1 requested feature ✅" (136 chars)

2/ "Built a notification system that emails + saves to portal. Took 3 tries to nail Next.js state management, but it's solid." (124 chars)

3/ "Deployed to Vercel in 20 mins. Polished contact & careers pages too. The styling makes it feel professional." (112 chars)

4/ "Next: document uploads for file sharing. Then beta users. Building in public keeps me accountable 💪" (103 chars)

BAD THREAD EXAMPLE (Don't do this):
1/ "Today's Next.js progress: Updated styling across multiple pages"
2/ "Fixed config for Vercel deployment. Updated package.json"
3/ "Changed 2,895 lines of code. Building in public!"

REQUIREMENTS:
- CRITICAL: Each tweet must be under 260 characters (aim for 240-260)
- Tell a story, not a changelog
- Include specific wins with business/user context
- Be concise and punchy - cut unnecessary words
- Sound authentic and human
- 2-4 tweets depending on content
- End with what's next or a key insight

Generate the thread with each tweet on its own line, numbered 1., 2., 3., etc.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that turns git commits into engaging tweet threads."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )

            # Parse response into individual tweets
            response_text = response.choices[0].message.content.strip()
            tweets = []

            for line in response_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    tweet = line.lstrip('0123456789.-) ').strip()
                    if tweet:
                        tweets.append(tweet)

            return tweets if tweets else [response_text]

        except Exception as e:
            raise Exception(f"Error generating thread: {str(e)}")
