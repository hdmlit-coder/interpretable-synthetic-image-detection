from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError
from pytesseract import Output
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    mean_absolute_error,
)


CONCEPT_COLUMN = "text_readability"
VALID_SCORES = {0, 1, 2, 3}


def load_annotations(csv_path: Path) -> pd.DataFrame:
    """Load comma- or semicolon-separated annotation data."""
    dataframe = pd.read_csv(
        csv_path,
        sep=None,
        engine="python",
        dtype=str,
    )

    required_columns = {
        "image_id",
        "image_path",
        "label",
        "generator",
        CONCEPT_COLUMN,
    }

    missing_columns = required_columns - set(dataframe.columns)
    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    dataframe[CONCEPT_COLUMN] = (
        dataframe[CONCEPT_COLUMN]
        .astype("string")
        .str.strip()
        .replace(
            {
                "": pd.NA,
                "N/A": pd.NA,
                "n/a": pd.NA,
                "NA": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
            }
        )
    )

    dataframe["manual_score"] = pd.to_numeric(
        dataframe[CONCEPT_COLUMN],
        errors="coerce",
    )

    invalid_scores = dataframe.loc[
        dataframe["manual_score"].notna()
        & ~dataframe["manual_score"].isin(VALID_SCORES),
        "manual_score",
    ]

    if not invalid_scores.empty:
        raise ValueError(
            "Invalid manual text-readability scores: "
            f"{sorted(invalid_scores.unique().tolist())}"
        )

    return dataframe


def resolve_image_path(
    raw_path: str,
    repository_root: Path,
    csv_path: Path,
) -> Path:
    """Resolve paths stored as absolute or repository-relative paths."""
    image_path = Path(raw_path).expanduser()

    candidates = [
        image_path,
        repository_root / image_path,
        csv_path.parent / image_path,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    return (repository_root / image_path).resolve()


def preprocess_image(image: Image.Image) -> Image.Image:
    """Apply lightweight preprocessing for the OCR baseline."""
    image = ImageOps.exif_transpose(image)
    image = image.convert("L")
    image = ImageOps.autocontrast(image)
    image = ImageEnhance.Sharpness(image).enhance(1.5)

    minimum_width = 1200
    if image.width < minimum_width:
        scale = minimum_width / image.width
        resized_size = (
            int(image.width * scale),
            int(image.height * scale),
        )
        image = image.resize(resized_size)

    return image


def predict_score(
    average_confidence: Optional[float],
    detected_word_count: int,
) -> Optional[int]:
    """Convert OCR confidence into an ordinal readability prediction."""
    if detected_word_count == 0 or average_confidence is None:
        return None

    if average_confidence >= 85:
        return 0
    if average_confidence >= 65:
        return 1
    if average_confidence >= 40:
        return 2

    return 3


def run_ocr(image_path: Path) -> dict:
    """Run Tesseract and return OCR evidence and the predicted score."""
    try:
        with Image.open(image_path) as opened_image:
            image = preprocess_image(opened_image)

        ocr_data = pytesseract.image_to_data(
            image,
            output_type=Output.DATAFRAME,
            config="--oem 3 --psm 11",
        )

        if ocr_data is None or ocr_data.empty:
            return {
                "ocr_text": "",
                "detected_word_count": 0,
                "average_confidence": None,
                "predicted_score": None,
                "error": "",
            }

        ocr_data["text"] = ocr_data["text"].fillna("").astype(str).str.strip()
        ocr_data["conf"] = pd.to_numeric(
            ocr_data["conf"],
            errors="coerce",
        )

        valid_words = ocr_data.loc[
            (ocr_data["text"] != "")
            & ocr_data["conf"].notna()
            & (ocr_data["conf"] >= 0)
        ].copy()

        detected_word_count = len(valid_words)

        if detected_word_count == 0:
            average_confidence = None
            detected_text = ""
        else:
            average_confidence = float(valid_words["conf"].mean())
            detected_text = " ".join(valid_words["text"].tolist())

        predicted_score = predict_score(
            average_confidence=average_confidence,
            detected_word_count=detected_word_count,
        )

        return {
            "ocr_text": detected_text,
            "detected_word_count": detected_word_count,
            "average_confidence": average_confidence,
            "predicted_score": predicted_score,
            "error": "",
        }

    except (
        FileNotFoundError,
        PermissionError,
        UnidentifiedImageError,
        OSError,
    ) as error:
        return {
            "ocr_text": "",
            "detected_word_count": 0,
            "average_confidence": None,
            "predicted_score": None,
            "error": str(error),
        }


def evaluate_predictions(predictions: pd.DataFrame) -> dict:
    """Evaluate rows for which both manual and predicted scores exist."""
    applicable = predictions.loc[
        predictions["manual_score"].notna()
        & predictions["predicted_score"].notna()
    ].copy()

    manual_applicable_count = int(
        predictions["manual_score"].notna().sum()
    )
    predicted_applicable_count = int(
        predictions["predicted_score"].notna().sum()
    )

    metrics = {
        "total_images": int(len(predictions)),
        "manual_applicable_images": manual_applicable_count,
        "ocr_detected_text_images": predicted_applicable_count,
        "evaluated_images": int(len(applicable)),
        "ocr_coverage_of_manual_applicable": (
            len(applicable) / manual_applicable_count
            if manual_applicable_count
            else None
        ),
    }

    if applicable.empty:
        metrics.update(
            {
                "exact_accuracy": None,
                "within_one_accuracy": None,
                "mean_absolute_error": None,
                "quadratic_weighted_kappa": None,
            }
        )
        return metrics

    y_true = applicable["manual_score"].astype(int)
    y_pred = applicable["predicted_score"].astype(int)

    metrics.update(
        {
            "exact_accuracy": float(accuracy_score(y_true, y_pred)),
            "within_one_accuracy": float(
                ((y_true - y_pred).abs() <= 1).mean()
            ),
            "mean_absolute_error": float(
                mean_absolute_error(y_true, y_pred)
            ),
            "quadratic_weighted_kappa": float(
                cohen_kappa_score(
                    y_true,
                    y_pred,
                    labels=[0, 1, 2, 3],
                    weights="quadratic",
                )
            ),
        }
    )

    return metrics


def save_confusion_matrix(
    predictions: pd.DataFrame,
    output_path: Path,
) -> None:
    applicable = predictions.loc[
        predictions["manual_score"].notna()
        & predictions["predicted_score"].notna()
    ].copy()

    if applicable.empty:
        return

    y_true = applicable["manual_score"].astype(int)
    y_pred = applicable["predicted_score"].astype(int)

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3],
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=[0, 1, 2, 3],
    )
    display.plot(values_format="d")
    plt.title("Text Readability: Manual vs OCR Prediction")
    plt.xlabel("Predicted score")
    plt.ylabel("Manual score")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict text readability with Tesseract OCR."
    )
    parser.add_argument(
        "--annotations",
        type=Path,
        default=Path(
            "data/concepts/batches/batch_001_annotations.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "results/concepts/text_readability"
        ),
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
    )
    args = parser.parse_args()

    annotations_path = args.annotations.resolve()
    repository_root = args.repository_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not annotations_path.exists():
        raise FileNotFoundError(
            f"Annotation file not found: {annotations_path}"
        )

    dataframe = load_annotations(annotations_path)

    prediction_rows = []

    for index, row in dataframe.iterrows():
        image_path = resolve_image_path(
            raw_path=str(row["image_path"]),
            repository_root=repository_root,
            csv_path=annotations_path,
        )

        print(
            f"[{index + 1}/{len(dataframe)}] "
            f"Processing {image_path.name}"
        )

        if not image_path.exists():
            ocr_result = {
                "ocr_text": "",
                "detected_word_count": 0,
                "average_confidence": None,
                "predicted_score": None,
                "error": f"Image not found: {image_path}",
            }
        else:
            ocr_result = run_ocr(image_path)

        prediction_rows.append(
            {
                "image_id": row["image_id"],
                "image_path": row["image_path"],
                "resolved_image_path": str(image_path),
                "label": row["label"],
                "generator": row["generator"],
                "manual_score": row["manual_score"],
                **ocr_result,
            }
        )

    predictions = pd.DataFrame(prediction_rows)

    predictions_path = output_dir / "predictions.csv"
    metrics_path = output_dir / "metrics.json"
    confusion_matrix_path = output_dir / "confusion_matrix.png"

    predictions.to_csv(predictions_path, index=False)

    metrics = evaluate_predictions(predictions)

    with metrics_path.open("w", encoding="utf-8") as output_file:
        json.dump(metrics, output_file, indent=2)

    save_confusion_matrix(
        predictions=predictions,
        output_path=confusion_matrix_path,
    )

    print("\nEvaluation metrics")
    print(json.dumps(metrics, indent=2))
    print(f"\nPredictions: {predictions_path}")
    print(f"Metrics: {metrics_path}")

    if confusion_matrix_path.exists():
        print(f"Confusion matrix: {confusion_matrix_path}")


if __name__ == "__main__":
    main()
