# Model Card: Mood Machine

This model card covers both versions of the Mood Machine mood classifier:

1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**
Both models were built and compared. The rule-based model was the primary focus; the ML model was run for comparison.

**Intended purpose:**
Classify short social media-style text posts into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**
The rule-based model scans each post for known positive and negative words, adjusts scores based on negation words like "not" or "never," and maps the final score to a label. The ML model converts each post into a bag-of-words vector using `CountVectorizer` and trains a logistic regression classifier on the labeled examples.

---

## 2. Data

**Dataset description:**
`SAMPLE_POSTS` contains 21 labeled posts. The original 6 starter posts were expanded with 15 new posts written to cover slang, sarcasm, mixed emotions, and ambiguous tone.

**Labeling process:**
Labels were assigned manually based on the overall feeling of each post, not just the presence of specific words. Several posts were genuinely hard to label:

- `"everything's fine I'm fine we're all fine"` — could be neutral (literal) or negative (sarcastic). Labeled `neutral` but reasonable to argue `negative`.
- `"could be worse I guess"` — resigned acceptance; labeled `neutral` but has a slightly defeated undertone.
- `"I hate that I actually enjoyed that"` — simultaneous dislike and enjoyment; labeled `mixed`.

**Important characteristics of the dataset:**

- Contains casual slang: "ngl," "no cap," "slapped," "lowkey"
- Includes emojis used both ironically and sincerely (e.g., crying emoji for joy)
- Contains at least one clear sarcasm example
- Several posts express genuinely mixed or hard-to-pin-down emotions
- All posts are short (one sentence), similar in structure to social media updates

**Possible issues with the dataset:**

- 21 examples is very small — not enough to train a generalizable ML model
- Labels reflect one person's interpretation; another labeler might disagree on several posts
- Language skews toward a specific demographic (English-speaking, US internet slang)
- No examples of formal language, non-English phrases, or non-Western emotional expression

---

## 3. How the Rule-Based Model Works

**Your scoring rules:**

- `preprocess()` lowercases the text, strips punctuation (keeping apostrophes so contractions stay intact), and splits on whitespace.
- `score_text()` loops over tokens: `+1` for each positive word hit, `-1` for each negative word hit. If the previous token is a negation word (`not`, `never`, `no`, `don't`, etc.), the score is flipped.
- `predict_label()` checks for both positive and negative hits in the same post — if both are present, it returns `"mixed"` before falling through to the score. Otherwise: score > 0 → `positive`, score < 0 → `negative`, score == 0 → `neutral`.
- Word lists were expanded beyond the starter set to include slang positives (`sick`, `fire`, `lit`, `slapped`) and missing emotional words (`exhausted`, `anxious`, `proud`, `overwhelmed`).

**Strengths of this approach:**

- Fully transparent — you can always trace exactly which word caused which score
- Negation handling correctly flips cases like "not happy" and "not bad"
- Adding a word to the list immediately changes behavior — easy to update
- Works without any training data

**Weaknesses of this approach:**

- **Sarcasm is invisible:** `"I absolutely love sitting in traffic for 2 hours"` → predicted `positive` because `love` scores +1. The model has no concept of context.
- **Vocabulary gaps dominate:** `"woke up late missed the bus and it is only Monday"` → predicted `neutral` because none of those words appear in the word lists, even though the sentiment is clearly negative.
- **Colloquial negation fails:** `"yeah no that was not it"` → predicted `neutral`. The phrase "not it" is idiomatic dismissal, but `it` isn't a sentiment word, so the negation has nothing to flip.
- **One strong word can dominate:** A post with ten neutral words and one word like `love` scores `positive` regardless of overall tone.

---

## 4. How the ML Model Works

**Features used:**
Bag of words using `CountVectorizer` — each post becomes a vector of word counts across the full vocabulary.

**Training data:**
Trained on all 21 posts in `SAMPLE_POSTS` with labels from `TRUE_LABELS`.

**Training behavior:**
The ML model achieved 100% accuracy — but it trained and evaluated on the same 21 examples. This is memorization, not learning. It learned that the word "Monday" correlates with `negative` and "a lot" correlates with `mixed` purely because those posts were labeled that way. This makes it extremely sensitive to how you label even a single example.

**Strengths and weaknesses:**

- Strength: it handled sarcasm correctly (`"I absolutely love sitting in traffic"` → `negative`) because it learned the full phrase pattern, not just the word `love`
- Strength: it correctly labeled posts the rule-based model missed entirely, like `"woke up late missed the bus and it is only Monday"` → `negative`
- Weakness: 100% training accuracy on 21 examples is a red flag, not a success — it almost certainly cannot generalize to new sentences
- Weakness: the model is a black box — there is no way to inspect why it made any given prediction

---

## 5. Evaluation

**How the models were evaluated:**
Both models were evaluated on the same 21 labeled posts in `dataset.py`. This measures training accuracy, not generalization.

| Model | Accuracy |
|---|---|
| Rule-based | 11/21 (52%) |
| ML (logistic regression) | 21/21 (100%) |

**Examples of correct predictions (rule-based):**

- `"I love this class so much"` → `positive` — `love` is in the word list, straightforward match
- `"I am not happy about this"` → `negative` — negation handling correctly flips `happy` from +1 to -1
- `"Feeling tired but kind of hopeful"` → `mixed` — `tired` (negative) and `hopeful` (positive) both hit, triggering the mixed path

**Examples of incorrect predictions (rule-based vs. ML):**

- `"I absolutely love sitting in traffic for 2 hours"` — rule-based: `positive`, ML: `negative`, true: `negative`
  The rule-based model sees `love` and stops. The ML model learned the full phrase context from training.

- `"bro why does everything happen at once"` — rule-based: `neutral`, ML: `negative`, true: `negative`
  No words in the rule-based vocabulary signal frustration here. The ML model picked it up as negative from the training label.

- `"this is giving me anxiety but also I kind of want to do it"` — rule-based: `neutral`, ML: `mixed`, true: `mixed`
  `anxiety` wasn't in the original word lists (added later). Even after adding it, `want` has no signal, so the rule-based model still couldn't detect the mixed emotion cleanly.

---

## 6. Limitations

- **The dataset is tiny.** 21 examples cannot train a generalizable ML model. Any accuracy number from `ml_experiments.py` is training accuracy only and is not meaningful for new inputs.
- **The rule-based model cannot detect sarcasm.** Sarcasm requires understanding intent and context — neither of which a word list can provide.
- **Vocabulary coverage is narrow.** Any word not in `POSITIVE_WORDS` or `NEGATIVE_WORDS` is completely invisible to the rule-based model. Entire posts can score neutral simply due to missing vocabulary.
- **Negation scope is limited to one word back.** `"not at all happy"` would fail because `all` sits between `not` and `happy`.
- **Emojis are partially stripped.** The `preprocess()` regex removes most punctuation, which eliminates some emoji signals. Text emoticons like `:)` are also stripped.
- **Labels are one person's interpretation.** For posts like `"everything's fine I'm fine we're all fine"`, another labeler might reasonably choose `negative`. Inter-rater disagreement is not measured.

---

## 7. Ethical Considerations

- **Misclassifying distress.** A post expressing genuine distress in understated language (`"I'm fine"`, `"this week has been a lot"`) could easily be labeled `neutral` or `positive` by this model. In any real-world context — mental health monitoring, content moderation, crisis detection — that failure has real consequences.
- **Dialect and slang bias.** The word lists and training data reflect a specific subset of English internet slang, predominantly US-based and youth-oriented. Language from different communities, dialects, or cultural contexts would be poorly served. For example, British slang ("gutted"), AAVE, or non-Western emotional expression patterns are not represented.
- **Confidentiality.** This model is designed for short social media-style posts. Using it to analyze private messages without consent raises serious privacy concerns.
- **False confidence from high accuracy.** The ML model's 100% score looks impressive. Without understanding that it's training accuracy on 21 examples, a reader might believe the model is reliable — it isn't. Evaluation numbers without context can mislead.

---

## 8. Ideas for Improvement

- **Add more labeled data** — at minimum several hundred examples from real sources to make the ML model's accuracy meaningful
- **Split into train/test sets** so accuracy reflects generalization, not memorization
- **Use TF-IDF** instead of raw counts to downweight common words like "I" and "the"
- **Expand negation scope** to handle multi-word negation like "not at all happy"
- **Add an emoji lookup table** that maps common emojis to sentiment signals before preprocessing strips them
- **Use a small pretrained model** (e.g., a fine-tuned sentiment classifier) that already understands sarcasm and context
- **Collect real disagreements** — for posts where labelers disagree, track uncertainty rather than forcing a single label
