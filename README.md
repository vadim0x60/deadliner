# Deadliner

Fetches scientific conference and workshops deadlines from the internet

## Command line usage

To use `deadliner` you need an account with [ValueSERP](https://www.valueserp.com/) and [OpenAI](https://openai.com/api/).
Sign up if you haven't already and get your API keys.
Then run

```
VALUESERP=your-valueserp-api-key OPENAI=your-openai-api-key CONFERENCE='ICLR 2022' ./deadliner
```

The expected output is:

```
ICLR 2022
Main track deadline: 2022-04-25 00:00:00
AI for Earth and Space Science 2022-04-09 00:00:00
Deep Generative Models for Highly Structured Data 2022-02-25 00:00:00
From Cells to Societies: Collective Learning Across Scales 2022-02-25 00:00:00
Gamification and Multiagent Solutions 2022-02-26 00:00:00
Generalizable Policy Learning in the Physical World 2022-04-29 00:00:00
Machine Learning for Drug Discovery (MLDD) 2022-04-09 00:00:00
Socially Responsible Machine Learning 2022-02-25 00:00:00
Wiki-M3L: Wikipedia and Multimodal & Multilingual Research 2022-04-09 00:00:00
Workshop on Agent Learning in Open-Endedness 2022-02-25 00:00:00
1st CSS program 2022-10-09 00:00:00
```

## Python library usage

```
from scrape import find_date
```

lets you find any date by query string like "The Battle of Hastings" or "ICML 2020 registration deadline" in python's `datetime` format

```
from conferencer import find_workshops
```

lets you fetch a list of workshops for a given conference name