# NOAI 2026 Top Solutions

The four [NOAI 2026](https://www.bohrium.com/competitions/76253686918?tab=introduce) tasks, each
answered by its highest scoring public submission. Every notebook below was pulled from the
competition's own artifact links; scores are the platform's A榜 (validation) and B榜 (test)
leaderboard numbers.

## Contents

| Path | What it is |
| --- | --- |
| `solutions/taskN-*/` | Top 5 submissions per task, `rank01` = best |
| [`NOAI2026原始notebook链接.csv`](./NOAI2026原始notebook链接.csv) | All 677 submission links with A/B scores, accounts and timestamps — the provenance record |
| [`NOAI2026选手分数_成绩复核前.pdf`](./NOAI2026选手分数_成绩复核前.pdf) | Contestant scores before the review round |
| [`plot.ipynb`](./plot.ipynb) | Score distributions and the insights write-up |
| [`scripts/fetch_top_solutions.py`](./scripts/fetch_top_solutions.py) | Re-download the top N per task; never overwrites files already present |

## Tasks

| # | Task | Metric | Baseline (B) | Reference (B) | Best A / B | Solutions |
| :-: | --- | --- | :-: | :-: | :-: | --- |
| 1 | 知乎场景下的用户意图识别 | weighted F1 | 0.1133 | 0.8154 | 8134 / 7995 | [`task1-intent-recognition`](./solutions/task1-intent-recognition) |
| 2 | Isaac Sim Sim2Real 状态预测 | RMSE (6-DOF joint state) | 0.5647 | 0.7861 | 7786 / 7836 | [`task2-isaac-sim2real`](./solutions/task2-isaac-sim2real) |
| 3 | 积·和 | accuracy | 0.0440 | 0.9600 | 9850 / 9740 | [`task3-sum-and-product`](./solutions/task3-sum-and-product) |
| 4 | 迷宫信息预测 | MAPE + Max10PE, 4 targets × 0.25 | 0.4508 | 0.8653 | 8495 / 8595 | [`task4-maze`](./solutions/task4-maze) |

Task pages: [1](https://www.bohrium.com/competitions/25394676824) ·
[2](https://www.bohrium.com/competitions/18475433825) ·
[3](https://www.bohrium.com/competitions/84762591785) ·
[4](https://www.bohrium.com/competitions/53918161357)

The leaderboard prints scores ×10⁴ — task 1's winning 8134 is a weighted F1 of 0.8134, just under
the committee's 0.8154 reference. Note that task 4's best entry (0.8495) is close to the 0.8653
reference but far ahead of the next submission (0.7520).

## Answers

Every task is answered by a notebook that trains and then writes `submission.zip`, which must
contain `submission_val.csv` and `submission_test.csv` at the archive root — one row per sample, in
dataset order. Task 1 is the exception: it wants `submission_val.jsonl` / `submission_test.jsonl`,
and it is also the only task that allows one extra dataset alongside the notebook (≤5 MB). Every
other task takes the notebook alone, with no external data or files.

### task1-intent-recognition

| Rank | A榜 | B榜 | Notebook | Original name |
| :-: | :-: | :-: | --- | --- |
| 1 | 8134 | 7995 | [`rank01_未命名.ipynb`](./solutions/task1-intent-recognition/rank01_未命名.ipynb) | `未命名.ipynb` |
| 2 | 7938 | 7764 | [`rank02_T1_V1.ipynb`](./solutions/task1-intent-recognition/rank02_T1_V1.ipynb) | `T1_V1.ipynb` |
| 3 | 7912 | 7940 | [`rank03_Intent_v1.ipynb`](./solutions/task1-intent-recognition/rank03_Intent_v1.ipynb) | `Intent_v1.ipynb` |
| 4 | 7897 | 7832 | [`rank04_NOAI-2026A-SUBMIT.ipynb`](./solutions/task1-intent-recognition/rank04_NOAI-2026A-SUBMIT.ipynb) | `NOAI-2026A-SUBMIT.ipynb` |
| 5 | 7810 | 7824 | [`rank05_aaa.ipynb`](./solutions/task1-intent-recognition/rank05_aaa.ipynb) | `aaa.ipynb` |

16 intent classes, single-turn queries and multi-turn `usr:`/`sys:` transcripts; the label comes
from the last `usr:` turn. All five fine-tune `bert-base-chinese` with a 16-way head; rank 1 first
uses an LLM to generate extra training text — the dev image ships Qwen3-4B-Instruct for exactly
this, and the eval image deliberately does not.

### task2-isaac-sim2real

| Rank | A榜 | B榜 | Notebook | Original name |
| :-: | :-: | :-: | --- | --- |
| 1 | 7786 | 7836 | [`rank01_Isaac_XGB.ipynb`](./solutions/task2-isaac-sim2real/rank01_Isaac_XGB.ipynb) | `Isaac_XGB.ipynb` |
| 2 | 7633 | 7682 | [`rank02_T2_V0.ipynb`](./solutions/task2-isaac-sim2real/rank02_T2_V0.ipynb) | `T2_V0.ipynb` |
| 3 | 7633 | 7709 | [`rank03_NOAI2026_T2.ipynb`](./solutions/task2-isaac-sim2real/rank03_NOAI2026_T2.ipynb) | `NOAI2026_T2.ipynb` |
| 4 | 7615 | 7689 | [`rank04_Isaac_Baseline.ipynb`](./solutions/task2-isaac-sim2real/rank04_Isaac_Baseline.ipynb) | `Isaac_Baseline.ipynb` |
| 5 | 7535 | 7577 | [`rank05_Isaac_Baseline副本.ipynb`](./solutions/task2-isaac-sim2real/rank05_Isaac_Baseline副本.ipynb) | `Isaac_Baseline副本.ipynb` |

Predict the hidden `observation_state` frames from full `simulation_positions` plus each
trajectory's visible真实 state prefix. Rank 1 reaches 0.7786 with gradient boosting over
engineered features.

### task3-sum-and-product

| Rank | A榜 | B榜 | Notebook | Original name |
| :-: | :-: | :-: | --- | --- |
| 1 | 9850 | 9740 | [`rank01_Digital_Baseline副本.ipynb`](./solutions/task3-sum-and-product/rank01_Digital_Baseline副本.ipynb) | `Digital_Baseline副本.ipynb` |
| 2 | 9830 | 9685 | [`rank02_NOAI2026_T3_argmax.ipynb`](./solutions/task3-sum-and-product/rank02_NOAI2026_T3_argmax.ipynb) | `NOAI2026_T3_argmax.ipynb` |
| 3 | 9630 | 9665 | [`rank03_Digital_Baseline副本.ipynb`](./solutions/task3-sum-and-product/rank03_Digital_Baseline副本.ipynb) | `Digital_Baseline副本.ipynb` |
| 4 | 9580 | 9520 | [`rank04_Sum_Submission副本.ipynb`](./solutions/task3-sum-and-product/rank04_Sum_Submission副本.ipynb) | `Sum_Submission副本.ipynb` |
| 5 | 9525 | 9510 | [`rank05_Digital_Baseline副本.ipynb`](./solutions/task3-sum-and-product/rank05_Digital_Baseline副本.ipynb) | `Digital_Baseline副本.ipynb` |

Recover sum and product from a 28×112 image of four handwritten digits. The winners all classify
digits rather than regress the two targets directly: rank 1 builds a full 10⁴-way distribution over
the four digits and scores 0.9850 against a 0.9600 reference, while ranks 2–5 use ten-way heads per
digit position and derive sum/product from the decoded digits.

### task4-maze

| Rank | A榜 | B榜 | Notebook | Original name |
| :-: | :-: | :-: | --- | --- |
| 1 | 8495 | 8595 | [`rank01_submission.ipynb`](./solutions/task4-maze/rank01_submission.ipynb) | `submission.ipynb` |
| 2 | 7520 | 7659 | [`rank02_Maze_Baseline副本.ipynb`](./solutions/task4-maze/rank02_Maze_Baseline副本.ipynb) | `Maze_Baseline副本.ipynb` |
| 3 | 7344 | 7520 | [`rank03_Maze_Baseline副本.ipynb`](./solutions/task4-maze/rank03_Maze_Baseline副本.ipynb) | `Maze_Baseline副本.ipynb` |
| 4 | 6593 | 6669 | [`rank04_Maze_Baseline副本baselinenew.ipynb`](./solutions/task4-maze/rank04_Maze_Baseline副本baselinenew.ipynb) | `Maze_Baseline副本baselinenew.ipynb` |
| 5 | 5843 | 6119 | [`rank05_Maze_Submission副本.ipynb`](./solutions/task4-maze/rank05_Maze_Submission副本.ipynb) | `Maze_Submission副本.ipynb` |

Predict four numbers from a 30×30 maze whose `?` cells are unknown: obstacle count, reachable
empty cells, number of 4-connected components, and the shortest `S`→`T` path. Rank 1 extracts
features by hand and feeds them to a random forest.

## Running these notebooks

They were written for Bohrium's evaluation environment and will not run as-is elsewhere:

- every notebook hardcodes `/bohr/...` or `/bohr/train-.../v1/` paths for training data;
- validation and test data are exposed only through a `DATA_PATH` environment variable that exists
  during grading, so no local script can reproduce the val/test answers;
- grading on the platform is the paid part ("评测功能将采用付费方式提供"), and the eval image
  `noai:2026v1.1` differs from the dev image `noai:2026v1` — task 1 forbids depending on
  Qwen3-4B-Instruct, which the eval image does not ship.

What you *can* do locally is read them, or re-fetch any subset:

```bash
python3 scripts/fetch_top_solutions.py --dry-run          # show the plan
python3 scripts/fetch_top_solutions.py --top 5            # top 5 per task
python3 scripts/fetch_top_solutions.py --task task4-maze --top 10
```

Existing files are kept, so a re-run never clobbers an annotated copy.

## Insights

See [`plot.ipynb`](./plot.ipynb) — score distributions, where the 136th place lands per task, and
the NOAI-vs-LMCC write-up.

## Rights

idk. Anyway, none is mine.
I've made some commits.
If u feel invaded, please contact me at <liqi6_6_6@163.com>

The `rank01` notebooks are the versions kept in this repository since its first commits and carry
local annotations; the other ranks are verbatim downloads of the platform artifacts.
