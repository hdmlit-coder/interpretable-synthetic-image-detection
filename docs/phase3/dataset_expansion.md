# Phase 3 – Expanded Concept Annotation Dataset

## Overview

Following the successful pilot annotation study, the concept-annotated dataset was expanded to support the development and evaluation of an interpretable synthetic image detection model.

The objective of this stage was to create a larger and more representative dataset containing manually annotated visual concepts for both real and synthetic images.

---

# Dataset Composition

The expanded dataset contains **200 manually annotated images**.

| Class | Images |
|-------|-------:|
| Real | 100 |
| Synthetic | 100 |
| Total | 200 |

---

# Data Sources

## Real Images

Real images were randomly selected from the **Synthbuster RAISE-1K** subset.

## Synthetic Images

Synthetic images were sampled from five different image generators included in the Synthbuster benchmark.

| Generator | Images |
|-----------|-------:|
| DALL·E 2 | 20 |
| DALL·E 3 | 20 |
| Firefly | 20 |
| Midjourney v5 | 20 |
| Stable Diffusion XL | 20 |

Using multiple generators increases the diversity of synthetic artifacts and reduces dependence on a single generation model.

---

# Selected Concepts

Each image was manually annotated using the six concepts retained after the pilot study.

1. Hand anatomy
2. Facial consistency
3. Text readability
4. Repeated texture patterns
5. Object boundary consistency
6. Background coherence

---

# Annotation Scale

Each applicable concept was assigned one of the following values.

| Score | Meaning |
|------:|---------|
| 0 | No visible issue |
| 1 | Minor issue |
| 2 | Clear issue |
| 3 | Severe issue |
| N/A | Concept not applicable |

Examples:

- No visible hands → Hand anatomy = N/A
- Visible realistic hands → Hand anatomy = 0
- No visible text → Text readability = N/A
- Clearly readable text → Text readability = 0

---

# Annotation Procedure

Annotations were performed manually by the project author.

Each image was inspected individually and evaluated according to the operational concept definitions established during Phase 2.

The completed annotations are stored in:

```
data/concepts/batches/batch_001_annotations.csv
```

---

# Dataset Analysis

The expanded dataset was analyzed using the script:

```
src/analyze_concept_annotations.py
```

The analysis generates:

- average concept scores by class;
- average concept scores by generator;
- concept score distributions;
- concept correlation matrix;
- N/A statistics; and
- comparison plots between real and synthetic images.

Generated results are stored in:

```
results/concepts/batch_001/
```

---

# Purpose

The expanded concept dataset serves as the foundation for the next stage of the research.

Rather than manually assigning concept values, Phase 3 will investigate automatic prediction of these concepts using computer vision and vision-language models.

The predicted concept vector will subsequently be used by an interpretable concept-based classifier for synthetic image detection.

---

# Current Status

The following milestones have been completed.

- ✅ Expanded concept dataset created.
- ✅ 200 images manually annotated.
- ✅ Balanced real and synthetic classes.
- ✅ Multiple synthetic generators included.
- ✅ Concept statistics generated.
- ✅ Dataset prepared for automatic concept prediction.

---

# Next Step

The next objective is to develop automatic predictors for the selected concepts.

The first concept to be investigated will be **Text Readability**, using Optical Character Recognition (OCR) as an initial baseline before extending the approach to the remaining concepts.