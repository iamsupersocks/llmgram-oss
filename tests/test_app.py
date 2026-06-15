import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app


def load_sample(name):
    return json.loads((ROOT / 'sample_data' / name).read_text(encoding='utf-8'))


def test_home_renders():
    app = create_app()
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'LLMgram OSS' in response.data


def test_signals_api_filters_and_limits():
    app = create_app()
    client = app.test_client()
    response = client.get('/api/signals?limit=2&category=agents')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) <= 2
    assert all(item['category'] == 'agents' for item in data['items'])


def test_weekly_api_shape():
    app = create_app()
    client = app.test_client()
    data = client.get('/api/weekly').get_json()
    assert data['week']
    assert data['stats']['signals_tracked'] >= 1000
    assert len(data['items']) >= 4


def test_sample_data_safe_demo_shape():
    signals = load_sample('signals.json')
    sources = load_sample('sources.json')
    weekly = load_sample('weekly.json')
    assert len(signals) >= 5
    assert len(sources) >= 4
    assert weekly['stats']['labs_monitored'] >= 10
    assert all({'id', 'rank', 'title', 'summary', 'source', 'url', 'score', 'confidence'} <= set(s) for s in signals)
    assert any('Mistral' in s['lab'] or 'mistral' in ' '.join(s.get('tags', [])).lower() for s in signals)


def test_docs_and_ci_exist():
    expected = [
        'README.md',
        'openapi.yaml',
        'docs/ARCHITECTURE.md',
        'docs/PRODUCTION_BLUEPRINT.md',
        'docs/REPORT.md',
        'docs/assets/llmgram-preview.svg',
        'docs/assets/llmgram-architecture.svg',
        '.github/workflows/ci.yml',
    ]
    for rel in expected:
        assert (ROOT / rel).exists(), rel
    assert 'gitleaks' in (ROOT / '.github/workflows/ci.yml').read_text(encoding='utf-8')
