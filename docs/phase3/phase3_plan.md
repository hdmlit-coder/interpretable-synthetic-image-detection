# Phase 3 – Interpretable Concept-Based Detection

## Objective

The objective of Phase 3 is to build an interpretable synthetic-image detector that predicts human-understandable visual concepts and uses those concepts to classify images as real or synthetic.

## Selected Concepts

1. Hand anatomy
2. Facial consistency
3. Text readability
4. Repeated texture patterns
5. Object boundary consistency
6. Background coherence

## Tasks

### Task 1 – Expand the Concept-Annotated Dataset

Create a larger balanced dataset containing real and synthetic images from multiple sources and generators.

### Task 2 – Measure Annotation Reliability

Use multiple annotators on a shared subset and calculate inter-annotator agreement.

### Task 3 – Build Automatic Concept Predictors

Evaluate CLIP-based prompting and conventional computer-vision approaches for predicting concept scores.

### Task 4 – Build the Concept Bottleneck Classifier

Train a classifier using the predicted concept vector rather than raw image pixels.

### Task 5 – Evaluate Detection Performance

Measure accuracy, precision, recall, F1 score, ROC-AUC, and performance on unseen generators.

### Task 6 – Evaluate Interpretability

Assess whether concept-based explanations are understandable, faithful, and useful.

### Task 7 – Compare Against Baselines

Compare the concept-based model against the reproduced CIFAKE and CLIP-based synthetic-image detection baselines.

## Initial Dataset Target

The first expanded annotation batch will contain:

- 100 real images
- 100 synthetic images
- 200 images in total

After validating the workflow, the dataset may be expanded further.
