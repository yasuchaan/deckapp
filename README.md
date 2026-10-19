# Deck announcements

Score Deck / Schedule Deck の公開お知らせ配信用リポジトリ。

公開JSONは docs/announcements.json。初期状態は0件です。管理画面は docs/admin/index.html。管理データは端末内で処理し、自分専用のFilesへ保存します。公開リポジトリには管理データ・下書き・アプリソース・秘密情報を置かないでください。

更新: 管理画面で公開JSONを書き出し、GitHubで docs/announcements.json を置換してmainへコミット。検証成功後、Actionsの Validate and publish announcements をmainで手動実行し、publishを有効にします。pushだけでは公開されません。

Pagesの配信対象は案内HTML・管理画面HTML・公開JSONのみです。iPad Safariでの保存・再読込とアプリ実機表示は別途確認が必要です。
