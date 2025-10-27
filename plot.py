import argparse, pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="artifacts/history.csv")
    a = ap.parse_args()
    df = pd.read_csv(a.input)
    plt.figure()
    plt.plot(df["t"], df["on_hand"], label="on_hand")
    plt.plot(df["t"], df["backlog"], label="backlog")
    plt.plot(df["t"], df["order"], label="order")
    plt.legend()
    plt.title("Inventory Trajectories")
    plt.xlabel("t")
    plt.ylabel("units")
    plt.tight_layout()
    plt.savefig("artifacts/trajectories.png")
    print("Saved artifacts/trajectories.png")
