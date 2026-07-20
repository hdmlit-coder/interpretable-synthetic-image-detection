from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import pandas as pd


CONCEPTS = [
    "hand_anatomy",
    "facial_consistency",
    "text_readability",
    "repeated_texture_patterns",
    "object_boundary_consistency",
    "background_coherence",
]


def load_annotations(path: Path) -> pd.DataFrame:
    # Automatically detects comma- or semicolon-separated CSV files.
    df = pd.read_csv(path, sep=None, engine="python", dtype=str)

    required = {
        "image_id",
        "image_path",
        "label",
        "generator",
        *CONCEPTS,
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(sorted(missing))
        )

    df["label"] = df["label"].str.strip().str.lower()
    df["generator"] = df["generator"].str.strip()

    for concept in CONCEPTS:
        values = df[concept].astype(str).str.strip()
        values = values.replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "N/A": pd.NA,
                "n/a": pd.NA,
                "NA": pd.NA,
            }
        )
        df[concept] = pd.to_numeric(values, errors="coerce")

        invalid = df[concept].dropna()[~df[concept].dropna().isin([0, 1, 2, 3])]
        if not invalid.empty:
            raise ValueError(
                f"Invalid scores found in {concept}: "
                f"{sorted(invalid.unique().tolist())}"
            )

    return df


def save_bar_chart(summary: pd.DataFrame, output: Path) -> None:
    chart = summary.set_index("concept")[["real", "synthetic"]]
    chart.plot(kind="bar", figsize=(11, 6))
    plt.title("Average Concept Scores: Real vs Synthetic")
    plt.xlabel("Concept")
    plt.ylabel("Average score")
    plt.xticks(rotation=35, ha="right")
    plt.ylim(0, 3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze concept annotations."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/concepts/batches/batch_001_annotations.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/concepts/batch_001"),
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    df = load_annotations(args.input)

    print(f"Loaded {len(df)} images.")
    print("\nLabel counts:")
    print(df["label"].value_counts(dropna=False))

    print("\nGenerator counts:")
    print(df["generator"].value_counts(dropna=False))

    # Average score by real/synthetic label.
    means = df.groupby("label")[CONCEPTS].mean().transpose()
    means.index.name = "concept"
    means = means.reset_index()

    for expected_label in ["real", "synthetic"]:
        if expected_label not in means.columns:
            means[expected_label] = pd.NA

    means = means[["concept", "real", "synthetic"]]
    means["difference"] = means["synthetic"] - means["real"]
    means.to_csv(
        args.output_dir / "concept_means_by_label.csv",
        index=False,
    )

    # Average score by generator.
    generator_means = (
        df.groupby("generator")[CONCEPTS]
        .mean()
        .transpose()
    )
    generator_means.index.name = "concept"
    generator_means.to_csv(
        args.output_dir / "concept_means_by_generator.csv"
    )

    # Number and percentage of N/A values.
    na_counts = df[CONCEPTS].isna().sum()
    na_summary = pd.DataFrame(
        {
            "concept": CONCEPTS,
            "na_count": [na_counts[c] for c in CONCEPTS],
            "na_percentage": [
                100 * na_counts[c] / len(df) for c in CONCEPTS
            ],
        }
    )
    na_summary.to_csv(
        args.output_dir / "concept_na_summary.csv",
        index=False,
    )

    # Score distributions.
    distribution_rows = []
    for concept in CONCEPTS:
        for label in ["real", "synthetic"]:
            subset = df.loc[df["label"] == label, concept]
            counts = subset.value_counts(dropna=False)

            for score in [0, 1, 2, 3]:
                distribution_rows.append(
                    {
                        "concept": concept,
                        "label": label,
                        "score": score,
                        "count": int(counts.get(score, 0)),
                    }
                )

            distribution_rows.append(
                {
                    "concept": concept,
                    "label": label,
                    "score": "N/A",
                    "count": int(subset.isna().sum()),
                }
            )

    pd.DataFrame(distribution_rows).to_csv(
        args.output_dir / "concept_score_distributions.csv",
        index=False,
    )

    # Concept correlations, excluding N/A pairwise.
    df[CONCEPTS].corr(method="spearman").to_csv(
        args.output_dir / "concept_spearman_correlations.csv"
    )

    save_bar_chart(
        means,
        args.output_dir / "concept_means_real_vs_synthetic.png",
    )

    print("\nAverage scores:")
    print(means.round(3).to_string(index=False))

    print(f"\nResults saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
