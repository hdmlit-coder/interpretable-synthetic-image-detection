# Baseline Comparison

## Summary

| Property | CIFAKE LeNet | CLIP-Based Detector |
|---|---|---|
| Main representation | CNN features | CLIP and forensic features |
| Dataset | CIFAKE | Synthbuster |
| Image resolution | 32 × 32 | Model-dependent preprocessing |
| Main evaluation | Accuracy | AUC |
| Multiple generators | No | Yes |
| Pretrained representation | No | Yes |
| Explicit concepts | No | No |
| Human-readable explanations | No | No |
| Reproduced locally | Yes | Yes |

## Main Observations

CIFAKE provides a simple and lightweight CNN baseline but relies on low-resolution data and has limited relevance to generalization across modern image generators.

The CLIP-based detector provides a considerably stronger synthetic-image detection baseline and achieves an average AUC of 0.924 using score fusion. However, its predictions remain difficult to interpret.

## Research Gap

Both reproduced baselines focus primarily on predictive performance. Neither baseline introduces an explicit intermediate representation based on human-understandable concepts.

They do not directly explain whether a prediction is supported by properties such as:

- inconsistent lighting,
- abnormal anatomy,
- distorted text,
- unrealistic texture,
- geometric inconsistencies,
- background irregularities.

This limitation motivates the proposed research on concept-based representations for interpretable AI-generated image detection.

## Proposed Direction

The planned research will investigate the following architecture:

```text
Input image
    ↓
Vision encoder
    ↓
Concept extraction
    ↓
Concept scores
    ↓
Concept-based classifier
    ↓
Real / synthetic prediction
    +
Human-readable explanation
