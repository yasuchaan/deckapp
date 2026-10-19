"""Validate the public feed before Pages deployment. No third-party dependencies."""
import json
from datetime import datetime
from pathlib import Path


def validate(path):
    raw = Path(path).read_bytes()
    assert len(raw) <= 1048576, 'Feed exceeds 1 MiB'
    feed = json.loads(raw)
    assert set(feed) == {'schemaVersion', 'announcements'}
    assert type(feed['schemaVersion']) is int and feed['schemaVersion'] == 1
    items = feed['announcements']
    assert isinstance(items, list) and len(items) <= 500
    ids = set()
    for item in items:
        assert set(item) <= {'id', 'apps', 'category', 'publishedAt', 'targetVersion', 'translations', 'links'}, 'Private or unknown fields in public feed'
        uid = item['id']
        assert isinstance(uid, str) and 0 < len(uid) <= 200 and uid not in ids
        ids.add(uid)
        assert isinstance(item['apps'], list) and item['apps'] and set(item['apps']) <= {'scoredeck', 'scheduledeck'}
        assert item['category'] in {'important', 'bug', 'improvement', 'feature', 'other'}
        stamp = item['publishedAt']
        assert isinstance(stamp, str) and stamp.endswith('Z') and '.' not in stamp
        datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%SZ')
        assert item.get('targetVersion') is None or isinstance(item['targetVersion'], str)
        translations = item['translations']
        assert isinstance(translations, dict) and translations and set(translations) <= {'ja', 'en'}
        for copy in translations.values():
            assert set(copy) <= {'title', 'summary', 'body', 'workaround'}
            for key, maximum in [('title', 300), ('summary', 2000), ('body', 50000)]:
                assert isinstance(copy[key], str) and len(copy[key]) <= maximum
            assert copy['title'].strip() and copy['body'].strip()
            assert copy.get('workaround') is None or isinstance(copy['workaround'], str)
        from urllib.parse import urlsplit
        assert 'links' not in item or isinstance(item['links'], list)
        for link in item.get('links', []):
            assert set(link) == {'title', 'url'} and isinstance(link['title'], str)
            url = urlsplit(link['url'])
            assert url.scheme == 'https' and url.hostname and url.username is None and url.password is None and url.port in (None, 443)
    return feed


if __name__ == '__main__':
    import sys
    validate(sys.argv[1] if len(sys.argv) > 1 else 'docs/announcements.json')
    print('Public feed valid')
