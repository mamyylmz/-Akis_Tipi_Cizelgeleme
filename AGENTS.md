# Repository Guidelines

## Project Structure

This workspace contains planning, paper, benchmark, model, tests, and initial algorithm code for YMM4142 Problem 7. The objective is to minimize makespan (Cmax) in the permutation flow shop scheduling problem (PFSP).

- Read `docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md` for the shared project standard, article headings (Part III), allowed journals (section 18), and acceptance gates. Official course documents and applicable journal rules retain the priority defined in that guide.
- This workspace is the repository root: `docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md` corresponds to `Akis_Tipi_Cizelgeleme/docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md` in the implementation repository. Do not create a duplicate nested repository directory.

- `sprintler/` contains the team plan, sprint assignments, and delivery evidence template. Start with `00_EKIP_ILK_SPRINT_VE_3_ARALIK_PLANI.md`.
- `kişiyeözeldosyaları/` contains role-specific instructions.
- The repository layout uses `src/problem.py` for the PFSP model, `src/algorithms/` for optimizers, `tests/` for independent checks, `data/taillard/` for benchmark files, and `docs/` / `paper/` for research materials. The PFSP model, required Taillard data, DE implementation, and their tests are present. The remaining algorithms and final 30-run experiment results are not yet complete.

## Development Commands

Review Markdown changes directly in this workspace. In the implementation checkout, run `python src/main.py --check` from the root to smoke-test the course template. Run the independent model and algorithm checks before accepting a change. When using the runner's `--only-analysis` option, verify that all expected result files exist.

## Coding Style and Naming

Use four spaces for Python indentation and snake_case for new functions and modules. Preserve the course template's shared API and result fields such as `best_x`, `best_f`, and `n_fes`. Use deterministic random-key decoding with stable sorting and initialize randomness with `np.random.default_rng(seed)`. Record benchmark provenance and SHA-256 hashes in `data/README.md`.

## Testing and Experiment Evidence

Use descriptive `test_*.py` filenames, such as `tests/test_problem.py` and `tests/test_contract.py`. Verify the documented five-job example yields Cmax = 20, reject invalid permutations, check same-seed reproducibility and function-evaluation budgets, and independently recompute the objective for the reported best permutation. Record seeds and retain raw results for each run.

## Commits and Review

Git history is unavailable in this workspace. Use a short, descriptive commit subject. In the PR or delivery record, include the commit SHA or file version, changed files, test commands, expected and observed results, and open issues. Use `sprintler/06_TESLIM_KANIT_SABLONU.md` for delivery evidence. Have an independent reviewer rerun at least one critical check before acceptance.

## Negative Quality Rules

Before accepting technical or paper work, read `docs/NEGATIF_KOMUTLAR_VE_KALITE_KARARLARI.md`. In particular: do not fabricate missing data or files, do not edit acceptance tests merely to make them pass, do not mark unverified literature details as verified, do not treat `main.py --check` as sufficient scientific validation, and do not close P0/P1 findings without rerunning the relevant evidence on the corrected files.
