# 使用服務一覽

## LINE Developers
https://developers.line.biz/en/

建立與管理 Messaging API Channel 的地方。在這裡產生 Channel Access Token（讓腳本有權限透過 API 發送訊息）。

## LINE Official Account Manager
https://manager.line.biz/

LINE 官方帳號的管理後台。可以設定帳號名稱、頭像、自動回覆訊息，以及查看好友數等基本資訊。

## cron-job.org
https://console.cron-job.org/dashboard

免費的外部排程服務。設定每天 10:00 與 22:00 呼叫 GitHub API，觸發 GitHub Actions 執行推送腳本。

## GitHub Repo
https://github.com/mying0928/tabi-shoku-hiyori

存放所有程式碼的地方。GitHub Actions 負責執行 Python 腳本並將進度回寫至 `progress.json`。
