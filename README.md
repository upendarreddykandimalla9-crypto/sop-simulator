# S&OP Simulator — Inventory & Replenishment Experiments

A minimal simulator to compare replenishment policies (EOQ, Base‑Stock, Newsvendor)
under stochastic demand with lead times and service‑level targets.

## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python simulate.py --policy basestock --h 1.0 --c 10.0 --p 30.0 --mu 100 --sigma 25 --lead 2 --periods 365
python plot.py --input artifacts/history.csv
```

## Policies
- `eoq`: classic EOQ with reorder point
- `basestock`: order-up-to S with lead time L
- `newsvendor`: single-period approximation repeated each day

Outputs: CSV history of on-hand, backlog, service level, total cost components.
