"""Identidade visual: uma paleta e uma ilustração por tela, ligadas ao tema de cada página."""
from __future__ import annotations

import base64
import colorsys
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"


@dataclass(frozen=True)
class PageTheme:
    icone: str
    primaria: str
    escura: str
    clara: str
    destaque: str
    paleta: tuple[str, ...]
    ilustracao: str
    resumo: str


THEMES: dict[str, PageTheme] = {
    "1. Propriedade": PageTheme(
        "🚜", "#8D6E63", "#4E342E", "#EFEBE9", "#7CB342",
        ("#6D4C41", "#7CB342", "#C0A062", "#33691E", "#A1887F", "#D4A373", "#558B2F", "#BCAAA4"),
        "1_propriedade.svg", "Terra e lavoura: localização, talhões, solo e premissas da fazenda."),
    "2. Diagnóstico ambiental": PageTheme(
        "🌦️", "#1E88E5", "#0D47A1", "#E3F2FD", "#FFB300",
        ("#1E88E5", "#FB8C00", "#43A047", "#E53935", "#00ACC1", "#8E24AA", "#FDD835", "#5C6BC0"),
        "2_diagnostico.svg", "Água e clima: chuva, evaporação, calor e veranicos medidos pela NASA POWER."),
    "3. Mapa dos talhões": PageTheme(
        "🛰️", "#00897B", "#004D40", "#E0F2F1", "#9CCC65",
        ("#00897B", "#7CB342", "#FDD835", "#5C6BC0", "#26C6DA", "#8D6E63", "#EC407A", "#9E9D24"),
        "3_mapa.svg", "Olhar do satélite: vigor da vegetação (NDVI MODIS) e condição do solo de cada talhão."),
    "4. Planejamento de rotação": PageTheme(
        "🌱", "#43A047", "#1B5E20", "#E8F5E9", "#F9A825",
        ("#2E7D32", "#F9A825", "#8D6E63", "#66BB6A", "#FBC02D", "#00897B", "#AED581", "#D84315"),
        "4_planejamento.svg", "Sequências de cultivo para dois anos, com motivos, riscos e comparação com o atual."),
    "5. Comparação de cenários": PageTheme(
        "⚖️", "#5E35B1", "#311B92", "#EDE7F6", "#26A69A",
        ("#1E88E5", "#8D6E63", "#F9A825", "#78909C", "#7E57C2", "#26A69A", "#EC407A", "#9CCC65"),
        "5_comparacao.svg", "A: conservar água · B: recuperar o solo · C: equilíbrio econômico e ambiental."),
    "6. Simulador climático": PageTheme(
        "🔥", "#F4511E", "#BF360C", "#FBE9E7", "#FFB300",
        ("#F4511E", "#FFB300", "#6D4C41", "#1E88E5", "#8E24AA", "#43A047", "#D81B60", "#90A4AE"),
        "6_simulador.svg", "E se chover menos ou fizer mais calor? Teste a resistência de cada rotação."),
    "7. Relatório": PageTheme(
        "📋", "#0B3D91", "#061F4A", "#E8EEF8", "#FC3D21",
        ("#0B3D91", "#FC3D21", "#43A047", "#FFB300", "#00ACC1", "#8E24AA", "#6D4C41", "#90A4AE"),
        "7_relatorio.svg", "Síntese para apresentar e levar a campo: estratégias, justificativas e limitações."),
}


@dataclass(frozen=True)
class Region:
    nome: str
    paisagem: str
    cores: dict[str, tuple[str, str]]


def _region(nome: str, paisagem: str, pares: list[tuple[str, str]]) -> Region:
    return Region(nome, paisagem, dict(zip(THEMES, pares)))


REGIONS: dict[str, Region] = {
    "Rio Verde (GO) — Cerrado": _region("Cerrado", "terra vermelha, buriti e ipê-amarelo", [
        ("#A0522D", "#C0CA33"), ("#1976D2", "#F9A825"), ("#2E7D5B", "#D4E157"), ("#558B2F", "#F9A825"),
        ("#6A1B9A", "#FF8F00"), ("#D84315", "#FFCA28"), ("#0B3D91", "#FC3D21")]),
    "Londrina (PR) — Norte do Paraná": _region("Norte do Paraná", "terra roxa e café", [
        ("#7B3F3F", "#8BC34A"), ("#3949AB", "#FFB300"), ("#00796B", "#AED581"), ("#2E7D32", "#C62828"),
        ("#880E4F", "#26A69A"), ("#E65100", "#FFD54F"), ("#283593", "#EF5350")]),
    "Passo Fundo (RS) — Planalto Médio": _region("Planalto Médio", "araucária, trigo e geada", [
        ("#5D6D3B", "#BCAAA4"), ("#0277BD", "#80DEEA"), ("#1B5E20", "#A5D6A7"), ("#33691E", "#FFD54F"),
        ("#4527A0", "#90CAF9"), ("#C62828", "#FFAB91"), ("#263238", "#4FC3F7")]),
    "Sorriso (MT) — Médio-Norte": _region("Médio-Norte", "soja dourada e chapadas", [
        ("#8D6E3F", "#9CCC65"), ("#0288D1", "#FFCA28"), ("#00695C", "#FFEE58"), ("#9E9D24", "#FFB300"),
        ("#512DA8", "#FFB300"), ("#EF6C00", "#FFE082"), ("#01579B", "#FFB300")]),
    "Petrolina (PE) — Semiárido": _region("Semiárido", "caatinga, rio São Francisco, uva e manga", [
        ("#B5651D", "#8D9E3A"), ("#00838F", "#FFB74D"), ("#6D8B3A", "#E0C068"), ("#7CB342", "#8E24AA"),
        ("#7A2E5C", "#FB8C00"), ("#BF360C", "#FFC107"), ("#4E342E", "#FF7043")]),
}


def _hls(hex_color: str) -> tuple[float, float, float]:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hls(r, g, b)


def _hex(h: float, l: float, s: float) -> str:
    return "#" + "".join(f"{round(c * 255):02X}" for c in colorsys.hls_to_rgb(h, l, s))


def text_on(hex_color: str) -> str:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return "#1F2A30" if 0.299 * r + 0.587 * g + 0.114 * b > 0.62 else "#FFFFFF"


def theme_for(page: str, preset: str | None = None) -> PageTheme:
    base = THEMES[page]
    region = REGIONS.get(preset or "")
    if region is None:
        return base
    primaria, destaque = region.cores[page]
    h, l, s = _hls(primaria)
    paleta = base.paleta if page.startswith("5.") else (primaria, *[c for c in base.paleta[1:] if c != primaria])
    return replace(base, primaria=primaria, destaque=destaque, escura=_hex(h, l * 0.55, s),
                   clara=_hex(h, 0.95, min(s, 0.45)), paleta=paleta)


@lru_cache(maxsize=None)
def svg_uri(name: str) -> str:
    data = (ASSETS / name).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()


def nav_label(page: str) -> str:
    return f"{THEMES[page].icone}  {page}"


def css(page: str, preset: str | None = None) -> str:
    t = theme_for(page, preset)
    nav = "\n".join(
        f'section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-of-type({i}) > label '
        f"{{ border-left: 5px solid {th.primaria}; }}\n"
        f'section[data-testid="stSidebar"] [role="radiogroup"] > div:nth-of-type({i}) > label:has(input:checked) '
        f"{{ background: {th.primaria}; }}"
        for i, th in enumerate((theme_for(p, preset) for p in THEMES), start=1)
    )
    return f"""
<style>
.stApp {{ background: linear-gradient(180deg, {t.clara} 0px, #FFFFFF 420px); }}
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {t.clara} 0%, #FFFFFF 70%);
  border-right: 4px solid {t.primaria}; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div > label {{ padding: 6px 10px; margin: 3px 0;
  border-radius: 8px; background: rgba(255,255,255,.75); transition: all .15s; width: 100%; }}
section[data-testid="stSidebar"] [role="radiogroup"] > div > label:has(input:checked) p {{ color: #FFFFFF; font-weight: 700; }}
{nav}
.rc-brand {{ display: flex; align-items: center; gap: 10px; }}
.rc-brand b {{ font-size: 1.45rem; color: {t.escura}; }}
.st-key-hero {{ background: linear-gradient(120deg, {t.primaria} 0%, {t.escura} 100%); border-radius: 18px;
  padding: 1.1rem 1.6rem; box-shadow: 0 8px 22px rgba(0,0,0,.14); }}
.st-key-hero h1, .st-key-hero p {{ color: #FFFFFF !important; }}
.st-key-hero .rc-region {{ display: inline-block; margin-left: 6px; border: 1.5px solid rgba(255,255,255,.8);
  color: #FFFFFF; border-radius: 999px; padding: 1px 10px; font-size: .8rem; }}
.st-key-hero h1 {{ padding-bottom: .2rem; }}
.st-key-hero .rc-chip {{ display: inline-block; background: {t.destaque}; color: {text_on(t.destaque)} !important; border-radius: 999px;
  padding: 2px 12px; font-size: .8rem; font-weight: 700; letter-spacing: .03em; }}
.st-key-hero img {{ width: 100%; max-height: 170px; filter: drop-shadow(0 4px 8px rgba(0,0,0,.25)); }}
h2, h3 {{ color: {t.escura}; }}
[data-testid="stMainBlockContainer"] h3 {{ border-left: 6px solid {t.primaria}; padding-left: .6rem; }}
[data-testid="stMetric"] {{ background: #FFFFFF; border: 1px solid {t.clara}; border-left: 6px solid {t.primaria};
  border-radius: 12px; padding: .7rem .9rem; box-shadow: 0 2px 8px rgba(0,0,0,.06); }}
[data-testid="stMetricValue"] {{ color: {t.escura}; font-size: 1.65rem; }}
[data-testid="stMetricLabel"] p {{ white-space: normal; font-weight: 600; color: {t.escura}; }}
.stButton button, .stDownloadButton button {{ border: 1.5px solid {t.primaria}; color: {t.escura}; border-radius: 10px; }}
.stButton button:hover, .stDownloadButton button:hover {{ background: {t.primaria}; color: #FFFFFF; border-color: {t.primaria}; }}
[data-testid="stExpander"] details {{ border-left: 5px solid {t.destaque}; border-radius: 10px; background: #FFFFFF; }}
[data-testid="stExpander"] summary:hover p {{ color: {t.primaria}; }}
span[data-baseweb="tag"] {{ background-color: {t.primaria} !important; }}
[data-testid="stSlider"] div[style*="translate(-50%"] {{ background-color: {t.primaria} !important; }}
[data-testid="stSliderThumbValue"] p {{ color: {t.escura} !important; font-weight: 700; }}
</style>
"""


def brand_html() -> str:
    return (f'<div class="rc-brand"><img src="{svg_uri("logo.svg")}" width="40"/>'
            f"<b>RotaClima</b></div>")


def hero_image(page: str) -> str:
    t = THEMES[page]
    return f'<img src="{svg_uri(t.ilustracao)}" alt="Ilustração: {page}"/>'

