import copy
import json
from pathlib import Path
import tempfile
import unittest
import validate

class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.item = dict(id="test-only-never-publish", apps=["scoredeck", "scheduledeck"], category="other", publishedAt="2026-10-19T00:00:00Z", translations={"ja":dict(title="配信テスト",summary="試験専用",body="正式なお知らせではありません。"),"en":dict(title="Delivery test",summary="Test only",body="This is not a production announcement.")})

    def run_feed(self, items):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"feed.json"
            path.write_text(json.dumps(dict(schemaVersion=1,announcements=items)))
            return validate.validate(path)

    def test_valid_empty_and_bilingual(self):
        self.run_feed([])
        self.run_feed([self.item])

    def test_reject_private_and_invalid(self):
        for mutation in [dict(status="draft"),dict(internalTags=["secret"]),dict(privateNote="secret"),dict(category="unknown"),dict(publishedAt="invalid"),dict(links=[dict(title="bad",url="http://example.invalid")]),dict(links=[dict(title="bad",url="https://user:pass@example.invalid")]),dict(links=[dict(title="bad",url="https://example.invalid:8443")]),dict(translations={"private":dict(title="x",summary="",body="x")})]:
            with self.subTest(mutation=mutation):
                item=copy.deepcopy(self.item)
                item.update(mutation)
                with self.assertRaises((AssertionError,ValueError)):
                    self.run_feed([item])
        with self.assertRaises(AssertionError):
            self.run_feed([self.item,self.item])

    def test_editor_no_network_and_no_embedded_data(self):
        root=Path(__file__).resolve().parents[1]
        html=(root/"docs/admin/index.html").read_text()
        self.assertIn("connect-src 'none'",html)
        self.assertIn("form-action 'none'",html)
        self.assertNotIn("fetch(",html)
        self.assertNotIn("localStorage",html)

if __name__=="__main__": unittest.main()
