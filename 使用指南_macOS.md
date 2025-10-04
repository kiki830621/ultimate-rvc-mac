# Ultimate RVC - macOS 使用指南

## 📋 目錄

- [系統需求](#系統需求)
- [快速開始](#快速開始)
- [功能說明](#功能說明)
- [常見問題](#常見問題)
- [進階設定](#進階設定)

---

## 系統需求

- **作業系統**: macOS (已在 Apple Silicon 測試)
- **Python**: 3.12 (由 uv 自動管理)
- **硬體**:
  - CPU: 建議 8 核心以上
  - RAM: 建議 16GB 以上
  - 儲存空間: 至少 10GB 可用空間
- **網路**: 穩定的網路連線 (用於下載模型)

⚠️ **重要**: macOS 版本僅支援 **CPU 模式**，處理速度會比 GPU 版本慢。建議處理較短的音訊檔案。

---

## 快速開始

### 1. 啟動應用程式

```bash
cd ultimate-rvc
./urvc-macos.sh run
```

### 2. 開啟網頁介面

啟動後會看到類似訊息：
```
Running on local URL:  http://127.0.0.1:7860
```

在瀏覽器中開啟 **http://127.0.0.1:7860**

### 3. 開始使用

首次啟動會自動下載預設的 AI 模型 (Taylor Swift, Eminem 等)，請耐心等待。

---

## 功能說明

### 🎤 生成歌曲翻唱 (Song Covers)

1. 進入 `Generate` > `Song covers` 頁籤
2. 選擇音訊來源：
   - **YouTube URL**: 貼上 YouTube 影片連結
   - **Upload audio**: 上傳本地音訊檔案 (MP3, WAV 等)
3. 從 `Voice model` 下拉選單選擇聲音模型
4. 點擊 `Generate` 開始處理
5. 等待處理完成後即可下載結果

### 🗣️ 文字轉語音 (Text-to-Speech)

1. 進入 `Generate` > `Speech` 頁籤
2. 輸入要轉換的文字
3. 選擇聲音模型
4. 調整語速、音高等參數
5. 點擊 `Generate` 生成語音

### 📥 下載聲音模型

1. 進入 `Models` > `Download` 頁籤
2. 貼上模型下載連結 (通常是 .zip 檔)
   - 可從 [AI Hub Discord](https://discord.gg/aihub) 尋找模型
3. 為模型命名 (英文)
4. 點擊 `Download`
5. 下載完成後即可在生成頁面使用

### 📤 上傳本地模型

1. 進入 `Models` > `Upload` 頁籤
2. 準備模型檔案：
   - `.pth` 檔案 (必要)
   - `.index` 檔案 (選用，可提升品質)
3. 依照指示上傳
4. 為模型命名並完成上傳

### 🎓 訓練自己的模型

1. 進入 `Train` 頁籤
2. 上傳訓練用音訊檔案 (建議至少 10 分鐘純人聲)
3. 設定訓練參數
4. 開始訓練 (⚠️ CPU 模式訓練會非常慢，不建議)

---

## 常見問題

### Q1: 處理速度很慢怎麼辦？

**A**: macOS 版本使用 CPU 運算，速度本來就較慢。建議：
- 處理較短的音訊 (< 5 分鐘)
- 關閉其他耗資源的應用程式
- 考慮使用 Google Colab 的 GPU 版本

### Q2: 如何更新到最新版本？

**A**: 執行更新命令：
```bash
./urvc-macos.sh update
```

### Q3: 下載的聲音模型在哪裡？

**A**: 模型儲存位置：
```
ultimate-rvc/voice_models/
```

### Q4: 支援哪些音訊格式？

**A**: 支援常見格式：
- 輸入: MP3, WAV, FLAC, M4A, OGG
- 輸出: WAV, MP3

### Q5: 出現錯誤訊息怎麼辦？

**A**: 常見解決方法：
1. 檢查網路連線
2. 確認音訊檔案沒有損壞
3. 重新啟動應用程式
4. 查看錯誤訊息並搜尋解決方案

---

## 進階設定

### 使用 CLI 命令列模式

```bash
# 查看 CLI 說明
./urvc-macos.sh cli --help

# CLI 模式生成歌曲翻唱
./urvc-macos.sh cli generate song-cover \
  --source "https://youtube.com/watch?v=..." \
  --model "模型名稱"
```

### 環境變數設定

可在執行前設定環境變數來自訂行為：

```bash
# 設定模型儲存位置
export URVC_MODELS_DIR="/path/to/models"

# 設定音訊檔案位置
export URVC_AUDIO_DIR="/path/to/audio"

# 設定 log 等級
export URVC_CONSOLE_LOG_LEVEL="DEBUG"

# 然後啟動應用程式
./urvc-macos.sh run
```

### 設定檔管理

可儲存和載入自訂設定：

```bash
# 在網頁 UI 中調整好設定後，可以儲存設定檔
# 設定檔位於: configs/

# 載入指定設定
export URVC_CONFIG="my_config"
./urvc-macos.sh run
```

### YouTube Cookie 設定

如果 YouTube 下載受限，可設定 cookie：

```bash
# 匯出瀏覽器的 YouTube cookies 為 cookies.txt
export YT_COOKIEFILE="/path/to/cookies.txt"
./urvc-macos.sh run
```

---

## 效能建議

### CPU 模式最佳化

1. **音訊長度**: 建議單次處理 < 5 分鐘
2. **並行處理**: 避免同時處理多個任務
3. **系統資源**:
   - 關閉不必要的應用程式
   - 確保充足的 RAM 可用
   - 使用 SSD 儲存空間

### 提升處理速度

- 降低音訊品質設定
- 使用較小的模型
- 關閉不必要的後處理效果

---

## 資源連結

- **官方文件**: [GitHub README](https://github.com/JackismyShephard/ultimate-rvc)
- **模型庫**: [AI Hub Discord](https://discord.gg/aihub)
- **問題回報**: [GitHub Issues](https://github.com/JackismyShephard/ultimate-rvc/issues)
- **Google Colab** (GPU 版本): [Colab Notebook](https://colab.research.google.com/github/JackismyShephard/ultimate-rvc/blob/main/notebooks/ultimate_rvc_colab.ipynb)

---

## 使用條款

請遵守以下使用規範：

❌ **禁止用途**:
- 批評或攻擊個人
- 宣傳特定政治立場、宗教或意識形態
- 販售聲音模型或生成的音訊
- 惡意冒充他人
- 詐欺用途

✅ **建議用途**:
- 個人娛樂創作
- 學術研究
- 藝術創作
- 技術測試

---

## 技術支援

如有問題，請先：
1. 查看本指南的「常見問題」章節
2. 搜尋 [GitHub Issues](https://github.com/JackismyShephard/ultimate-rvc/issues)
3. 加入 [Discord 社群](https://discord.gg/T4ejEz8HtX) 尋求協助

---

**最後更新**: 2025-10-04
**版本**: 0.5.13 (macOS CPU 版)
