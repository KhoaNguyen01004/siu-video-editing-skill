# Free tools and MCP servers for Claude + CapCut (survey 2026-11-24)

Bottom line: **there is no official CapCut MCP for Claude.** CapCut's official AI route (announced 24 Oct 2026) is a
ChatGPT desktop plugin; it publishes no MCP endpoint or editing API. Every Claude route writes CapCut desktop draft files
on the same PC. Our pipeline (pycapcut + capcut_kit + computer-use for open/export) is proven on CapCut 9.8 and stays
the default. Re-check this page's claims when CapCut updates.

| Tool | What it is | Verdict for SIU work |
|---|---|---|
| **pycapcut 0.0.4** (GuanYixuan/pyCapCut, PyPI) | Python library that writes CapCut drafts: tracks, video/audio/text segments, keyframes, masks, transitions, text animations, filters, effects; template mode (load a real draft, replace media/text) | **Use (default).** Proven on 9.8. Pin 0.0.4 (0.1.0 changes the track API). No auto-export on CapCut ≥ 7 → export via computer-use. Some "free" enums are Pro in the app. |
| **capcut_kit.py** (this skill) | Our wrapper: source-time keyframes, string durations, text fitting with measured K, highlight ranges, SFX lanes, portable zip + installer | **Use.** Encodes every hand-over bug we hit. |
| **capcut-cli** (renezander030, MIT, Node, also `pip install capcut`) | CLI any agent can drive: `info`, `lint`, `diff` (incl. "what CapCut changed since my write"), `compile` from a JSON spec, `import-srt`, `caption` (Whisper), `loudness` gate, version-aware writes, `.bak` backups. Ships a `capcut-edit` agent skill | **Optional QA.** Worth installing when you need `lint` / `diff` on a draft (e.g. to see exactly what a client changed in a returned project). Not needed to build. Ask the user before installing (npm package from a community author). |
| **JmsLdrn/capcut-mcp** (MIT, Node, 17 tools) | MCP that edits existing drafts by cloning segment templates from a real draft; refuses to save while CapCut is open; validates | Optional for small edits to an existing draft from chat. Effects/transitions best-effort; needs a template draft with a text layer. Forks: Gusmares (filters, transitions, masks, keyframes, undo), RedmanOne/capcut-harness (pinned to 9.5). |
| VectCutAPI (sun-guannan, Apache-2.0) + wrappers (Atx-Guy, MigueDuque) | Python HTTP server (port 9001) + MCP mode: drafts, text, subtitles, effects, stickers, keyframes | Heavier (a server to run); its cloud render is not open source. No advantage over pycapcut for us. |
| alex28042/capcut-mcp, dlyrr/capcut-mcp | Light draft writers (7 tools; beat edits) | Too limited / experimental. |
| CapCut × ChatGPT plugin (official) | Builds a draft from chat inside ChatGPT desktop | Not usable from Claude. |
| Hosted render MCPs (e.g. Wireflow) | Cloud timeline + render | Paid credits, no CapCut project → does not meet the hand-over requirement. |
| Higgsfield MCP (connected in this account) | AI image/video generation, upscaling | Costs credits: ask first. Possible uses: upscale a blurry shot, an AI transition. Not needed for recaps. |
| **Remotion** (installed skills) | React video renderer | Use only for graphics CapCut cannot do, exported as transparent layers. |
| **HyperFrames** (installed skills) | HTML-based video compositions | Alternative to Remotion for motion-graphic layers / promos. |
| **faster-whisper** | Local ASR, language ID, forced alignment | Use (lang_id.py, score_text.py, music lyrics check). |
| **librosa** | Beats, bars, novelty | Use (music_check.py). |
| **rembg** | Person masks / cut-outs | Use (cutout.py, textcheck.py). |
| **ffmpeg** | Everything else (grading LUTs, interpolation, loudness) | Use. `drawtext` segfaults on this build: label with PIL. |
| computer-use MCP | Drive the CapCut window | Use for opening, checking and exporting (capcut-gui.md). |

## Why not switch to an MCP
- Building from one Python source of truth (cut list → draft) is reproducible: re-run after any change. MCP edits are
  imperative steps in a chat, hard to replay and review.
- The hard problems (source-time keyframes, text sizing, portable paths, Pro checks) are not solved by any of the MCPs.
- Drawback of our route: pycapcut lags CapCut versions; a CapCut auto-update can change the draft format. Mitigation:
  note the CapCut version in each project, open one draft after every CapCut update before a delivery.

## Sources
- wireflow.ai/blog/capcut-mcp (survey of servers, official ChatGPT plugin)
- github.com/JmsLdrn/capcut-mcp · github.com/renezander030/capcut-cli (docs/version-support.md) · github.com/GuanYixuan/pyCapCut
- usecarly.com/blog/claude-capcut-integration · aituber.app/blog/capcut-mcp-claude
