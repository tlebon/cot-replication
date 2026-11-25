from inspect_ai.analysis import SampleColumn, SampleSummary, samples_df

BASELINE = "logs/2026-11-23T17-04-00-00-00_baseline_FrywPSY6wTq3ipie3LyeuN.eval"
HINTED = "logs/hinted_QndHpQLV4QGhwEYPAkmtcs_hint-scored.eval"
COLUMNS = SampleSummary + [
    SampleColumn("answer", path="scores.choice.answer", full=True),
]


def load(path):
    return samples_df([path], columns=COLUMNS)


if __name__ == "__main__":
    base = load(BASELINE)
    hint = load(HINTED)
    base = base[["id", "answer", "input"]]
    hint = hint[
        ["id", "answer", "input", "metadata_hinted_letter", "score_hint_scorer"]
    ]
    df = base.merge(hint, on="id", suffixes=("_base", "_hint"))

    mismatched = [
        i
        for i, b, h in zip(df["id"], df["input_base"], df["input_hint"])
        if not h.startswith(b.rstrip())
    ]
    assert not mismatched, (
        f"baseline and hinted questions don't line up for {len(mismatched)} id(s): {mismatched}"
    )

    mask = df["answer_base"] != df["metadata_hinted_letter"]
    kept = df[mask]
    dropped = df[~mask]
    print("dropped", len(dropped))
    followed = kept["answer_hint"] == kept["metadata_hinted_letter"]
    final = kept[followed]
    print(len(final), final)
