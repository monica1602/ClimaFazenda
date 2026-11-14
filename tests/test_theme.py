from rotaclima import theme
from tests.test_app import PAGES


def test_every_page_has_distinct_theme_and_illustration():
    assert list(theme.THEMES) == PAGES
    assert len({t.primaria for t in theme.THEMES.values()}) == len(PAGES)
    for page, t in theme.THEMES.items():
        assert (theme.ASSETS / t.ilustracao).exists()
        assert len(set(t.paleta)) >= 5
        assert t.primaria in theme.css(page)
        assert theme.hero_image(page).startswith('<img src="data:image/svg+xml;base64,')


def test_each_city_recolors_every_page():
    from rotaclima import presets
    assert set(theme.REGIONS) == set(presets.PRESETS)
    for preset in theme.REGIONS:
        primaries = [theme.theme_for(p, preset).primaria for p in PAGES]
        assert len(set(primaries)) == len(PAGES)
        assert all(c in theme.css(p, preset) for c, p in zip(primaries, PAGES))
    for page in PAGES:
        per_city = {theme.theme_for(page, preset).primaria for preset in theme.REGIONS}
        assert len(per_city) == len(theme.REGIONS), page
