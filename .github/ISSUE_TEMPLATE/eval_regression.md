---
name: Evaluation Regression
about: Report a quality regression in RAG output
title: '[EVAL] '
labels: eval, regression
assignees: ''
---

## Regression Summary
<!-- What metric degraded? By how much? -->

## Before / After
| Metric | Before | After |
|---|---|---|
| Faithfulness | | |
| Numeric Accuracy | | |
| P99 Latency | | |

## Affected Queries
<!-- List 1-3 example queries that now produce worse results -->

## Environment / PR
<!-- Which commit or PR introduced the regression? -->

## Reproduction
```bash
python evaluate.py --dataset evals/golden_dataset.jsonl --output report.json
