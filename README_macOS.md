# Ultimate RVC - macOS Edition

這是 [Ultimate RVC](https://github.com/JackismyShephard/ultimate-rvc) 的 macOS 客製版本，專門針對 Apple Silicon (M1/M2/M3) 和 Intel Mac 優化，支援 CPU 模式運行。

## ⚠️ 重要說明

- **原始專案**: [JackismyShephard/ultimate-rvc](https://github.com/JackismyShephard/ultimate-rvc)
- **此版本修改**: 支援 macOS 平台的 CPU 執行模式
- **效能提醒**: 因使用 CPU 運算，處理速度會比 GPU 版本慢

## 主要修改

1. **pyproject.toml**: 加入 macOS (`darwin`) 平台支援
2. **依賴調整**:
   - `onnxruntime-gpu` → `onnxruntime` (macOS)
   - `audio-separator[gpu]` → `audio-separator` (macOS)
3. **啟動腳本**: 新增 `urvc-macos.sh` 專用啟動器
4. **中文文檔**: 完整繁體中文使用指南

## 快速開始

```bash
# 啟動網頁介面
./urvc-macos.sh run

# 查看說明
./urvc-macos.sh help
```

詳細使用方式請參考 [使用指南_macOS.md](./使用指南_macOS.md)

## 系統需求

- macOS (Apple Silicon 或 Intel)
- Python 3.12 (自動安裝)
- 16GB+ RAM 建議
- 10GB+ 可用儲存空間

## 授權

本專案繼承原始 Ultimate RVC 的授權條款（MIT License）。

## 致謝

感謝 [JackismyShephard](https://github.com/JackismyShephard) 開發的優秀 Ultimate RVC 專案。
