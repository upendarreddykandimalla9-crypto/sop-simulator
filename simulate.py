import argparse, numpy as np, pandas as pd, os

def demand_series(mu, sigma, periods, seed=7):
    rng = np.random.default_rng(seed)
    return np.maximum(0, rng.normal(mu, sigma, periods)).astype(float)

def simulate(policy, h, c, p, mu, sigma, lead, periods, seed=7):
    d = demand_series(mu, sigma, periods, seed)
    on_hand = 0.0
    backlog = 0.0
    pipeline = [0.0]*lead
    history = []

    # policy params
    if policy == "eoq":
        import math
        K = 100.0  # setup cost proxy
        Q = max(1.0, math.sqrt(2 * K * mu / h))
        R = lead * mu + 1.65 * np.sqrt(lead) * sigma  # 95% service
    elif policy == "basestock":
        S = lead * mu + 1.65 * np.sqrt(lead) * sigma
    elif policy == "newsvendor":
        # simple critical fractile with c (unit cost), p (penalty/lost sale), h (holding)
        crit = (p - c) / (p + h)
    else:
        raise ValueError("unknown policy")

    for t in range(periods):
        # receive pipeline
        arriving = pipeline.pop(0) if lead > 0 else 0.0
        on_hand += arriving

        # demand
        dem = d[t]
        shipped = min(on_hand, dem + backlog)
        on_hand -= shipped
        backlog = max(0.0, dem + backlog - shipped)

        # place order
        inv_pos = on_hand + backlog * (-1) + sum(pipeline)
        if policy == "eoq":
            if inv_pos <= R:
                order = Q
            else:
                order = 0.0
        elif policy == "basestock":
            order = max(0.0, S - inv_pos)
        else:  # newsvendor heuristic: order to quantile of next-period demand
            from scipy.stats import norm
            q = norm.ppf(crit, loc=mu, scale=sigma)
            order = max(0.0, q - inv_pos)

        if lead > 0:
            pipeline.append(order)
        else:
            on_hand += order

        history.append({
            "t": t,
            "demand": dem,
            "arrivals": arriving,
            "on_hand": on_hand,
            "backlog": backlog,
            "order": order
        })

    hist = pd.DataFrame(history)
    # cost calc
    hist["holding_cost"] = h * hist["on_hand"]
    hist["backlog_cost"] = p * hist["backlog"]
    hist["purchase_cost"] = c * hist["order"]
    hist["total_cost"] = hist[["holding_cost","backlog_cost","purchase_cost"]].sum(axis=1)
    os.makedirs("artifacts", exist_ok=True)
    hist.to_csv("artifacts/history.csv", index=False)
    print("Saved artifacts/history.csv")
    return hist

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", choices=["eoq","basestock","newsvendor"], default="basestock")
    ap.add_argument("--h", type=float, default=1.0)
    ap.add_argument("--c", type=float, default=10.0)
    ap.add_argument("--p", type=float, default=30.0)
    ap.add_argument("--mu", type=float, default=100.0)
    ap.add_argument("--sigma", type=float, default=25.0)
    ap.add_argument("--lead", type=int, default=2)
    ap.add_argument("--periods", type=int, default=365)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    simulate(a.policy, a.h, a.c, a.p, a.mu, a.sigma, a.lead, a.periods, a.seed)
