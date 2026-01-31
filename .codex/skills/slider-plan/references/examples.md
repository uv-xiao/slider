# Example plans (v2)

## Example 1: Material → PDF/PPTX

- Input: `materials/code-agent-huawei/`
- Output: `artifacts/code-agent-huawei/code-agent-huawei.pdf` + `.pptx`

Plan action items should include:

- `$content-prompts` → `prompts/content/code-agent-huawei.md`
- Prompt review gate
- `$styled-prompts` with `styles/<style>.md` → `prompts/styled/code-agent-huawei.md`
- Prompt review gate
- `$styled-artifacts` → `artifacts/code-agent-huawei/work/` + final PDF/PPTX

## Example 2: Styled prompt → PDF only

- Input: `prompts/styled/mydeck.md`
- Output: `artifacts/mydeck/mydeck.pdf`

Plan action items should include:

- Review `prompts/styled/mydeck.md` (no artifact regeneration loop)
- `$styled-artifacts` with `--pdf artifacts/mydeck/mydeck.pdf` (optionally skip `--pptx`)
