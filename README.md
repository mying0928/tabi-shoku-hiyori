# 旅食日和 (tabi-shoku-hiyori) — N5+N4 旅遊/菜單單字 LINE Bot

每天 10:00 推送 N5+N4 等級的「旅遊」10個 + 「菜單」10個（共20個）單字，
22:00 推送複習提醒。架構與設定方式同 [jp-vocab-line](https://github.com/mying0928/jp-vocab-line)，
詳細申請流程可參考該repo的 `GUIDE.md`。

## 結構說明

- `words_travel.json`：旅遊主題單字庫（68個，前38個為N5、後30個為N4，依序排列、已逐字檢查讀音/意思）
- `words_menu.json`：菜單/餐廳主題單字庫（66個，前40個為N5、後26個為N4）
- `progress.json`：分別記錄旅遊/菜單目前進度與今日推送內容
- `reminders.json`：記錄 GitHub PAT 的核發日/到期日，過期前會在訊息中提醒
- `send_words.py`：10:00推送，旅遊+菜單各10個新單字，並檢查PAT是否快過期
- `send_review.py`：22:00推送，複習今天的20個單字
- `.github/workflows/schedule.yml`：排程定義（UTC 02:00 / UTC 14:00）

## 進度顯示與輪換機制

每天訊息底部會顯示旅遊、菜單各自的「第 X / Y 天」（旅遊68字、菜單66字 ÷ 10 = **約7天一輪**）。
單字庫依「先N5、後N4」排序，所以前幾天會先複習N5基礎詞，接著自然銜接N4詞彙，
達到循序漸進學習的效果，**不需要手動更新單字庫**。

一輪（約7天）跑完後會自動從頭重新開始（用同一批N5+N4單字複習），同時訊息會提示：
「N5+N4單字已全部學完！可繼續複習，或考慮向上學習N3 🎓」。

如果之後想往N3邁進，可以請Claude準備N3版本的旅遊/菜單單字庫並調整程式。

## PAT 到期提醒

`reminders.json` 記錄了：

```json
{
  "pat_issued": "2026-06-14",
  "pat_expires": "2026-09-12",
  "remind_days_before": 3
}
```

- 到期前3天起，每天早上的訊息會附帶提醒：「GitHub PAT 將於 XXXX-XX-XX 過期」
- 過期後則提示「已過期，記得重新產生token」
- 重新產生PAT後，記得更新 `pat_issued` / `pat_expires`（push日 + 90天）

## 關於「30天沒commit」的提醒

這個排程**每天都會自動commit `progress.json`**，所以正常運作下不會發生
「30天沒commit」的狀況。

⚠️ 但如果某天發現訊息沒有正常送達（代表排程可能已停止），這個檢查程式本身
也跑不動，無法自動提醒你 —— 這是邏輯上的限制（排程停了，依賴排程的提醒
自然也不會跑）。

**建議：** 如果發現連續幾天沒收到LINE訊息，直接到
https://github.com/mying0928/tabi-shoku-hiyori/actions 確認排程狀態，
若顯示因不活躍被停用，點選重新啟用即可。

## 怎麼請 Claude 繼續擴充

開新對話直接說：

> 繼續 tabi-shoku-hiyori 單字庫擴充

Claude 會接續準備下一批旅遊/菜單單字（例如擴充成「第二輪」全新100字）。
