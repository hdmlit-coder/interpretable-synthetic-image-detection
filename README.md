# Interpretable Synthetic Image Detection

This repository contains the experimental work for my PhD research on **concept-based representations for detecting AI-generated images**.

The objective of this research is to investigate how interpretable, concept-based representations can improve the transparency and trustworthiness of AI-generated image detection systems while maintaining competitive detection performance.

---

## Research Motivation

Recent advances in generative AI have made it possible to produce highly realistic synthetic images using diffusion models and GANs. Although numerous detection methods have been proposed, most existing approaches operate as black-box classifiers and provide little insight into **why** an image is classified as real or AI-generated.

This research aims to bridge the gap between **high-performance detection** and **human-understandable explanations** by incorporating concept-based representations into the detection pipeline.

The central research question is:

> **Can concept-based representations improve the interpretability of AI-generated image detection systems without significantly degrading detection performance?**

---

## Research Objectives

- Review and compare state-of-the-art methods for AI-generated image detection.
- Reproduce published detection methods to establish reliable experimental baselines.
- Compare different architectures, datasets, and evaluation protocols.
- Investigate explainability techniques and concept-based learning methods.
- Design and implement a concept-based framework for interpretable AI-generated image detection.

---

## Current Progress

### Literature Review
- Comprehensive survey of AI-generated image detection methods.
- Identification of research gaps in explainability and interpretability.

### Reproduced Baselines

#### 1. CIFAKE
- Repository successfully reproduced.
- Models reproduced:
  - LeNet
  - VGG16 (planned)
  - Neural Network baseline (planned)
- Dataset:
  - CIFAKE

#### 2. CLIP-Based Synthetic Image Detection
- Repository successfully reproduced.
- Models evaluated:
  - `clipdet_latent10k_plus`
  - `Corvi2023`
  - Fusion model
- Dataset:
  - Synthbuster

Obtained results:

| Model | Average AUC |
|--------|------------:|
| clipdet_latent10k_plus | **0.871** |
| Corvi2023 | **0.821** |
| Fusion | **0.924** |

---

## Planned Research

The next stage of this research focuses on developing a **Concept-Based Representation Framework** capable of:

- discovering meaningful visual concepts,
- associating concepts with AI-generated artifacts,
- providing human-interpretable explanations,
- maintaining competitive detection performance.

---

## Future Work

- Reproduce additional state-of-the-art detectors.
- Study Concept Bottleneck Models (CBMs).
- Investigate TCAV and ACE for concept-based explanations.
- Develop an interpretable concept extraction module.
- Evaluate explainability and detection performance on multiple datasets.

---
## Project Status

### Phase 1 – Baselines
- ✅ CIFAKE reproduced
- ✅ CLIP-Based Synthetic Image Detection reproduced

### Phase 2 – Concept Learning
- ✅ Concept vocabulary
- ✅ Concept definitions
- ✅ Pilot dataset (20 images)
- ✅ Pilot annotation
- ✅ Pilot analysis

### Phase 3 – Expanded Concept Dataset
- ✅ 200 manually annotated images
- ✅ Balanced real/synthetic dataset
- ✅ Multi-generator coverage
- ✅ Concept analysis pipeline

### Upcoming
- Automatic concept prediction
- Concept Bottleneck Model
- Evaluation against baseline detectors
  
---
## Author

**Houda Malki**

PhD Research Project

Topic:

**Concept-Based Representations for Detecting AI-Generated Images**
