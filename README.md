# 旅食日和 (tabi-shoku-hiyori) — N5 旅遊/菜單單字 LINE Bot

每天 10:00 推送 N5 等級的「旅遊」10個 + 「菜單」10個（共20個）單字，
22:00 推送複習提醒。架構與設定方式同 [jp-vocab-line](https://github.com/mying0928/jp-vocab-line)，
詳細申請流程可參考該repo的 `GUIDE.md`。

## 結構說明

- `words_travel.json`：旅遊主題單字庫（目前50個，N5為主）
- `words_menu.json`：菜單/餐廳主題單字庫（目前50個，N5為主）
- `progress.json`：分別記錄旅遊/菜單目前進度與今日推送內容
- `send_words.py`：10:00推送，旅遊+菜單各10個新單字
- `send_review.py`：22:00推送，複習今天的20個單字
- `.github/workflows/schedule.yml`：排程定義（UTC 02:00 / UTC 14:00）

## 進度顯示

每天訊息底部會顯示旅遊、菜單各自的「第 X / Y 天」（50字 ÷ 10 = 5天一輪），
跑完一輪會自動從頭開始並提示可以擴充單字庫。

## 怎麼請 Claude 繼續擴充

開新對話直接說：

> 繼續 tabi-shoku-hiyori 單字庫擴充

Claude 會接續準備下一批旅遊/菜單單字。
