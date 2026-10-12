# MJEPA Schedule of Japan, parsed to HS6

Machine-readable version of **Japan's tariff commitments under the
Malaysia–Japan Economic Partnership Agreement (MJEPA)**, in force 13 July
2006. The source is a 172-page PDF table. This repository gives every
category row of that table, and the staging category of every HS 2002
six-digit code, as CSV and Excel files.

Prepared by **Firdaus** for MA thesis research on the effect of MJEPA on
Malaysian exports to Japan. This is not an official dataset. For legal
purposes, always use the original schedule.

## Files

| File | Content |
|---|---|
| `data/mjepa_japan_schedule_hs6.csv` | One row per HS 2002 six-digit code (5,223 codes): the schedule row that sets its category, and the category(ies) |
| `data/mjepa_japan_schedule_rows.csv` | Every category row parsed from the schedule (1,723 rows), at chapter, heading or HS6 level, with its PDF page |
| `data/categories.csv` | Meaning of each staging category, quoted from the General Notes |
| `data/mjepa_japan_schedule.xlsx` | The three tables above, plus a README sheet, in one workbook |
| `scripts/make_xlsx.py` | Builds the workbook from the CSV files (Python standard library only) |

## Source

| | |
|---|---|
| Document | Japan – Schedule of Tariff Commitments, MJEPA Annex 1, Part 2, Section 2 |
| Copy used | MITI Malaysia: <https://fta.miti.gov.my/miti-fta/resources/Malaysia-Japan/Japan_-_Schedule_of_Tariff_Commitments.pdf> |
| Downloaded | 13 May 2026; 1,044,162 bytes; SHA-256 `679a8d618813ed236be2ba368b2f457b742c23383593ec81611f72edfa0bdee5` |
| Also published by | MOFA Japan, Annex 1 (both countries' schedules): <https://www.mofa.go.jp/region/asia-paci/malaysia/epa/annex1.pdf> |
| Category definitions | MJEPA Annex 1, Part 1, General Notes (MITI copy) |
| Nomenclature | HS 2002 (General Notes, para. 3) |

## How the schedule assigns categories

The schedule does not list every HS6 code. It gives a category at three
levels:

- a **chapter** row, e.g. `Chapter 47 … A` (the whole chapter);
- a **heading** row, e.g. `04.05 … X` (all HS6 codes under the heading);
- an **HS6** row, e.g. `0302.21 … 3.5% B5`, sometimes with several sub-rows
  that carry different categories.

**Resolution rule** (used in `mjepa_japan_schedule_hs6.csv`): each HS6 code
takes its category from the most specific row that covers it: its own HS6
row, else its heading row, else its chapter row. A chapter row applies only
to headings that the schedule does not list separately. The column
`resolved_level` records which level was used.

The **Base Rate** column is blank for Category A rows, because Category A
goes to zero on entry into force and needs no starting rate (General Notes,
para. 4: the base rate is "only the starting point of reduction").

## Data dictionary

### `mjepa_japan_schedule_hs6.csv`

| Column | Meaning |
|---|---|
| `hs6` | HS 2002 six-digit code, `NNNN.NN` (text; keep the leading zero) |
| `resolved_level` | `hs6`, `heading` or `chapter`: the schedule level that set the category; `unresolved` if no row covers the code |
| `schedule_row` | The covering row as printed: `0302.21`, `04.05` or `Chapter 47` |
| `pdf_page` | Page of that row in the source PDF (viewer page number) |
| `n_schedule_rows` | Number of category rows (sub-rows) that apply to the code |
| `categories` | All categories that apply, comma-separated (e.g. `A,X`) |
| `main_category` | Most frequent category among those rows |
| `base_rate_printed` | Base rate(s) as printed, e.g. `3.5%` or `1.6% / 1.2%`; blank if none |
| `row_ids` | `row_id`s in `mjepa_japan_schedule_rows.csv`, `;`-separated |
| `mixed_categories` | `TRUE` if the sub-rows carry more than one category |

The list of 5,223 codes is the HS 2002 six-digit universe as reported for
Japan's 2005 tariff in WITS/TRAINS (World Bank). Only the code list comes
from WITS; no tariff values are included.

### `mjepa_japan_schedule_rows.csv`

| Column | Meaning |
|---|---|
| `row_id` | Sequential identifier |
| `pdf_page` | Page in the source PDF |
| `level` | `chapter`, `heading` or `hs6` |
| `chapter`, `heading` | HS chapter (`NN`) and heading (`NN.NN`) of the row |
| `hs6` | HS6 code, for HS6-level rows only |
| `category` | Staging category in Column 4 (see `categories.csv`) |
| `base_rate_printed` | Column 3 as printed |
| `base_rate_pct` | Ad-valorem part of the base rate, percent; blank if none |
| `has_specific_duty` | `TRUE` if the base rate has a specific (per-unit) part |

## Summary

| `main_category` | HS6 codes |
|---|---|
| A (free from 2006) | 4,767 |
| X (excluded) | 176 |
| B7 | 86 |
| B10 | 58 |
| B5 | 45 |
| R (negotiation) | 44 |
| B15 | 41 |
| P | 5 |
| unresolved | 1 |

Category set by: chapter row 3,452 codes; heading row 998; HS6 row 772.

## Validation

A stratified random sample of 30 HS6 codes was checked against the PDF:
up to 3 codes for every combination of level (chapter, heading, HS6) and
outcome (liberalised, excluded, other). The check reads the PDF as plain
text, independently of the parser, and confirms for each code:

- the category and the printed base rate;
- that no more specific row exists for the code;
- the page number.

**Result: 30 of 30 correct.**

## Limitations

- **Yearly staging columns are not parsed.** The MITI copy prints one column
  per year with the rate in force that year; the dataset gives only the
  category and the base rate. Rates by year follow from the category
  (`categories.csv`) and the base rate.
- **Notes in Column 5 are not parsed.** Categories P, Q and R depend on
  these notes (tariff-rate quotas, seasonal rates, negotiation).
- **Mixed codes.** Where an HS6 has sub-rows with different categories
  (`mixed_categories = TRUE`), the sub-rows apply to parts of the code
  (national tariff lines). Use `schedule_rows` for the detail.
- **Not official.** Parsing errors are possible. Please report them as an
  issue.

## Citation

> Firdaus (2026). *MJEPA Schedule of Japan, parsed to HS6* [dataset].
> GitHub. <https://github.com/mfirdausali/mjepa-japan-schedule-data>

See `CITATION.cff`.

## Licence

Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code (`scripts/`): MIT. The underlying schedule is an international
agreement text published by the Governments of Japan and Malaysia.
