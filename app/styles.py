"""Visual design for the Gradio app: theme, CSS variables and component styles.

Only presentation lives here. app.py imports THEME, CSS and EMOTION_COLORS.
"""
import gradio as gr

# Per-emotion colours, used for bars, chips and the confidence ring.
# Each entry is (light-mode colour, dark-mode colour).
EMOTION_COLORS = {
    'angry':    ('#E5484D', '#FF7276'),
    'fear':     ('#8E6BD8', '#A98BF0'),
    'happy':    ('#E8A317', '#FFC14D'),
    'neutral':  ('#7D8DA3', '#A3B1C4'),
    'sad':      ('#4C78A8', '#7AA3D6'),
    'surprise': ('#16A89A', '#3FD1C0'),
}

_emo_light = '\n'.join(f'  --emo-{k}: {v[0]};' for k, v in EMOTION_COLORS.items())
_emo_dark = '\n'.join(f'  --emo-{k}: {v[1]};' for k, v in EMOTION_COLORS.items())

THEME = gr.themes.Soft(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.purple,
    neutral_hue=gr.themes.colors.slate,
    radius_size=gr.themes.sizes.radius_lg,
    font=[gr.themes.GoogleFont('Inter'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
).set(
    body_background_fill='linear-gradient(135deg, #EEF4FF 0%, #F9F0FB 48%, #FFF3E9 100%)',
    body_background_fill_dark='linear-gradient(135deg, #0D1220 0%, #151329 55%, #211923 100%)',
    body_text_color='#1F2A3D',
    body_text_color_dark='#E9EDF6',
    body_text_color_subdued='#647089',
    body_text_color_subdued_dark='#A3AEC2',
    block_background_fill='rgba(255,255,255,0.78)',
    block_background_fill_dark='rgba(27,32,48,0.78)',
    block_border_width='1px',
    block_border_color='rgba(76,120,168,0.13)',
    block_border_color_dark='rgba(255,255,255,0.08)',
    block_radius='22px',
    container_radius='22px',
    input_radius='14px',
    block_shadow='0 10px 30px rgba(76,120,168,0.10)',
    block_shadow_dark='0 10px 30px rgba(0,0,0,0.35)',
    block_title_text_weight='700',
    button_large_radius='14px',
    button_primary_background_fill='linear-gradient(135deg, #4C78A8 0%, #6A93C8 100%)',
    button_primary_background_fill_hover='linear-gradient(135deg, #416B99 0%, #5A83B8 100%)',
    button_primary_background_fill_dark='linear-gradient(135deg, #4C78A8 0%, #7199CE 100%)',
    button_primary_background_fill_hover_dark='linear-gradient(135deg, #5A86B8 0%, #82A8DA 100%)',
    button_primary_text_color='white',
    button_primary_text_color_dark='white',
    layout_gap='18px',
)

CSS = f"""
/* ---------- design tokens ---------- */
:root {{
  --accent: #4C78A8;
  --accent-deep: #2F5585;
  --accent-soft: rgba(76,120,168,0.11);
  --warm: #E07A5F;
  --warm-soft: rgba(224,122,95,0.13);
  --ok: #2E9E6A;
  --ok-soft: rgba(46,158,106,0.12);
  --amber: #D98A0B;
  --amber-soft: rgba(217,138,11,0.13);
  --text: #1F2A3D;
  --muted: #647089;
  --card: rgba(255,255,255,0.78);
  --card-solid: #FFFFFF;
  --line: rgba(76,120,168,0.13);
  --track: rgba(76,120,168,0.11);
  --shadow: 0 10px 30px rgba(76,120,168,0.11), 0 2px 6px rgba(31,42,61,0.04);
  --shadow-lift: 0 18px 44px rgba(76,120,168,0.18);
  --radius: 24px;
  --radius-sm: 16px;
{_emo_light}
}}
.dark {{
  --accent-soft: rgba(122,163,214,0.13);
  --warm: #F09073;
  --warm-soft: rgba(240,144,115,0.15);
  --ok: #4CC98E;
  --ok-soft: rgba(76,201,142,0.14);
  --amber: #FFB547;
  --amber-soft: rgba(255,181,71,0.14);
  --text: #E9EDF6;
  --muted: #A3AEC2;
  --card: rgba(27,32,48,0.80);
  --card-solid: #1B2030;
  --line: rgba(255,255,255,0.09);
  --track: rgba(255,255,255,0.08);
  --shadow: 0 10px 30px rgba(0,0,0,0.38), 0 2px 6px rgba(0,0,0,0.18);
  --shadow-lift: 0 18px 44px rgba(0,0,0,0.45);
{_emo_dark}
}}

/* ---------- page shell ---------- */
body {{
  background-attachment: fixed !important;
  min-height: 100vh;
}}
.gradio-container {{
  max-width: 1180px !important;
  margin: 0 auto !important;
  padding: clamp(14px, 3vw, 30px) clamp(12px, 3vw, 24px) 44px !important;
  background: transparent !important;
}}
.gradio-container, .gradio-container * {{
  font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif !important;
}}
/* let tab content shrink to the viewport instead of widening the page */
.gradio-container .tabs, .gradio-container .tabitem, .gradio-container main,
.gradio-container .tab-wrapper, .gradio-container .tab-container {{
  min-width: 0 !important;
}}
.gradio-container .tab-wrapper {{ height: auto !important; }}
.gradio-container .tab-container {{
  flex-wrap: wrap !important; width: 100% !important; height: auto !important;
  overflow: visible !important;
}}
.no-panel {{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}}

/* ---------- hero ---------- */
.hero {{
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  padding: clamp(26px, 4.4vw, 46px) clamp(22px, 4.4vw, 48px);
  border-radius: 30px;
  color: #fff;
  background:
    radial-gradient(520px 240px at 88% -20%, rgba(255,255,255,0.24), transparent 70%),
    radial-gradient(360px 260px at -10% 120%, rgba(255,214,196,0.24), transparent 70%),
    linear-gradient(118deg, #3E6C9C 0%, #4C78A8 36%, #7A82C4 68%, #C88BA9 105%);
  box-shadow: 0 22px 54px rgba(76,120,168,0.30);
}}
.hero::after {{
  content: '';
  position: absolute;
  right: 10%;
  top: -90px;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  background: rgba(255,255,255,0.10);
  filter: blur(2px);
}}
.hero-copy {{ position: relative; z-index: 1; max-width: 720px; }}
.hero-eyebrow {{
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: rgba(255,255,255,0.96);
  background: rgba(255,255,255,0.16);
  border: 1px solid rgba(255,255,255,0.26);
  backdrop-filter: blur(6px);
}}
.hero h1 {{
  margin: 14px 0 10px;
  color: #fff !important;
  font-size: clamp(28px, 4.8vw, 46px);
  font-weight: 800;
  line-height: 1.06;
  letter-spacing: -0.5px;
}}
.hero p {{
  margin: 0 0 18px;
  max-width: 640px;
  color: rgba(255,255,255,0.92) !important;
  font-size: clamp(14px, 2vw, 17px);
  line-height: 1.6;
}}
.badges {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 13px;
  border-radius: 999px;
  font-size: 12.5px;
  font-weight: 700;
  color: #fff;
  background: rgba(255,255,255,0.17);
  border: 1px solid rgba(255,255,255,0.30);
  backdrop-filter: blur(6px);
}}
.hero-emojis {{
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, 58px);
  gap: 11px;
  flex: none;
}}
.hero-emojis span {{
  display: grid;
  place-items: center;
  width: 58px;
  height: 58px;
  border-radius: 19px;
  font-size: 27px;
  background: rgba(255,255,255,0.17);
  border: 1px solid rgba(255,255,255,0.30);
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 18px rgba(20,40,70,0.12);
  animation: fer-float 5.5s ease-in-out infinite;
  animation-delay: calc(var(--i) * -0.75s);
}}

/* ---------- tabs ---------- */
.gradio-container [role="tablist"] {{
  gap: 5px;
  border-bottom: none !important;
  padding: 7px 0 15px;
}}
.gradio-container button[role="tab"] {{
  border-radius: 999px !important;
  padding: 9px 17px !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  color: var(--muted) !important;
  background: transparent !important;
  border: 1px solid transparent !important;
  transition: background .18s ease, color .18s ease, box-shadow .18s ease;
}}
.gradio-container button[role="tab"]:hover {{
  background: var(--accent-soft) !important;
  color: var(--text) !important;
}}
.gradio-container button[role="tab"][aria-selected="true"],
.gradio-container button[role="tab"].selected {{
  background: var(--accent) !important;
  color: #fff !important;
  box-shadow: 0 6px 16px rgba(76,120,168,0.32);
}}
.gradio-container button[role="tab"][aria-selected="true"]::after,
.gradio-container button[role="tab"].selected::after {{ display: none !important; }}
.tabitem {{ padding-top: 6px !important; }}

/* ---------- buttons ---------- */
#analyze-btn {{
  margin-top: 12px;
  font-size: 17px !important;
  font-weight: 800 !important;
  letter-spacing: .2px;
  padding: 13px 0 !important;
  border: none !important;
  box-shadow: 0 10px 22px rgba(76,120,168,0.32) !important;
  transition: transform .15s ease, box-shadow .15s ease, filter .15s ease !important;
}}
#analyze-btn:hover {{
  transform: translateY(-2px);
  box-shadow: 0 14px 28px rgba(76,120,168,0.40) !important;
  filter: brightness(1.04);
}}
#analyze-btn:active {{
  transform: translateY(1px) scale(.99);
  box-shadow: 0 5px 12px rgba(76,120,168,0.28) !important;
}}

/* ---------- image containers ---------- */
.img-card {{
  border-radius: var(--radius) !important;
  overflow: hidden;
  border: 1px solid var(--line) !important;
  background: var(--card) !important;
  box-shadow: var(--shadow);
}}
.img-card img, .img-card video {{
  border-radius: var(--radius-sm);
  object-fit: cover;
}}
.live-cam video {{
  border-radius: 18px;
  width: 100%;
}}
.live-cam {{
  border: 1px solid color-mix(in srgb, var(--accent) 26%, transparent) !important;
}}
.face48 img {{ image-rendering: pixelated; }}
.chart-card {{ overflow: hidden; }}
.chart-card img {{
  background: #fff;
  border-radius: var(--radius-sm);
  padding: 7px;
}}

/* ---------- banners ---------- */
.banner {{
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 18px;
  margin: 6px 0;
  color: var(--text);
  font-size: 15px;
  line-height: 1.5;
  border: 1px solid var(--line);
}}
.banner .icon {{
  flex: none;
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 12px;
  font-size: 18px;
  background: rgba(255,255,255,0.55);
}}
.dark .banner .icon {{ background: rgba(255,255,255,0.08); }}
.banner-body {{ flex: 1; min-width: 0; padding-top: 3px; }}
.banner.ok {{
  background: var(--ok-soft);
  border-color: color-mix(in srgb, var(--ok) 34%, transparent);
}}
.banner.warn {{
  background: var(--amber-soft);
  border-color: color-mix(in srgb, var(--amber) 34%, transparent);
}}
.banner.info {{
  background: var(--accent-soft);
  border-color: color-mix(in srgb, var(--accent) 30%, transparent);
}}
.banner.split {{
  background: var(--warm-soft);
  border-color: color-mix(in srgb, var(--warm) 36%, transparent);
}}
.banner b {{ color: inherit; }}

/* empty-state steps */
.steps {{ display: flex; flex-wrap: wrap; gap: 9px; margin-top: 10px; }}
.step {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border-radius: 999px;
  background: var(--card-solid);
  border: 1px solid var(--line);
  font-size: 13px;
  font-weight: 700;
}}
.step .num {{
  width: 21px;
  height: 21px;
  border-radius: 50%;
  display: inline-grid;
  place-items: center;
  background: var(--accent);
  color: #fff;
  font-size: 11px;
}}

/* ---------- live status ---------- */
.live-status {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
.pill {{
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 13px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
  background: var(--card);
  border: 1px solid var(--line);
  box-shadow: 0 3px 10px rgba(76,120,168,0.07);
}}
.pill .dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--muted);
}}
.pill.ok .dot {{
  background: var(--ok);
  box-shadow: 0 0 0 4px var(--ok-soft);
  animation: fer-pulse 1.8s ease-in-out infinite;
}}
.pill.warn .dot {{
  background: var(--amber);
  box-shadow: 0 0 0 4px var(--amber-soft);
  animation: fer-pulse 1.2s ease-in-out infinite;
}}
.pill.idle .dot {{ background: var(--muted); }}

/* ---------- result cards ---------- */
.result-card {{
  position: relative;
  height: 100%;
  box-sizing: border-box;
  padding: 20px 22px;
  border-radius: var(--radius);
  background: var(--card);
  border: 1px solid var(--line);
  box-shadow: var(--shadow);
  color: var(--text);
  overflow: hidden;
}}
.result-card::before {{
  content: '';
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, var(--c, var(--accent)), transparent 85%);
  opacity: .75;
}}
.result-card:not(.live):not(.empty) {{ animation: fer-pop .35s ease both; }}
.result-card.winner {{
  border-color: color-mix(in srgb, var(--ok) 45%, transparent);
  box-shadow: 0 0 0 4px var(--ok-soft), var(--shadow);
}}
.result-card.split {{
  border-color: color-mix(in srgb, var(--warm) 45%, transparent);
  box-shadow: 0 0 0 4px var(--warm-soft), var(--shadow);
}}
.card-kicker {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 1.15px;
  text-transform: uppercase;
  color: var(--muted);
}}
.tag {{
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 10.5px;
  letter-spacing: .5px;
  background: var(--ok-soft);
  color: var(--ok);
}}
.tag.split {{ background: var(--warm-soft); color: var(--warm); }}
.card-hero {{
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 14px 0 15px;
}}
.emoji-bubble {{
  flex: none;
  display: grid;
  place-items: center;
  width: 74px;
  height: 74px;
  border-radius: 24px;
  background: color-mix(in srgb, var(--c, var(--accent)) 14%, transparent);
  border: 1px solid color-mix(in srgb, var(--c, var(--accent)) 22%, transparent);
}}
.card-hero .emoji {{
  font-size: 44px;
  line-height: 1;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.12));
}}
.hero-copy {{ flex: 1; min-width: 0; }}
.card-label {{
  font-size: clamp(25px, 3.6vw, 33px);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.3px;
  color: var(--c, var(--accent));
}}
.card-sub {{ font-size: 13.5px; color: var(--muted); margin-top: 3px; }}
.card-sub b {{ color: var(--text); }}

/* confidence ring */
@property --p {{ syntax: '<number>'; inherits: false; initial-value: 0; }}
.ring {{
  --p: var(--target);
  flex: none;
  margin-left: auto;
  width: 74px;
  height: 74px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: conic-gradient(var(--c, var(--accent)) calc(var(--p) * 1%), var(--track) 0);
}}
.result-card:not(.live) .ring {{ animation: fer-ring 1s cubic-bezier(.2,.8,.2,1) both; }}
.ring span {{
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--card-solid);
  font-weight: 800;
  font-size: 14px;
  color: var(--text);
}}

/* bars */
.bar-row {{
  display: grid;
  grid-template-columns: 105px 1fr 52px;
  align-items: center;
  gap: 10px;
  margin: 8px 0;
  font-size: 14px;
}}
.bar-row .name {{ white-space: nowrap; color: var(--muted); }}
.bar-row .pct {{
  text-align: right;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
}}
.bar-row.top .name, .bar-row.top .pct {{ font-weight: 800; color: var(--text); }}
.track {{
  height: 10px;
  border-radius: 999px;
  background: var(--track);
  overflow: hidden;
}}
.fill {{
  height: 100%;
  width: var(--w);
  border-radius: 999px;
  background: var(--c, var(--accent));
  opacity: .55;
}}
.result-card:not(.live) .fill {{
  animation: fer-grow .8s cubic-bezier(.2,.8,.2,1) both;
}}
.bar-row.top .fill {{
  opacity: 1;
  box-shadow: 0 0 12px color-mix(in srgb, var(--c, var(--accent)) 55%, transparent);
}}
.result-card.live .fill {{ transition: width .35s ease; }}

.card-note {{
  margin-top: 12px;
  font-size: 12px;
  color: var(--muted);
  line-height: 1.45;
}}
.svm-line {{
  display: flex;
  align-items: center;
  gap: 9px;
  flex-wrap: wrap;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--line);
  font-size: 13.5px;
}}
.svm-label {{
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--muted);
}}
.muted {{ color: var(--muted); font-size: 12.5px; }}

.chip {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 10px;
  border-radius: 999px;
  font-weight: 800;
  color: var(--c, var(--accent));
  background: color-mix(in srgb, var(--c, var(--accent)) 15%, transparent);
}}

.result-card.empty {{
  text-align: center;
  padding: 34px 22px;
  border-style: dashed;
  box-shadow: none;
}}
.result-card.empty::before {{ display: none; }}
.empty-emoji {{
  font-size: 44px;
  line-height: 1;
  margin: 16px 0 4px;
  display: inline-block;
  animation: fer-float 3.5s ease-in-out infinite;
}}
.result-card.empty p {{ color: var(--muted); margin: 6px 0 0; line-height: 1.5; }}

.fine-print {{
  font-size: 12.5px;
  color: var(--muted);
  margin: 8px 4px 0;
  line-height: 1.55;
}}

/* ---------- comparison tab ---------- */
.comparison {{ display: flex; flex-direction: column; gap: 18px; }}
.model-cards {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
}}
.model-card {{
  padding: 20px 22px;
  border-radius: var(--radius);
  background: var(--card);
  border: 1px solid var(--line);
  box-shadow: var(--shadow);
  color: var(--text);
}}
.model-card.winner {{
  border-color: color-mix(in srgb, var(--ok) 48%, transparent);
  box-shadow: 0 0 0 4px var(--ok-soft), var(--shadow);
}}
.model-head {{ display: flex; align-items: center; gap: 12px; }}
.model-icon {{
  flex: none;
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 15px;
  font-size: 22px;
  background: var(--accent-soft);
}}
.model-card.winner .model-icon {{ background: var(--ok-soft); }}
.model-head h3 {{ margin: 0; font-size: 18px; font-weight: 800; }}
.model-head p {{ margin: 2px 0 0; font-size: 12.5px; color: var(--muted); }}
.winner-badge {{
  margin-left: auto;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  color: var(--ok);
  background: var(--ok-soft);
  white-space: nowrap;
}}
.model-stats {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin: 18px 0 14px;
}}
.model-stats b {{
  display: block;
  font-size: clamp(18px, 2.6vw, 24px);
  font-weight: 800;
  line-height: 1.1;
  color: var(--text);
}}
.model-stats span {{
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .55px;
  color: var(--muted);
}}
.meter {{
  height: 8px;
  border-radius: 999px;
  background: var(--track);
  overflow: hidden;
}}
.meter span {{
  display: block;
  width: var(--w);
  height: 100%;
  border-radius: 999px;
  background: var(--accent);
}}
.meter.win span {{ background: var(--ok); }}

.table-card {{
  padding: 20px 22px;
  border-radius: var(--radius);
  background: var(--card);
  border: 1px solid var(--line);
  box-shadow: var(--shadow);
  overflow-x: auto;
  color: var(--text);
}}
.table-card h3 {{ margin: 0; color: var(--text); font-size: 20px; font-weight: 800; }}
.table-sub {{ margin: 5px 0 16px; font-size: 13px; color: var(--muted); }}
.metrics {{
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 15px;
  color: var(--text);
  background: transparent !important;
  border: none !important;
}}
.metrics th, .metrics td {{
  padding: 12px 14px;
  text-align: left;
  background: transparent;
  border: none !important;
  border-bottom: 1px solid var(--line) !important;
}}
.metrics th {{
  font-size: 11.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .75px;
  color: var(--muted);
}}
.metrics td {{ font-variant-numeric: tabular-nums; }}
.metrics tr {{ background: transparent !important; border: none !important; }}
.metrics tbody tr:last-child td {{ border-bottom: none !important; }}
.metrics .win {{
  background: var(--ok-soft);
  font-weight: 800;
}}
.metrics th.win {{
  color: var(--ok);
  border-radius: 12px 12px 0 0;
}}
.metrics tbody tr:last-child td.win {{ border-radius: 0 0 12px 12px; }}
.metrics .gain {{ color: var(--accent); font-weight: 800; white-space: nowrap; }}
.dark .metrics .gain {{ color: var(--emo-sad); }}
.metrics tbody tr:hover td {{ background: var(--accent-soft); }}
.metrics tbody tr:hover td.win {{
  background: color-mix(in srgb, var(--ok) 20%, transparent);
}}

/* ---------- about tab ---------- */
.about-card {{
  padding: clamp(20px, 3.4vw, 34px) !important;
  border-radius: var(--radius) !important;
  background: var(--card) !important;
  border: 1px solid var(--line) !important;
  box-shadow: var(--shadow);
  color: var(--text) !important;
}}
.about-card h3 {{
  margin: 26px 0 10px !important;
  color: var(--accent) !important;
  font-size: 20px !important;
  font-weight: 800 !important;
}}
.dark .about-card h3 {{ color: var(--emo-sad) !important; }}
.about-card h3:first-child {{ margin-top: 0 !important; }}
.about-card p, .about-card li {{
  color: var(--text) !important;
  line-height: 1.7 !important;
}}
.about-card strong {{ color: var(--accent-deep) !important; }}
.dark .about-card strong {{ color: var(--emo-sad) !important; }}
.about-card ul {{ padding-left: 22px; }}

/* ---------- footer ---------- */
.fer-footer {{
  text-align: center;
  margin: 22px auto 0;
  padding: 13px 20px;
  border-radius: 999px;
  max-width: 680px;
  background: var(--card);
  border: 1px solid var(--line);
  color: var(--muted);
  font-size: 13.5px;
  font-weight: 600;
}}

/* ---------- animations ---------- */
@keyframes fer-grow  {{ from {{ width: 0; }} }}
@keyframes fer-ring  {{ from {{ --p: 0; }} }}
@keyframes fer-pop   {{ from {{ opacity: 0; transform: translateY(7px) scale(.99); }} }}
@keyframes fer-float {{ 50% {{ transform: translateY(-5px); }} }}
@keyframes fer-pulse {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: .45; }}
}}
@media (prefers-reduced-motion: reduce) {{
  .fill, .ring, .result-card, .banner, .empty-emoji, .hero-emojis span, .pill .dot {{
    animation: none !important;
    transition: none !important;
  }}
}}

/* ---------- phone width ---------- */
@media (max-width: 760px) {{
  .hero-emojis {{ display: none; }}
  .hero {{ border-radius: 24px; }}
}}
@media (max-width: 640px) {{
  .gradio-container {{ padding: 10px 12px 32px !important; }}
  .hero {{ padding: 24px 20px; }}
  .hero h1 {{ margin-top: 12px; }}
  .card-hero {{ gap: 10px; }}
  .emoji-bubble {{ width: 60px; height: 60px; border-radius: 19px; }}
  .card-hero .emoji {{ font-size: 35px; }}
  .ring {{ width: 62px; height: 62px; }}
  .ring span {{ width: 48px; height: 48px; font-size: 12px; }}
  .bar-row {{ grid-template-columns: 88px 1fr 46px; font-size: 13px; }}
  .result-card {{ padding: 17px 16px; }}
  .model-card, .table-card {{ padding: 16px; }}
  .metrics {{ font-size: 13.5px; }}
  .metrics th, .metrics td {{ padding: 9px 8px; }}
  .metrics th {{ font-size: 10.5px; }}
  .pill {{ padding: 6px 11px; font-size: 12px; }}
  .gradio-container button[role="tab"] {{ padding: 8px 13px !important; font-size: 13px !important; }}
}}
"""
