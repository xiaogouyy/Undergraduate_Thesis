# The Impact of Brand Response Styles on Customer Sentiment in C2C Conflicts

### A Social Identity Perspective on Consumer-to-Consumer Conflicts in Online Brand Communities

> Undergraduate Dissertation (BUSI3222) — Nottingham University Business School, AY2025/2026
> Author: **Yangyang Liu** · Supervisor: Prof. Cai Zhao

---

## Overview

Online Brand Communities (OBCs) are increasingly hotbeds for **Consumer-to-Consumer (C2C) conflicts** — public disputes where users criticize or attack one another. Because these communities are built on shared identities, such conflicts are highly visible, permanent, and contagious, and brands are now expected to intervene. But intervening is risky: *how* a brand responds can either de-escalate a dispute or pour fuel on it.

This dissertation empirically investigates **how the social boundary of a conflict moderates the effect of a brand's response style on post-conflict customer sentiment**. It combines **Social Identity Theory (SIT)** with **Organizational Justice Theory**, and uses a large real-world dataset of Reddit brand-community conversations to test whether "intuitively appropriate" brand responses actually work.

---

## 🔑 Headline Result

> **Brand response styles do *not* work in a uniformly beneficial way — the responses that feel intuitively appropriate often backfire.**
>
> Assertive responses *intensify* negativity in intergroup conflicts, and cooperative ("friendly") responses can *worsen* sentiment in both intergroup and intragroup disputes — a cooperative gesture toward rivals reads as a betrayal of in-group loyalty. Customers evaluate brand interventions not only through **identity protection**, but through **fairness, legitimacy, and communicative appropriateness**. The right move depends on the interaction between the **conflict boundary** and the **social meaning** attached to the response style.

This translates into a concrete, scenario-specific playbook for community managers — the **C2C Conflict Response Strategy Matrix**:

| Conflict Type | Participant Dynamics | Recommended Assertiveness | Recommended Cooperativeness | Core Strategic Orientation |
|---|---|---|---|---|
| **Intragroup** | Loyal Fans vs. Loyal Fans | Low | Low to Moderate | Avoiding or Compromising |
| **Intergroup** | In-group Fans vs. Rival Out-group | Low | Low | Avoiding |
| **Outergroup** | Out-group rivals vs. Out-group rivals | Moderate | Moderate | Compromising / Collaborating / Accommodating |

<sub>*The counter-intuitive core: in most conflict settings, restraint (low assertiveness, low cooperativeness) protects community sentiment better than active identity-defending intervention.*</sub>

---

## Research Design

**Core research question:** Do assertive vs. cooperative brand responses have different effects on customer sentiment across three C2C conflict types — *intragroup*, *intergroup*, and *outergroup* conflicts?

| Element | Detail |
|---|---|
| **Dependent variable** | Post-intervention customer sentiment (Google NLP emotion score, −1 to +1) |
| **Independent variables** | Conflict type (categorical), brand **Assertiveness** index, brand **Cooperativeness** index |
| **Theoretical lens** | Social Identity Theory + Organizational Justice Theory |
| **Data** | 1,148 Reddit conversations → **495 annotated C2C conflicts** (188 intragroup, 164 intergroup, 143 outergroup) |
| **Scope** | 68 brand-owned subreddits across 11 industries |
| **Model** | Partition Least Squares Dummy Variable (LSDV) regression, subreddit-clustered standard errors |

**Method pipeline:** Netnographic data collection (Reddit API) → manual conflict annotation → sentiment quantification (Google NLP) → response-style quantification via **LIWC**-based assertiveness and cooperativeness indices → partition LSDV regression and hypothesis testing.

---

## Key Findings

All three conflict types significantly depress customer sentiment, with **intergroup conflicts** producing the most negative emotional baseline. The moderating effects of response style, however, frequently contradict what Social Identity Theory alone would predict:

| Hypothesis | Path | β | Result |
|---|---|---|---|
| H1a | Intragroup conflict → sentiment | −0.0918*** | Supported |
| H1b | Intergroup conflict → sentiment | −0.1993*** | Supported |
| H1c | Outergroup conflict → sentiment | −0.1694*** | Supported |
| H2a | Assertiveness × Intragroup | −0.0084 | Not supported |
| H2b | Assertiveness × Intergroup | −0.0495* | Supported (negative) |
| H2c | Assertiveness × Outergroup | +0.0044 | Not supported |
| H3a | Cooperativeness × Intragroup | −0.0360* | Refuted (opposite direction) |
| H3b | Cooperativeness × Intergroup | −0.0557** | Supported (negative) |
| H3c | Cooperativeness × Outergroup | −0.0257 | Not supported |

<sub>*p < 0.05, **p < 0.01, ***p < 0.001. N = 495.*</sub>

**Takeaway:** Assertive intervention in intergroup disputes and cooperative ("friendly") intervention toward rivals both *worsen* community sentiment — the latter reads as a betrayal of in-group loyalty. The emotional consequences of an intervention depend on the interaction between the **conflict boundary** and the **social meaning** attached to the response style.

---

## Repository Structure

```
.
├── data_collection.py                    # Reddit API scraper: fetches brand-community
│                                         #   conversations; hash-encrypts user IDs
├── google_nlp_quantify.py                # Google NLP sentiment scoring of post-response comments
├── regression_and_hypothesis_testing.py  # Partition LSDV model + clustered SE + H1–H3 testing
├── Full_text_dissertation.pdf            # Complete dissertation
├── .env.example                          # Template for required API credentials
└── .gitignore
```

---

## Tech Stack

- **Python** — data collection, processing, and statistical modeling
- **Reddit API** — netnographic data source (comment threads from 68 brand subreddits)
- **Google Cloud Natural Language API** — sentiment quantification
- **LIWC** — dictionary-based linguistic indices for assertiveness and cooperativeness
- **Statistical modeling** — partition LSDV regression with subreddit-clustered standard errors

---

## Reproducing the Analysis

> Requires Python 3.x. Install dependencies, then supply your own API credentials.

```bash
# 1. Clone
git clone https://github.com/xiaogouyy/Undergraduate_Thesis.git
cd Undergraduate_Thesis

# 2. Configure credentials
cp .env.example .env
# then edit .env with your Reddit API and Google Cloud NLP keys

# 3. Run the pipeline
python data_collection.py                    # collect raw conversations
python google_nlp_quantify.py                # score sentiment
python regression_and_hypothesis_testing.py  # run the LSDV model
```

*Note:* Raw scraped data is not committed. Reddit and Google NLP credentials are read from `.env` and are never stored in the repository.

---

## Research Ethics & Data Handling

- Only publicly available Reddit comment data was collected.
- All user IDs (except brand-representing subreddit moderators) were **hash-encrypted** during collection to protect user privacy.
- API keys and secrets are kept out of version control via `.env` / `.gitignore`.

---

## Citation

> Liu, Y. (2026). *The Impact of Brand Response Styles on Customer Sentiment in C2C Conflicts: A Social Identity Perspective.* Undergraduate Dissertation, Nottingham University Business School.

**Keywords:** Consumer-to-Consumer (C2C) conflicts · brand response styles · customer sentiment · online brand communities · Social Identity Theory · assertiveness · cooperativeness · sentiment analysis

---

## Contact

**Yangyang Liu** — [yangyang.liu3@mail.mcgill.ca](mailto:yangyang.liu3@mail.mcgill.ca)
