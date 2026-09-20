from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "train.csv"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"


def load_data() -> pd.DataFrame:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            "Place the Kaggle train.csv file in data/raw/ before running this script."
        )
    df = pd.read_csv(RAW_FILE)
    df.columns = df.columns.str.lower()
    df["employment_type"] = df["employment_type"].fillna("Unknown")
    df["ltv_band"] = pd.cut(
        df["ltv"],
        bins=[0, 60, 70, 80, 90, float("inf")],
        labels=["<=60%", "60-70%", "70-80%", "80-90%", ">90%"],
        include_lowest=True,
    )
    df["credit_score_band"] = pd.cut(
        df["perform_cns_score"],
        bins=[-1, 0, 300, 600, 750, 900],
        labels=["No score", "1-300", "301-600", "601-750", "751-900"],
    )
    df["prior_delinquency"] = (
        df["delinquent_accts_in_last_six_months"] > 0
    ).map({True: "Yes", False: "No"})
    return df


def summarize(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    overview = pd.DataFrame(
        {
            "metric": [
                "Total loans",
                "Total disbursed amount",
                "Average loan amount",
                "Average LTV",
                "Default rate",
            ],
            "value": [
                len(df),
                df["disbursed_amount"].sum(),
                df["disbursed_amount"].mean(),
                df["ltv"].mean(),
                df["loan_default"].mean(),
            ],
        }
    )

    def segment(column: str) -> pd.DataFrame:
        return (
            df.groupby(column, observed=True)
            .agg(
                loans=("uniqueid", "count"),
                disbursed_amount=("disbursed_amount", "sum"),
                default_rate=("loan_default", "mean"),
                average_ltv=("ltv", "mean"),
            )
            .reset_index()
            .sort_values("default_rate", ascending=False)
        )

    return {
        "overview": overview,
        "ltv_summary": segment("ltv_band"),
        "credit_score_summary": segment("credit_score_band"),
        "employment_summary": segment("employment_type"),
        "prior_delinquency_summary": segment("prior_delinquency"),
    }


def create_dashboard(df: pd.DataFrame, summaries: dict[str, pd.DataFrame]) -> None:
    sns.set_theme(style="whitegrid")
    navy, blue, orange, red = "#17324D", "#2F75B5", "#F4A261", "#C94C4C"
    fig = plt.figure(figsize=(16, 10), facecolor="#F5F7FA")
    grid = fig.add_gridspec(3, 4, height_ratios=[0.8, 2.2, 2.2], hspace=0.55, wspace=0.4)
    metrics = [
        ("LOANS", f"{len(df):,.0f}"),
        ("DISBURSED", f"{df['disbursed_amount'].sum()/1e9:.2f}B"),
        ("AVG LTV", f"{df['ltv'].mean():.1f}%"),
        ("DEFAULT RATE", f"{df['loan_default'].mean():.1%}"),
    ]
    for i, (label, value) in enumerate(metrics):
        ax = fig.add_subplot(grid[0, i])
        ax.set_facecolor("white")
        ax.text(0.05, 0.72, label, fontsize=10, color="#637083", weight="bold")
        ax.text(0.05, 0.18, value, fontsize=23, color=navy, weight="bold")
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_visible(False)

    ax1 = fig.add_subplot(grid[1, :2])
    ltv = summaries["ltv_summary"].sort_values("ltv_band")
    sns.barplot(data=ltv, x="ltv_band", y="default_rate", color=blue, ax=ax1)
    ax1.set(title="Default Rate by LTV Band", xlabel="Loan-to-Value band", ylabel="Default rate")
    ax1.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")

    ax2 = fig.add_subplot(grid[1, 2:])
    credit = summaries["credit_score_summary"].sort_values("credit_score_band")
    sns.barplot(data=credit, x="credit_score_band", y="default_rate", color=orange, ax=ax2)
    ax2.set(title="Default Rate by Credit Score", xlabel="Credit score band", ylabel="Default rate")
    ax2.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")

    ax3 = fig.add_subplot(grid[2, :2])
    prior = summaries["prior_delinquency_summary"].sort_values("prior_delinquency")
    colors = [blue, red] if len(prior) == 2 else [blue]
    sns.barplot(data=prior, x="prior_delinquency", y="default_rate", palette=colors, hue="prior_delinquency", legend=False, ax=ax3)
    ax3.set(title="Impact of Recent Delinquency", xlabel="Delinquent account in last 6 months", ylabel="Default rate")
    ax3.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")

    ax4 = fig.add_subplot(grid[2, 2:])
    top = (
        df.groupby("state_id")
        .agg(loans=("uniqueid", "count"), default_rate=("loan_default", "mean"))
        .query("loans >= 1000")
        .nlargest(8, "default_rate")
        .sort_values("default_rate")
        .reset_index()
    )
    sns.barplot(data=top, x="default_rate", y=top["state_id"].astype(str), color=red, ax=ax4)
    ax4.set(title="Highest-Default States (1,000+ loans)", xlabel="Default rate", ylabel="State ID")
    ax4.xaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")

    fig.suptitle("AUTO LOAN PORTFOLIO | DEFAULT & RISK OVERVIEW", x=0.05, y=0.99, ha="left", fontsize=18, weight="bold", color=navy)
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / "portfolio_dashboard.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = load_data()
    summaries = summarize(df)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for name, table in summaries.items():
        table.to_csv(PROCESSED / f"{name}.csv", index=False)
    create_dashboard(df, summaries)
    print("Analysis complete. Outputs saved to data/processed and reports/figures.")


if __name__ == "__main__":
    main()

