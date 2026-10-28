import json
import os
import time

import cv2
import gradio as gr
import numpy as np

import core
from styles import CSS, THEME

HERE = os.path.dirname(os.path.abspath(__file__))
CLASSES = core.CLASSES
EMOJI = {
    'angry': '😠', 'fear': '😨', 'happy': '😊',
    'neutral': '😐', 'sad': '😢', 'surprise': '😲',
}
TITLES = {'cnn': 'CNN · deep learning', 'svm': 'HOG + SVM · classic baseline'}
METRICS = json.load(open(os.path.join(HERE, 'test_metrics.json')))
SMOOTH_FRAMES = 7

LIVE_NOTE = ('Facial-expression classification, not emotion or stress detection. '
             'The SVM value is a relative score, not a calibrated probability.')


def chip(name):
    return (f'<span class="chip" style="--c:var(--emo-{name})">'
            f'{EMOJI[name]} {name.capitalize()}</span>')


def banner_html(text, tone, icon):
    return (f'<div class="banner {tone}"><span class="icon">{icon}</span>'
            f'<div class="banner-body">{text}</div></div>')


def _bars(probs):
    rows = ''
    for i, name in enumerate(CLASSES):
        pct = float(probs[i]) * 100
        top = ' top' if i == int(np.argmax(probs)) else ''
        rows += f'''
        <div class="bar-row{top}" style="--c:var(--emo-{name})">
          <div class="name">{EMOJI[name]} {name.capitalize()}</div>
          <div class="track"><div class="fill" style="--w:{pct:.1f}%"></div></div>
          <div class="pct">{pct:.1f}%</div>
        </div>'''
    return rows


def _ring(pct):
    return f'<div class="ring" style="--target:{pct:.1f}"><span>{pct:.0f}%</span></div>'


def result_card(probs, kind, agree, live=False, n_frames=0):
    top = int(np.argmax(probs))
    name = CLASSES[top]
    top_pct = float(probs[top]) * 100
    metric = 'Confidence' if kind == 'cnn' else 'Relative score'
    tag = ('<span class="tag">✓ agree</span>' if agree
           else '<span class="tag split">≠ differs</span>')
    note = ('Softmax output of the network.' if kind == 'cnn'
            else 'Relative score: softmax of SVM decision values, not a calibrated probability.')
    if live:
        frame_word = 'frame' if n_frames == 1 else 'frames'
        note = (f'Averaged over the last {n_frames} {frame_word} · '
                + ('CNN softmax confidence.' if kind == 'cnn'
                   else 'SVM relative score, not a calibrated probability.'))
    classes = 'result-card live' if live else 'result-card'
    classes += ' winner' if agree else ' split'
    return f'''
    <div class="{classes}" style="--c:var(--emo-{name})">
      <div class="card-kicker"><span>{TITLES[kind]}</span>{tag}</div>
      <div class="card-hero">
        <div class="emoji-bubble"><span class="emoji">{EMOJI[name]}</span></div>
        <div class="hero-copy">
          <div class="card-label">{name.capitalize()}</div>
          <div class="card-sub">{metric} · <b>{top_pct:.1f}%</b></div>
        </div>
        {_ring(top_pct)}
      </div>
      {_bars(probs)}
      <div class="card-note">{note}</div>
    </div>'''


def empty_card(kind, message='Results appear here after you press Analyze.'):
    icon = '🧠' if kind == 'cnn' else '📐'
    return f'''
    <div class="result-card empty">
      <div class="card-kicker"><span>{TITLES[kind]}</span></div>
      <div class="empty-emoji">{icon}</div>
      <p>{message}</p>
    </div>'''


EMPTY_BANNER = banner_html(
    '<b>Ready when you are.</b> Pick a photo or take a snapshot, then press '
    '<b>Analyze expression</b> to compare both models.'
    '<div class="steps"><span class="step"><span class="num">1</span>Upload or snap</span>'
    '<span class="step"><span class="num">2</span>Press Analyze</span>'
    '<span class="step"><span class="num">3</span>Compare the models</span></div>',
    'info', '👋')


def predict(img):
    if img is None:
        return (None, None, EMPTY_BANNER,
                empty_card('cnn'), empty_card('svm'))
    img = np.asarray(img)
    if img.ndim == 2:
        img = np.stack([img] * 3, axis=-1)
    img = img[..., :3].astype('uint8')

    out = core.analyze(img)
    face_view = cv2.resize(out['face48'], (192, 192), interpolation=cv2.INTER_NEAREST)

    msgs = ''
    if not out['face_found']:
        msgs += banner_html(
            '<b>No face detected</b>, so the whole image was used. Results may be unreliable. '
            'Try a clearer, front-facing photo.', 'warn', '🔍')

    agree = out['cnn_label'] == out['svm_label']
    if agree:
        msgs += banner_html(
            f'<b>Models agree:</b> {chip(CLASSES[out["cnn_label"]])} '
            'Both models read the same expression.', 'ok', '🎉')
    else:
        msgs += banner_html(
            f'<b>Models disagree:</b> CNN reads {chip(CLASSES[out["cnn_label"]])}, '
            f'while HOG + SVM reads {chip(CLASSES[out["svm_label"]])}. '
            'Expressions are often ambiguous, and the two methods learn different patterns.',
            'split', '🤔')

    return (out['annotated'], face_view, msgs,
            result_card(out['cnn_probs'], 'cnn', agree),
            result_card(out['svm_probs'], 'svm', agree))


# ---------------------------------------------------------------- live tab

def _live_status(fps, face, ms):
    if fps is None:
        fps_text = '— FPS'
    else:
        fps_text = f'{fps:.1f} FPS'
    if face:
        face_pill = '<span class="pill ok"><span class="dot"></span>Face detected</span>'
    else:
        face_pill = '<span class="pill warn"><span class="dot"></span>No face</span>'
    return f'''
    <div class="live-status">
      {face_pill}
      <span class="pill">⚡ {fps_text}</span>
      <span class="pill">⏱ {ms:.0f} ms / frame</span>
    </div>'''


IDLE_STATUS = '''
<div class="live-status">
  <span class="pill idle"><span class="dot"></span>Camera idle</span>
  <span class="pill">Click the camera once to allow access</span>
</div>'''


def live_empty_card():
    return f'''
    <div class="result-card live empty">
      <div class="card-kicker"><span>Live result</span></div>
      <div class="empty-emoji">📷</div>
      <p>Allow camera access once — predictions stream in here automatically.</p>
    </div>'''


def no_face_card():
    return f'''
    <div class="result-card live empty">
      <div class="card-kicker"><span>Live result</span></div>
      <div class="empty-emoji">🫥</div>
      <p><b>No face detected.</b> Move into the frame and face the camera.</p>
    </div>'''


LIVE_IDLE_BANNER = banner_html(
    '<b>Almost live.</b> Click the camera once to allow access — analysis starts '
    'automatically and predictions are smoothed over the last few frames.', 'info', '📹')


def live_predict(frame, state):
    now = time.time()
    st = dict(state or {})
    history = list(st.get('history', []))
    times = list(st.get('times', []))
    last_face = float(st.get('last_face', 0.0))
    misses = int(st.get('misses', 0))
    last_card = st.get('last_card')

    if frame is None:
        return st, IDLE_STATUS, LIVE_IDLE_BANNER, live_empty_card()

    img = np.asarray(frame)
    if img.ndim == 2:
        img = np.stack([img] * 3, axis=-1)
    img = img[..., :3].astype('uint8')

    started = time.perf_counter()
    out = core.analyze(img, detect_max_width=480)
    infer_ms = (time.perf_counter() - started) * 1000

    times = (times + [now])[-9:]
    fps = None
    if len(times) >= 2 and times[-1] > times[0]:
        fps = (len(times) - 1) / (times[-1] - times[0])

    if not out['face_found']:
        misses += 1
        if misses < 2 and last_card and (now - last_face) < 1.5:
            card = last_card
            banner = banner_html(
                '<b>Searching for a face…</b> Hold still and face the camera.', 'warn', '🔍')
        else:
            history = []
            card = no_face_card()
            banner = banner_html(
                '<b>No face detected.</b> Move into the frame and face the camera. '
                'The camera keeps running.', 'warn', '🫥')
        st.update(history=history, times=times, last_face=last_face,
                  misses=misses, last_card=card)
        return st, _live_status(fps, False, infer_ms), banner, card

    if history and (now - last_face) > 2.0:
        history = []
    if not history:
        misses = 0

    history = (history + [(out['cnn_probs'].tolist(), out['svm_probs'].tolist())])[-SMOOTH_FRAMES:]
    cnn_avg = np.mean([h[0] for h in history], axis=0)
    svm_avg = np.mean([h[1] for h in history], axis=0)
    cnn_label = int(np.argmax(cnn_avg))
    svm_label = int(np.argmax(svm_avg))
    agree = cnn_label == svm_label

    card = result_card(cnn_avg, 'cnn', agree, live=True, n_frames=len(history))
    extra = f'''
      <div class="svm-line">
        <span class="svm-label">HOG + SVM</span>
        {chip(CLASSES[svm_label])}
        <span class="muted">relative score {float(svm_avg[svm_label]) * 100:.1f}%</span>
      </div>'''
    card = card.replace('<div class="card-note">', extra + '<div class="card-note">')

    if agree:
        banner = banner_html(
            f'<b>Models agree:</b> {chip(CLASSES[cnn_label])} '
            'Both models read the same expression.', 'ok', '🎉')
    else:
        banner = banner_html(
            f'<b>Models disagree:</b> CNN reads {chip(CLASSES[cnn_label])}, '
            f'HOG + SVM reads {chip(CLASSES[svm_label])}.', 'split', '🤔')

    st.update(history=history, times=times, last_face=now,
              misses=0, last_card=card)
    return st, _live_status(fps, True, infer_ms), banner, card


# --------------------------------------------------------- comparison tab

def metrics_table():
    rows = ''
    for key, label in [('accuracy', 'Accuracy'), ('precision', 'Macro precision'),
                       ('recall', 'Macro recall'), ('f1', 'Macro F1')]:
        s, c = METRICS['SVM'][key] * 100, METRICS['CNN'][key] * 100
        rows += (f'<tr><td>{label}</td><td>{s:.1f}%</td>'
                 f'<td class="win">{c:.1f}%</td>'
                 f'<td class="gain">+{c - s:.1f} pts</td></tr>')
    rows += (f"<tr><td>Inference time / image</td><td>{METRICS['SVM']['ms_per_image']:.2f} ms</td>"
             f"<td class=\"win\">{METRICS['CNN']['ms_per_image']:.2f} ms</td><td></td></tr>")

    svm_acc = METRICS['SVM']['accuracy'] * 100
    cnn_acc = METRICS['CNN']['accuracy'] * 100
    return f'''
    <div class="comparison">
      <div class="model-cards">
        <div class="model-card">
          <div class="model-head">
            <span class="model-icon">📐</span>
            <div><h3>HOG + SVM</h3><p>Traditional machine learning baseline</p></div>
          </div>
          <div class="model-stats">
            <div><b>{svm_acc:.1f}%</b><span>accuracy</span></div>
            <div><b>{METRICS['SVM']['f1'] * 100:.1f}%</b><span>macro F1</span></div>
            <div><b>{METRICS['SVM']['ms_per_image']:.2f} ms</b><span>per image</span></div>
          </div>
          <div class="meter"><span style="--w:{svm_acc:.1f}%"></span></div>
        </div>
        <div class="model-card winner">
          <div class="model-head">
            <span class="model-icon">🧠</span>
            <div><h3>CNN</h3><p>Convolutional neural network</p></div>
            <span class="winner-badge">🏆 Winner</span>
          </div>
          <div class="model-stats">
            <div><b>{cnn_acc:.1f}%</b><span>accuracy</span></div>
            <div><b>{METRICS['CNN']['f1'] * 100:.1f}%</b><span>macro F1</span></div>
            <div><b>{METRICS['CNN']['ms_per_image']:.2f} ms</b><span>per image</span></div>
          </div>
          <div class="meter win"><span style="--w:{cnn_acc:.1f}%"></span></div>
        </div>
      </div>
      <div class="table-card">
        <h3>📊 Test-set results</h3>
        <p class="table-sub">Identical untouched test split · 7,067 images · 6 classes</p>
        <table class="metrics">
          <thead><tr><th>Metric</th><th>HOG + SVM</th>
            <th class="win">🏆 CNN</th><th>Gain</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <p class="fine-print">Speed note: the CNN ran batched on a GPU; the SVM time includes
        HOG feature extraction on CPU, so the speed gap is not a perfectly fair comparison.</p>
      </div>
    </div>'''


HEADER = f'''
<div class="hero">
  <div class="hero-copy">
    <div class="hero-eyebrow">🎭 FER-2013 · Bachelor AI project</div>
    <h1>Facial Expression Classifier</h1>
    <p>See what a CNN and a classic HOG + SVM baseline read in a face —
    live from your webcam or from a photo.</p>
    <div class="badges">
      <span class="badge">🗂️ FER-2013</span>
      <span class="badge">🧠 CNN vs HOG+SVM</span>
      <span class="badge">🎭 6 classes</span>
    </div>
  </div>
  <div class="hero-emojis" aria-hidden="true">
    {''.join(f'<span style="--i:{i}">{EMOJI[c]}</span>' for i, c in enumerate(CLASSES))}
  </div>
</div>'''

FOOTER = ('<div class="fer-footer">🌱 Facial-expression classification only — '
          'not a measure of real emotion or stress.</div>')

ABOUT = '''
### What this app does
It detects a face, crops it to 48×48 grayscale, and classifies the **visible facial expression**
into 6 classes: angry, fear, happy, neutral, sad, surprise.

### Important limitations
- **This is facial-expression classification, not emotion or stress detection.** A face's appearance does
  not reliably reveal what a person actually feels, and it cannot measure stress or diagnose anything.
- **Labels are noisy.** FER-2013 labels were crowd-sourced, and humans agree with them only about 65–70% of the time.
- **Accuracy is limited** (CNN: about 64% on 6 classes). `Fear` is the weakest class and is often confused
  with sad, angry or surprise.
- **Bias risk.** Models trained on one dataset may perform differently across ages, skin tones, lighting and
  cultures. Posed expressions differ from natural ones.
- **Not for decisions.** Do not use this for hiring, grading, surveillance, health or any decision about a person.

### Privacy
Images are processed in memory to produce a prediction and are not stored by this app.
In the Live tab, frames are processed one at a time and are not saved.

### Method
- Dataset: FER-2013 (disgust class removed: only 436 training images)
- Baseline: HOG features → standardize → PCA (200) → RBF SVM
- CNN: 4 conv blocks (BatchNorm, Dropout), augmentation, class weights, about 1.2M parameters
- Metrics: accuracy, macro precision/recall/F1, confusion matrix on an untouched test set
- Live view: face detection on a downscaled frame, CNN called directly, predictions averaged over 7 frames
'''

with gr.Blocks(title='Facial Expression Classifier') as demo:
    gr.HTML(HEADER)

    with gr.Tabs():
        with gr.Tab('Live'):
            gr.HTML(banner_html(LIVE_NOTE, 'info', '💡'))
            with gr.Row(equal_height=False):
                with gr.Column(scale=5, min_width=320, elem_classes='no-panel'):
                    cam = gr.Image(
                        sources=['webcam'], streaming=True, type='numpy',
                        label='Live camera', height=380,
                        elem_classes=['img-card', 'live-cam'],
                        placeholder='Click the camera button to start the live stream')
                    live_status = gr.HTML(IDLE_STATUS)
                    gr.HTML('<p class="fine-print">Analysis starts automatically after you allow '
                            'camera access. Good front lighting and a centered face give the '
                            'most stable predictions.</p>')
                with gr.Column(scale=5, min_width=320, elem_classes='no-panel'):
                    live_banner = gr.HTML(LIVE_IDLE_BANNER)
                    live_card = gr.HTML(live_empty_card())
            live_state = gr.State(value=None)
            cam.stream(
                live_predict,
                inputs=[cam, live_state],
                outputs=[live_state, live_status, live_banner, live_card],
                stream_every=0.16,
                concurrency_limit=1,
                time_limit=300,
                api_visibility='private',
                show_progress='hidden',
            )

        with gr.Tab('Upload'):
            with gr.Row(equal_height=False):
                with gr.Column(scale=5, min_width=300, elem_classes='no-panel'):
                    inp = gr.Image(
                        sources=['upload', 'webcam'], type='numpy',
                        label='Face photo', height=380,
                        placeholder='📷 Drop a face photo here, or browse / take a snapshot',
                        elem_classes=['img-card', 'upload-card'])
                    btn = gr.Button('🔍 Analyze expression', variant='primary',
                                    size='lg', elem_id='analyze-btn')
                with gr.Column(scale=5, min_width=300, elem_classes='no-panel'):
                    annotated = gr.Image(label='Detected face', height=290,
                                         interactive=False, buttons=[],
                                         elem_classes=['img-card', 'result-image'])
                    face = gr.Image(label='What the models see · 48×48 grayscale',
                                    height=170, interactive=False, buttons=[],
                                    elem_classes=['img-card', 'face48'])
            banner = gr.HTML(EMPTY_BANNER)
            with gr.Row(equal_height=True):
                with gr.Column(scale=1, min_width=300, elem_classes='no-panel'):
                    cnn_out = gr.HTML(empty_card('cnn'))
                with gr.Column(scale=1, min_width=300, elem_classes='no-panel'):
                    svm_out = gr.HTML(empty_card('svm'))
            gr.HTML('<p class="fine-print">The CNN confidence is its softmax output. '
                    'The SVM value is a relative score, not a calibrated probability. '
                    'Facial-expression classification only: not a measure of real emotion or stress.</p>')
            btn.click(predict, inp, [annotated, face, banner, cnn_out, svm_out])

        with gr.Tab('Compare'):
            gr.HTML(metrics_table())
            with gr.Row(equal_height=True):
                with gr.Column(scale=1, min_width=300, elem_classes='no-panel'):
                    gr.Image(os.path.join(HERE, 'model_comparison.png'),
                             label='Metric comparison', interactive=False, buttons=[],
                             elem_classes=['img-card', 'chart-card'])
                with gr.Column(scale=1, min_width=300, elem_classes='no-panel'):
                    gr.Image(os.path.join(HERE, 'confusion_matrices.png'),
                             label='Confusion matrices · rows = true class, normalized',
                             interactive=False, buttons=[],
                             elem_classes=['img-card', 'chart-card'])
            with gr.Column(elem_classes='no-panel'):
                gr.Image(os.path.join(HERE, 'class_distribution.png'),
                         label='Training data · class distribution',
                         interactive=False, buttons=[],
                         elem_classes=['img-card', 'chart-card'])

        with gr.Tab('About'):
            gr.Markdown(ABOUT, elem_classes='about-card')

    gr.HTML(FOOTER)

AUTO_START_JS = '''
(() => {
  let started = false;
  const maybeStart = () => {
    if (started) return;
    const cam = document.querySelector('.live-cam');
    if (!cam) return;
    const btn = cam.querySelector('button.capture-button');
    if (!btn) return;
    started = true;
    setTimeout(() => {
      if (document.body.contains(btn)) btn.click();
    }, 250);
  };
  const observer = new MutationObserver(maybeStart);
  observer.observe(document.body, { childList: true, subtree: true });
  setInterval(maybeStart, 1200);
  maybeStart();
})();
'''

if __name__ == '__main__':
    demo.launch(theme=THEME, css=CSS, js=AUTO_START_JS)
