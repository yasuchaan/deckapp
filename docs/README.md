# Deck announcements publication repository

配信専用リポジトリ: `yasuchaan/deckapp`。初期JSONは空です。公開URLはPages設定画面で確認します。

## 初期設定（公開前に確認）

このフォルダーの内容だけをリポジトリ直下へ配置する。`.github`を含める。
アプリソース、管理JSON、証明書、秘密鍵、テストログは含めない。
GitHub Freeではpublicリポジトリを使用する。リポジトリ作成自体がファイルの外部公開になるため、所有者と内容の承認後に行う。

Settings → Pages → Source: GitHub Actions。`github-pages` environmentはmainのみ許可。
既存の別のPages配信ワークフロー・branch配信は併用しない。

push/PRは検証のみ。公開はActions → Validate and publish announcements → Run workflow → mainを選択 → publishを有効にして実行。
publish未選択・main以外ではデプロイしない。承認を得るまでは実行しない。
配信するのはJSON、案内HTML、空の管理画面HTMLだけ。手動実行時に選んだmainのrevisionが配信対象。

## iPadだけで更新

1. Pagesの `admin/` をSafariで開く（初回公開後はMacサーバー・証明書設定不要）。画面自体は誰でも閲覧できるが、GitHubへの書込み権限はない。
2. 自分だけのFiles/iCloud Driveに保存した最新の管理JSONを読み込む。編集後に「編集内容を反映」→「管理データを保存」。ブラウザを閉じる前に保存を確認。端末間の自動同期・競合解決はない。
3. 公開対象・日英文面・日時・対象アプリを確認し「公開JSONを書き出す」。下書きや内部タグは除外される。
4. GitHubへログインし、docs/announcements.jsonを同名ファイルで置換・mainへコミット。Safariのアップロード選択でFilesを使用。GitHubのファイル編集画面も利用可能。
5. Actions検証の成功を確認して、上記の手動公開を実行。失敗時は前回のPages配信が残る。PagesのHTTPS URLとJSONを確認。

管理画面は外部ライブラリ・通信処理・トークン保存を持たない。CSPで接続とフォーム送信を禁止する。公開ページに管理データは埋め込まない。管理画面自体は非公開の保管場所ではない。
公開リポジトリへアップロードした内容はPagesをデプロイする前から閲覧可能。管理JSONはアップロードしない。公開コミットの履歴は残る。

iPad Safariのファイル保存・アップロード・GitHub Actions操作は実機未検証。Mac Safariローカルファイルでは新規作成・日英編集・反映・プレビューを確認した。

## アプリ接続と確認

Pages画面に表示された実URLのannouncements.jsonをHTTPSで取得・検証してから、両アプリのDeckAnnouncementsURLへ設定する。仮URLは設定しない。
テスト告知は本番と分けた試験用リポジトリを推奨し、その作成・公開にも承認を得る。本番で行う場合は告知文・公開範囲を別途承認後にする。
未読NEWは一覧のみでは消えず、詳細表示で既読。同一ID修正では既読維持。キャッシュは通常24時間、失敗時保持。試験のため本番端末データ・既読設定は削除しない。

公式資料:
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
