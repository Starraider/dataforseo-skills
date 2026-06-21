# SEO Text Keyword Optimization

This skill analyzes supplied prose against one to three seed keywords, retrieves up to 50 related Google keywords per seed through DataForSEO MCP, deduplicates and filters the combined pool, and ranks up to 20 low-hanging-fruit opportunities using search volume and organic keyword difficulty.

It then produces three distinct optimization approaches for the original text. Each approach maps selected keywords to concrete headings, passages, or additions while preserving the text's factual boundaries and voice.

## Inputs

- Complete pasted text or a readable local text/Markdown file.
- One to three seed keywords.
- Optional DataForSEO location and language; defaults are United States and English.
- Optional report root; the default is `SEO/` under the current working directory.

## Output

The Markdown report includes DataForSEO call costs and coverage, deduplication and exclusion counts, a sorted opportunity table with volume and organic difficulty, current-text coverage, three optimization approaches, one recommendation, methodology, and limitations. Search volume is treated as demand rather than guaranteed traffic.

The default path is:

`SEO/text-keyword-optimization/<YYYY-MM-DD>_Text-Keyword-Optimization_<safe-first-seed>.md`

## Example prompts

- Optimize this blog post for `heat pump maintenance` and `heat pump service`; find 20 low-hanging-fruit keywords and give me three approaches.
- Analyze the article in `draft.md` using the seeds `remote onboarding`, `virtual onboarding`, and `employee onboarding` for Germany and English.
- Find related opportunities for this news analysis and propose a light edit, structural revision, and expanded version.

## Requirements

Configure the official DataForSEO MCP server with the `DATAFORSEO_LABS` module and credentials. Filesystem write access is required for the report.
