# CLIP-Based Synthetic Image Detection Baseline

## Paper and Repository

This baseline corresponds to the official implementation of a CLIP-based method for detecting AI-generated images.

Repository:

https://github.com/grip-unina/ClipBased-SyntheticImageDetection

## Objective

The objective of this reproduction was to evaluate a modern synthetic-image detector that uses pretrained CLIP representations and compare it with a conventional forensic detector.

## Architecture

The method combines two detector branches:

```text
Input image
    ↓
CLIP-based detector ─────────┐
                             ├── Fusion score
Forensic ResNet detector ────┘
    ↓
Real / synthetic prediction
