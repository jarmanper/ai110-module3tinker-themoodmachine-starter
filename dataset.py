"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "ngl today actually slapped 😭",
    "I absolutely love sitting in traffic for 2 hours",
    "lowkey stressed but the coffee is hitting rn ☕",
    "vibes are off today idk",
    "just found out I passed no cap I was literally shaking 😭😭",
    "everything's fine I'm fine we're all fine",
    "this week has been a lot but I'm still here 🙃",
    "bro why does everything happen at once 💀",
    "not gonna lie I needed that 😌",
    "could be worse I guess",
    "I hate that I actually enjoyed that 💀",
    "woke up late missed the bus and it is only Monday",
    "honestly kind of proud of myself today :)",
    "this is giving me anxiety but also I kind of want to do it",
    "yeah no that was not it 😭",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # "ngl today actually slapped"
    "negative",  # "I absolutely love sitting in traffic for 2 hours" — sarcasm
    "mixed",     # "lowkey stressed but the coffee is hitting rn"
    "neutral",   # "vibes are off today idk" — vague, hard to pin down
    "positive",  # "just found out I passed no cap I was literally shaking" — overwhelmed relief
    "neutral",   # "everything's fine I'm fine we're all fine" — edge case: possibly sarcastic
    "mixed",     # "this week has been a lot but I'm still here"
    "negative",  # "bro why does everything happen at once"
    "positive",  # "not gonna lie I needed that"
    "neutral",   # "could be worse I guess" — resigned, hard to call
    "mixed",     # "I hate that I actually enjoyed that"
    "negative",  # "woke up late missed the bus and it is only Monday"
    "positive",  # "honestly kind of proud of myself today"
    "mixed",     # "this is giving me anxiety but also I kind of want to do it"
    "negative",  # "yeah no that was not it"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
