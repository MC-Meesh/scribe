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

GOOD EXAMPLES:
✓ "Building a legal case management tool. Today: shipped a client portal where lawyers can share updates in real-time. Users won't have to call asking 'what's the status?' anymore. Next: notifications."

✓ "Day 12 of building in public: Added Vercel deployment to my SaaS starter. Went from localhost to production in 20 mins. The DevOps learning curve is real but we're shipping. Auth & payments next week 🚀"

✓ "Solved a tough one today: rewrote our data sync logic to handle offline mode. Tested on my phone with airplane mode - it just works. This is the kind of polish that'll set us apart."

BAD EXAMPLES (Don't do this):
✗ "Updated styling across multiple pages and fixed config for Vercel deployment"
✗ "Just shipped styling improvements and Vercel fixes for my Next.js app"
✗ "Next.js project update: Fixed Vercel deployment issues, updated multiple page components"

REQUIREMENTS:
- Under 280 characters
- Lead with WHAT you're building, not how
- Frame technical work as user/business value
- Include specific details but with context
- Sound human - use "I" and "we", share learnings
- Emojis are fine but don't overdo it
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

GOOD THREAD EXAMPLE:
1/ "Just shipped the client portal for my legal case management SaaS. Lawyers can now share case updates with clients in real-time. No more 'what's my case status?' calls. This was the #1 requested feature 🎉"

2/ "The interesting part: built a notification system that emails clients when there's an update, but also saves it in the portal. Took 3 attempts to get the state management right in Next.js, but it's solid now."

3/ "Deployed to Vercel in 20 mins. Added some polish to the contact page and careers section while I was at it. The styling improvements make the whole app feel more professional."

4/ "Next up: adding document uploads so lawyers can share files directly. Then we're ready for beta users. Building in public keeps me accountable 💪"

BAD THREAD EXAMPLE (Don't do this):
1/ "Today's Next.js progress: Updated styling across multiple pages"
2/ "Fixed config for Vercel deployment. Updated package.json"
3/ "Changed 2,895 lines of code. Building in public!"

REQUIREMENTS:
- Each tweet under 280 characters
- Tell a story, not a changelog
- Include specific wins with business/user context
- Share learnings or challenges overcome
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
