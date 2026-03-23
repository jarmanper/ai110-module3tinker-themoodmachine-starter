# The Mood Machine

The Mood Machine is a simple text classifier that begins with a rule based approach and can optionally be extended with a small machine learning model. It tries to guess whether a short piece of text sounds **positive**, **negative**, **neutral**, or even **mixed** based on patterns in your data.

This lab gives you hands on experience with how basic systems work, where they break, and how different modeling choices affect fairness and accuracy. You will edit code, add data, run experiments, and write a short model card reflection.

---

## Repo Structure

```plaintext
├── dataset.py         # Starter word lists and example posts (you will expand these)
├── mood_analyzer.py   # Rule based classifier with TODOs to improve
├── main.py            # Runs the rule based model and interactive demo
├── ml_experiments.py  # (New) A tiny ML classifier using scikit-learn
├── model_card.md      # Template to fill out after experimenting
└── requirements.txt   # Dependencies for optional ML exploration
```

---

## Getting Started

1. Open this folder in VS Code.
2. Make sure your Python environment is active.
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the rule-based starter:

    ```bash
    python main.py
    ```

If pieces of the analyzer are not implemented yet, you will see helpful errors that guide you to the TODOs.

To try the ML model later, run:

```bash
python ml_experiments.py
```

---

## What You Will Do

During this lab you will:

- Implement the missing parts of the rule based `MoodAnalyzer`.
- Add new positive and negative words.
- Expand the dataset with more posts, including slang, emojis, sarcasm, or mixed emotions.
- Observe unusual or incorrect predictions and think about why they happen.
- Train a tiny machine learning model and compare its behavior to your rule based system.
- Complete the model card with your findings about data, behavior, limitations, and improvements.
- The goal is to help you reason about how models behave, how data shapes them, and why even small design choices matter.

---

## Tips

- Start with preprocessing before updating scoring rules.
- When debugging, print tokens, scores, or intermediate choices.
- Ask an AI assistant to help create edge case posts or unusual wording.
- Try examples that mislead or confuse your model. Failure cases teach you the most.

---

## Instructor Notes

The core concept here is that models don't understand language — they match patterns, and the patterns they can match are bounded by the data and rules you give them. Students are most likely to struggle when the ML model reports 100% accuracy and they take it at face value; the leap from "it got everything right" to "it memorized the training data" is not obvious without prompting. AI tools like Copilot were genuinely helpful for brainstorming edge-case posts and explaining why a specific word triggered a wrong score, but they tend to propose fixes before students have had a chance to diagnose the failure themselves, which shortcuts the most valuable part of the exercise. If a student is stuck on why a post is mislabeled, a useful nudge is to ask them to run `explain()` on it and read the output aloud — once they see which single word drove the decision, they usually figure out the problem on their own. The sarcasm case ("I absolutely love sitting in traffic") is the best teaching moment in the lab: it's a clean example of a model being confidently wrong for a reason that no amount of word-list tuning can fix, which sets up the honest conversation about what rule-based systems fundamentally cannot do.

---

## Activity Summary

### What was built

A two-version mood classifier that labels short text as `positive`, `negative`, `neutral`, or `mixed`.

The rule-based version in `mood_analyzer.py` was implemented from scratch:

- `preprocess()` lowercases text, strips punctuation (keeping apostrophes for contractions), and tokenizes on whitespace.
- `score_text()` loops over tokens, adding +1 for positive words and -1 for negative words, with negation handling — if a token like `not` or `never` precedes a sentiment word, the score is flipped.
- `predict_label()` checks for both positive and negative hits in the same post to catch mixed sentiment, then falls back to the numeric score.

The word lists in `dataset.py` were expanded beyond the starter set to include slang positives (`sick`, `fire`, `lit`, `slapped`) and missing emotional words (`exhausted`, `anxious`, `proud`, `overwhelmed`).

### Dataset

`SAMPLE_POSTS` was expanded from 6 to 21 labeled examples. New posts were written to include:

- Casual slang and informal tone ("ngl today actually slapped", "lowkey stressed")
- Sarcasm ("I absolutely love sitting in traffic for 2 hours")
- Mixed emotions ("exhausted but so proud of myself")
- Ambiguous phrasing ("everything's fine I'm fine we're all fine")

### Evaluation results

| Model | Accuracy on SAMPLE_POSTS |
|---|---|
| Rule-based | 11/21 (52%) |
| ML (logistic regression) | 21/21 (100%) |

The ML model's 100% is training accuracy on the same 21 examples it was trained on — memorization, not generalization. The rule-based failures were almost entirely due to vocabulary gaps and one case of undetectable sarcasm.

### Key failure patterns identified

- **Sarcasm:** `"I absolutely love sitting in traffic for 2 hours"` → predicted `positive` because `love` dominates. No word-list approach can detect this.
- **Missing vocabulary:** `"woke up late missed the bus and it is only Monday"` → predicted `neutral` because no words matched any list, despite a clearly negative tone.
- **Colloquial negation:** `"yeah no that was not it"` → predicted `neutral`. The phrase is idiomatic — `not it` is a dismissal, but `it` has no sentiment value.

### Takeaway

Rule-based systems are transparent and debuggable but brittle — every gap in the vocabulary is a gap in coverage. The ML model handled patterns the rules couldn't, but its accuracy number is misleading at this dataset size. Both approaches require careful evaluation beyond a single accuracy score.
