# -*- coding: utf-8 -*-
"""RNN 드롭아웃 설명용 순서도 2종 (light/dark) SVG 생성.
색 토큰과 폰트는 how-rnn-dropout-works/index.html 의 :root 토큰을 그대로 따른다.
  --s1 = 세로(비순환 연결) · --s2 = 가로(순환 연결/기억) · --crit = 끊긴 곳
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

FONT = ("Pretendard, -apple-system, BlinkMacSystemFont, 'Apple SD Gothic Neo', "
        "'Segoe UI', 'Noto Sans KR', 'Malgun Gothic', sans-serif")

THEMES = {
    'light': dict(bg='#f6f7f5', surface='#fdfdfc', surface2='#eff1ee', ink='#171a18',
                  ink2='#565b57', muted='#898781', line='#e1e0d9', accent='#157a63',
                  accent_soft='#ddeee7', accent_ink='#0d5c4a', s1='#2a78d6', s2='#eb6834',
                  crit='#d03b3b', crit_ink='#b02f2f', crit_soft='#faecec'),
    'dark':  dict(bg='#0f1211', surface='#181c1a', surface2='#202522', ink='#edf0ed',
                  ink2='#aab3ac', muted='#898781', line='#262b28', accent='#43c3a0',
                  accent_soft='#14352c', accent_ink='#6fd7ba', s1='#5b9cf0', s2='#e9743f',
                  crit='#e8605e', crit_ink='#f0908e', crit_soft='#2a1918'),
}

PAPER = 'Zaremba, Sutskever &amp; Vinyals (2015) · Recurrent Neural Network Regularization'


class Fig:
    def __init__(self, w, h, t):
        self.w, self.h, self.t = w, h, t
        self.p = []
        self.p.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">')
        self.p.append(f'<style>text {{ font-family: {FONT}; }}</style>')
        self.p.append('<defs>')
        for name, col in (('s1', t['s1']), ('s2', t['s2']), ('mut', t['muted'])):
            self.p.append(
                f'<marker id="ah-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
                f'markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
        self.p.append('</defs>')
        self.p.append(f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>')
        self.p.append(f'<rect x="14" y="14" width="{w-28}" height="{h-28}" rx="14" '
                      f'fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="1"/>')

    def text(self, x, y, s, size=14, fill=None, anchor='start', weight='400'):
        fill = fill or self.t['ink']
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
                      f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')

    def box(self, cx, cy, w, h, label, stroke=None, size=17, dash=None):
        x, y = cx - w / 2, cy - h / 2
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="11" '
                      f'fill="{self.t["surface2"]}" stroke="{stroke or self.t["line"]}" '
                      f'stroke-width="1.6"{d}/>')
        self.text(cx, cy + size * 0.36, label, size, self.t['ink'], 'middle', '700')

    def arrow(self, x1, y1, x2, y2, kind='s2', width=2.1, dash=None):
        col = self.t[kind] if kind in ('s1', 's2') else self.t['muted']
        mk = 'ah-' + ('mut' if kind not in ('s1', 's2') else kind)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
                      f'stroke-width="{width}" marker-end="url(#{mk})"{d} stroke-linecap="butt"/>')

    def cut(self, cx, cy, r=13):
        d = r * 0.42
        self.p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{self.t["surface"]}" '
                      f'stroke="{self.t["crit"]}" stroke-width="2.2"/>')
        self.p.append(f'<path d="M{cx-d},{cy-d} L{cx+d},{cy+d} M{cx+d},{cy-d} L{cx-d},{cy+d}" '
                      f'stroke="{self.t["crit"]}" stroke-width="2.2" stroke-linecap="round"/>')

    def callout(self, x, y, w, h, tone, lines, uid):
        fill = self.t['crit_soft'] if tone == 'crit' else self.t['accent_soft']
        bar = self.t['crit'] if tone == 'crit' else self.t['accent']
        ink = self.t['crit_ink'] if tone == 'crit' else self.t['accent_ink']
        self.p.append(f'<clipPath id="clip-{uid}"><rect x="{x}" y="{y}" width="{w}" '
                      f'height="{h}" rx="10"/></clipPath>')
        self.p.append(f'<g clip-path="url(#clip-{uid})">')
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
        self.p.append(f'<rect x="{x}" y="{y}" width="3" height="{h}" fill="{bar}"/>')
        self.p.append('</g>')
        for dy, size, s in lines:
            self.text(x + 20, y + dy, s, size, ink)

    def footer(self):
        self.text(self.w - 40, self.h - 30, PAPER, 11, self.t['muted'], 'end')

    def save(self, name):
        self.p.append('</svg>')
        path = os.path.join(OUT, name)
        with open(path, 'w') as f:
            f.write('\n'.join(self.p))
        return path


def sub(s, size=11):
    return f'<tspan dy="5" font-size="{size}">{s}</tspan><tspan dy="-5">&#8203;</tspan>'


def sup(s, size=10):
    return f'<tspan dy="-6" font-size="{size}">{s}</tspan><tspan dy="6">&#8203;</tspan>'


# ---------------------------------------------------------------- 그림 1
def fig1(t):
    W, H = 920, 406
    f = Fig(W, H, t)
    f.text(40, 56, '순환 연결(가로)에 드롭아웃을 걸면', 23, t['ink'], weight='700')
    f.text(40, 85, '히든 스테이트가 흐르는 길을 자르는 것 = 앞에서 읽은 내용을 무작위로 지우는 것',
           14.5, t['ink2'])

    cols, CY, BW, BH = [140, 360, 580, 800], 186, 104, 60
    for i, c in enumerate(cols):
        f.text(c, 144, f'스텝 {i+1}', 12, t['muted'], 'middle', '600')
        f.box(c, CY, BW, BH, 'h' + sub(str(i + 1), 12), stroke=t['s2'], size=19)
    for a, b in zip(cols, cols[1:]):
        f.arrow(a + BW / 2 + 8, CY, b - BW / 2 - 4, CY, 's2')
        mid = (a + b) / 2
        f.cut(mid, CY)
        f.text(mid, 144, '20% 삭제', 12, t['crit_ink'], 'middle', '600')

    f.text(40, 252, '정보 생존율', 12.5, t['muted'], weight='700')
    for c, pct, lab in zip(cols, [1.0, .8, .64, .51], ['100%', '80%', '64%', '51%']):
        x0 = c - BW / 2
        f.p.append(f'<rect x="{x0}" y="262" width="{BW}" height="9" rx="4.5" fill="{t["line"]}"/>')
        f.p.append(f'<rect x="{x0}" y="262" width="{BW*pct:.1f}" height="9" rx="4.5" fill="{t["s2"]}"/>')
        f.text(c, 293, lab, 13, t['ink'] if pct > .6 else t['crit_ink'], 'middle', '700')

    f.callout(40, 310, 840, 58, 'crit', [
        (24, 14, '100단어짜리 문장이면 이 가위질이 100번 반복된다 — 첫 단어가 끝까지 살아남을 확률은 '
                 '0.8' + sup('100') + ' &#8776; 2&#215;10' + sup('&#8722;10') + ', 사실상 0.'),
        (44, 13, 'LSTM이 셀 스테이트까지 따로 만들어 지키려 했던 장기 기억을, 드롭아웃이 앞장서서 부수는 셈.'),
    ], 'f1')
    f.footer()
    return f


# ---------------------------------------------------------------- 그림 2
def fig2(t):
    W, H = 900, 670
    f = Fig(W, H, t)
    f.text(40, 56, '해결책: 비순환 연결(세로)에만 드롭아웃', 23, t['ink'], weight='700')
    f.text(40, 85, '순환 연결(가로)은 그대로 두고, 층과 층을 잇는 비순환 연결(세로)에만 드롭아웃을 건다',
           14.5, t['ink2'])

    cols, BW, BH = [280, 500, 720], 116, 54
    Y_OUT, Y_L2, Y_L1, Y_IN = 128, 251, 381, 464
    for y, name in ((Y_OUT, '출력'), (Y_L2, '2층'), (Y_L1, '1층'), (Y_IN, '입력')):
        f.text(180, y + 6, name, 14.5, t['muted'], 'end', '700')

    for i, c in enumerate(cols):
        f.p.append(f'<rect x="{c-BW/2}" y="{Y_OUT-20}" width="{BW}" height="40" rx="10" '
                   f'fill="{t["surface2"]}" stroke="{t["line"]}" stroke-width="1.4" '
                   f'stroke-dasharray="5 4"/>')
        f.text(c, Y_OUT + 6, '&#375;' + sub(str(i + 1)), 17, t['ink2'], 'middle', '700')
        f.box(c, Y_L2, BW, BH, 'LSTM', stroke=t['line'])
        f.box(c, Y_L1, BW, BH, 'LSTM', stroke=t['line'])
        f.text(c, Y_IN + 6, 'x' + sub(str(i + 1), 12), 18, t['ink2'], 'middle', '700')
        f.text(c, Y_IN + 36, f'스텝 {i+1}', 12.5, t['muted'], 'middle', '600')
        f.arrow(c, Y_IN - 16, c, Y_L1 + BH / 2 + 4, 'mut', 1.8)          # 입력 → 1층
        f.arrow(c, Y_L1 - BH / 2 - 4, c, Y_L2 + BH / 2 + 4, 's1')        # 1층 → 2층
        f.cut(c, (Y_L1 - BH / 2 + Y_L2 + BH / 2) / 2)
        f.arrow(c, Y_L2 - BH / 2 - 4, c, Y_OUT + 24, 's1')               # 2층 → 출력
        f.cut(c, (Y_L2 - BH / 2 + Y_OUT + 20) / 2)

    for a, b in zip(cols, cols[1:]):
        for y in (Y_L2, Y_L1):
            f.arrow(a + BW / 2 + 8, y, b - BW / 2 - 4, y, 's2')

    f.p.append(f'<line x1="40" y1="528" x2="860" y2="528" stroke="{t["line"]}" stroke-width="1"/>')
    f.cut(54, 550, 11)
    f.text(74, 555, '드롭아웃 — 층 사이(세로)에만 건다', 13, t['ink'])
    f.arrow(360, 550, 400, 550, 's2')
    f.text(410, 555, '히든 스테이트 — 시간 축(가로)은 자르지 않는다', 13, t['ink'])

    f.callout(40, 570, 820, 50, 'accent', [
        (31, 14, '정보가 거치는 드롭아웃 횟수 = 층 수(여기서는 2번)로 고정 — 문장이 100단어여도 늘어나지 않는다.'),
    ], 'f2')
    f.footer()
    return f


made = []
for theme, t in THEMES.items():
    made.append(fig1(t).save(f'fig1-recurrent-dropout-erases-memory-{theme}.svg'))
    made.append(fig2(t).save(f'fig2-dropout-on-vertical-only-{theme}.svg'))
print('\n'.join(made))
