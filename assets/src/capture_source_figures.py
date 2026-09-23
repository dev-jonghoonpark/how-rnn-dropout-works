# -*- coding: utf-8 -*-
"""how-rnn-dropout-works/index.html 안의 canvas 데모(그림 1~3)를 PNG로 캡처한다.
헤드리스 Chromium 2패스: 1패스에서 요소 크기를 재고, 2패스에서 그 크기로 스크린샷.
"""
import os, re, subprocess, tempfile

CHROME = os.path.expanduser('~/.cache/ms-playwright/chromium-1107/chrome-linux/chrome')
SRC = '/home/jonghoonpark/claude-rc/how-rnn-dropout-works/index.html'
OUT = '/home/jonghoonpark/claude-rc/rnn-dropout-figures/source-figures'
TMP = tempfile.mkdtemp(prefix='figshot-')

FONTCONF = os.path.join(TMP, 'fonts.conf')
open(FONTCONF, 'w').write('''<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
  <alias><family>sans-serif</family><prefer><family>Pretendard</family></prefer></alias>
  <alias><family>system-ui</family><prefer><family>Pretendard</family></prefer></alias>
</fontconfig>''')
ENV = dict(os.environ, FONTCONFIG_FILE=FONTCONF)

HTML = open(SRC, encoding='utf-8').read()

INJECT = '''
<script>
(function(){
  var SEL = %(sel)s, THEME = %(theme)s, ACTION = %(action)s;
  document.documentElement.dataset.theme = THEME;
  function go(){
    if (ACTION) { try { ACTION(); } catch(e) {} }
    setTimeout(function(){
      var el = document.querySelector(SEL).closest('.demo');
      var body = document.body;
      while (body.firstChild) body.removeChild(body.firstChild);
      body.appendChild(el);
      body.style.cssText = 'margin:0;padding:20px;background:var(--bg);display:inline-block';
      el.style.margin = '0'; el.style.maxWidth = 'none'; el.style.width = '840px';
      var need = 840;
      el.querySelectorAll('.scrollx, .panel, canvas, table').forEach(function(n){
        need = Math.max(need, n.scrollWidth + 40);
      });
      el.style.width = need + 'px';
      var r = el.getBoundingClientRect();
      document.title = 'SIZE:' + Math.ceil(r.width + 40) + 'x' + Math.ceil(r.height + 40);
    }, 250);
  }
  if (document.readyState === 'complete') go();
  else window.addEventListener('load', go);
})();
</script>
'''

SPECS = [
    ('g1-two-kinds-of-arrows',        '#g1canvas', 'null'),
    ('g1-vertical-only',              '#g1canvas', "function(){document.querySelector('button.g1mode[data-m=\\\"vert\\\"]').click();}"),
    ('g1-horizontal-only',            '#g1canvas', "function(){document.querySelector('button.g1mode[data-m=\\\"horiz\\\"]').click();}"),
    ('g2-adding-a-layer',             '#g2canvas', 'null'),
    ('g3-mask-on-one-report',         '#g3grid',   'null'),
]


def run(args, capture=False):
    return subprocess.run([CHROME, '--headless=old', '--disable-gpu', '--no-sandbox',
                           '--hide-scrollbars', '--allow-file-access-from-files'] + args,
                          env=ENV, capture_output=True, text=True, timeout=120)


for name, sel, action in SPECS:
    for theme in ('light', 'dark'):
        page = os.path.join(TMP, f'{name}-{theme}.html')
        inj = INJECT % dict(sel=f"'{sel}'", theme=f"'{theme}'", action=action)
        open(page, 'w', encoding='utf-8').write(HTML + inj)
        url = 'file://' + page
        # 1패스: 요소 크기 측정
        dom = run(['--virtual-time-budget=4000', '--dump-dom', '--window-size=1500,1200', url],
                  capture=True).stdout
        m = re.search(r'SIZE:(\d+)x(\d+)', dom)
        if not m:
            print('  !! size 측정 실패:', name, theme); continue
        w, h = m.group(1), m.group(2)
        # 2패스: 실제 크기로 2x 스크린샷
        png = os.path.join(OUT, f'{name}-{theme}.png')
        run(['--virtual-time-budget=4000', '--force-device-scale-factor=2',
             f'--window-size={w},{h}', f'--screenshot={png}', url])
        print(f'{os.path.basename(png)}  {w}x{h} @2x')
