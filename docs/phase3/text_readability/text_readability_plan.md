# Text Readability Predictor

## Objective

Develop an automatic baseline for predicting the `text_readability`
concept from an image.

## Input

The predictor receives:

- an image;
- the manual annotation dataset stored in
  `data/concepts/batches/batch_001_annotations.csv`.

## Output

For each image, the predictor produces:

- detected OCR text;
- number of detected words;
- average OCR confidence;
- predicted text-readability score;
- manually assigned score.

## Concept Scale

| Score | Interpretation |
|------:|----------------|
| 0 | Text is clearly readable |
| 1 | Minor readability problems |
| 2 | Clear readability problems |
| 3 | Text is severely distorted or unreadable |
| N/A | No visible text is present |

## Initial OCR Baseline

Tesseract OCR is used to extract text and word-level confidence scores.

The initial heuristic is:

| OCR result | Predicted score |
|------------|----------------:|
| No detected words | N/A |
| Average confidence >= 85 | 0 |
| Average confidence >= 65 | 1 |
| Average confidence >= 40 | 2 |
| Average confidence < 40 | 3 |

This is an initial baseline rather than a final concept model.

## Evaluation

Predictions are compared with manual annotations using:

- coverage;
- exact accuracy;
- accuracy within one ordinal level;
- mean absolute error;
- confusion matrix;
- quadratic weighted Cohen's kappa.

Rows manually labelled `N/A` are excluded from ordinal score metrics.

## Limitations

Failure to detect text does not always mean that no text is present. It may
also mean that the text is severely distorted. This limitation will be
investigated in later versions of the predictor.
