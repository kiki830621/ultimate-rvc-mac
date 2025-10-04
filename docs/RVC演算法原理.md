# RVC (Retrieval-based Voice Conversion) 演算法原理

## 📚 目錄

- [核心概念](#核心概念)
- [演算法架構](#演算法架構)
- [處理流程](#處理流程)
- [關鍵技術](#關鍵技術)
- [模型訓練](#模型訓練)
- [推論過程](#推論過程)

---

## 核心概念

### 什麼是 RVC？

**RVC (Retrieval-based Voice Conversion)** 是一種**基於檢索的語音轉換技術**，能夠將一個人的語音轉換成另一個人的聲音，同時保持原始語音的內容（語義、音調變化等）。

### 核心優勢

1. **高品質聲音克隆** - 能夠精確複製目標聲音的特徵
2. **少量資料訓練** - 只需 10 分鐘的音訊即可訓練模型
3. **實時轉換能力** - 優化後可達到低延遲
4. **音調保持** - 保留原始說話者的音調變化和情感

---

## 演算法架構

### 整體架構圖

```
輸入音訊
    ↓
【1. 音訊預處理】
    ├─ 重採樣 (16kHz)
    ├─ 分段切割
    └─ 高通濾波
    ↓
【2. 音高提取 (F0 Extraction)】
    ├─ FCPE (Fast Crepe Pitch Estimator)
    ├─ RMVPE (Robust Model for Voice Pitch Estimation)
    └─ Crepe
    ↓
【3. 特徵提取 (Feature Extraction)】
    ├─ ContentVec Embedder
    ├─ HuBERT Embedder
    └─ 提取語音內容特徵
    ↓
【4. 特徵檢索 (Feature Retrieval)】★ 核心創新
    ├─ FAISS 索引搜尋
    ├─ K-最近鄰檢索 (K=8)
    └─ 加權平均特徵
    ↓
【5. 語音合成 (Voice Synthesis)】
    ├─ 特徵上採樣 (2x)
    ├─ 音高引導
    ├─ HiFiGAN 生成器
    └─ 輸出音訊 (40kHz/48kHz)
    ↓
【6. 後處理】
    ├─ RMS 音量調整
    ├─ 自動調音 (可選)
    └─ 降噪 (可選)
    ↓
輸出音訊
```

---

## 處理流程

### 階段 1: 音訊預處理

**目的**: 標準化輸入音訊格式

```python
# pipeline.py:580-581
audio = signal.filtfilt(bh, ah, audio)  # 高通濾波 (48Hz)
audio_pad = np.pad(audio, (window//2, window//2), mode="reflect")
```

**操作**:
1. **重採樣**: 轉換為 16kHz (特徵提取用)
2. **高通濾波**: 移除 48Hz 以下的低頻雜訊
3. **音訊填充**: 使用反射模式填充邊界

### 階段 2: 音高提取 (F0 Extraction)

**目的**: 提取音高資訊，保留說話者的音調變化

**支援方法**:

1. **FCPE (Fast Crepe Pitch Estimator)**
   - 速度最快
   - 精度中等
   - 適合即時應用

2. **RMVPE (Robust Model for Voice Pitch Estimation)**
   - 精度最高
   - 對雜訊有抵抗力
   - 計算量較大

3. **Crepe**
   - 經典方法
   - 平衡速度與精度

```python
# pipeline.py:614-624
pitch, pitchf = self.get_f0(
    audio_pad, p_len, pitch, f0_methods,
    hop_length, f0_autotune, f0_autotune_strength, inp_f0
)
```

**輸出**:
- `pitch`: 量化的音高序列（整數）
- `pitchf`: 原始音高序列（浮點數）

### 階段 3: 特徵提取

**目的**: 提取語音的內容特徵（不含說話者身份）

**Embedder 模型**:

1. **ContentVec**
   - 自監督學習模型
   - 專注於語音內容
   - 忽略說話者特徵

2. **HuBERT (Hidden-Unit BERT)**
   - Facebook 開發
   - 基於 BERT 架構
   - 更好的語義理解

```python
# pipeline.py:461-464
feats = model(feats)["last_hidden_state"]
feats = model.final_proj(feats[0]).unsqueeze(0) if version == "v1" else feats
```

**輸出**: 語音特徵向量 `feats` (shape: [1, T, 256])

### 階段 4: 特徵檢索 ★ 核心創新

**目的**: 使用目標聲音的特徵庫，檢索最相似的特徵

這是 RVC 的**核心創新**，使用**檢索機制**而非直接映射。

#### 4.1 建立 FAISS 索引

訓練時，將目標聲音的所有特徵向量儲存在 FAISS 索引中：

```python
# 訓練時建立索引
index = faiss.IndexFlatL2(256)  # 256 維特徵
index.add(target_voice_features)  # 加入所有訓練特徵
faiss.write_index(index, "model.index")
```

#### 4.2 推論時檢索

```python
# pipeline.py:516-522
def _retrieve_speaker_embeddings(self, feats, index, big_npy, index_rate):
    npy = feats[0].cpu().numpy()

    # K-最近鄰搜尋 (K=8)
    score, ix = index.search(npy, k=8)

    # 加權平均
    weight = np.square(1 / score)
    weight /= weight.sum(axis=1, keepdims=True)
    npy = np.sum(big_npy[ix] * np.expand_dims(weight, axis=2), axis=1)

    # 混合原始特徵
    feats = (
        torch.from_numpy(npy).unsqueeze(0).to(self.device) * index_rate
        + feats * (1 - index_rate)
    )
    return feats
```

**步驟解析**:

1. **搜尋**: 找出最相似的 8 個特徵向量
2. **計算權重**: 距離越近，權重越高 `w = 1/d²`
3. **加權平均**: 混合 8 個相似特徵
4. **混合原始**: 用 `index_rate` 控制混合比例
   - `index_rate=1`: 完全使用檢索特徵
   - `index_rate=0`: 完全使用原始特徵

**優勢**:
- 保留目標聲音的細微特徵
- 避免過度平滑
- 提供更自然的聲音轉換

### 階段 5: 語音合成

**目的**: 將特徵轉換為音訊波形

#### 5.1 特徵上採樣

```python
# pipeline.py:478-482
feats = F.interpolate(
    feats.permute(0, 2, 1),
    scale_factor=2
).permute(0, 2, 1)
```

將特徵序列長度擴展 2 倍，匹配音訊解析度。

#### 5.2 音高保護 (Pitch Protection)

```python
# pipeline.py:493-500
if protect < 0.5:
    pitchff = pitchf.clone()
    pitchff[pitchf > 0] = 1
    pitchff[pitchf < 1] = protect
    feats = feats * pitchff.unsqueeze(-1) + feats0 * (1 - pitchff.unsqueeze(-1))
```

**保護機制**:
- `protect=0`: 不保護，完全使用檢索特徵
- `protect=0.5`: 平衡混合
- 保護原始音高的細微變化

#### 5.3 HiFiGAN 生成器

```python
# pipeline.py:504-509
audio1 = (
    net_g.infer(feats.float(), p_len, pitch, pitchf.float(), sid)[0][0, 0]
    .data.cpu().float().numpy()
)
```

**HiFiGAN** (High-Fidelity Generative Adversarial Network):
- 將特徵轉換為音訊波形
- 支援不同採樣率 (32k/40k/48k)
- 高品質語音合成

### 階段 6: 後處理

#### 6.1 RMS 音量調整

```python
# pipeline.py:55-99 (AudioProcessor.change_rms)
rms1 = librosa.feature.rms(y=source_audio, ...)
rms2 = librosa.feature.rms(y=target_audio, ...)

adjusted_audio = target_audio * (
    (rms1 * rate + rms2 * (1 - rate)) / rms2
)
```

匹配原始音訊的音量包絡。

#### 6.2 自動調音 (Auto-tune)

```python
# 使用 librosa 的音高校正
if f0_autotune:
    f0 = correct_pitch(f0, strength=f0_autotune_strength)
```

#### 6.3 降噪

使用 `noisereduce` 庫去除背景雜訊。

---

## 關鍵技術

### 1. FAISS (Facebook AI Similarity Search)

**用途**: 高效的向量相似度搜尋

```python
index = faiss.IndexFlatL2(dim)  # L2 距離
score, ix = index.search(query, k)  # K-NN 搜尋
```

**優勢**:
- 支援大規模向量檢索
- 多種距離度量（L2, cosine, etc.）
- GPU 加速支援

### 2. ContentVec / HuBERT Embedder

**原理**: 自監督學習

1. **訓練階段**: 使用大量未標註語音學習通用特徵
2. **遮罩預測**: 預測被遮罩的語音片段
3. **特徵提取**: 最後一層隱藏狀態作為特徵

**特點**:
- 不含說話者資訊
- 保留語義和韻律
- 跨語言能力

### 3. HiFiGAN Vocoder

**架構**:
```
特徵序列 → 上採樣卷積 → 殘差塊 → 輸出音訊
              ↓
          多尺度判別器
```

**訓練**:
- 生成器 (Generator): 特徵 → 音訊
- 判別器 (Discriminator): 真實 vs 生成
- 對抗訓練：提升合成品質

---

## 模型訓練

### 訓練流程

```
1. 資料準備
   ├─ 收集目標聲音 (10-30 分鐘)
   ├─ 音訊切片 (4-10 秒)
   └─ 音高標註

2. 特徵提取
   ├─ 使用 ContentVec/HuBERT
   ├─ 提取 F0 (音高)
   └─ 儲存特徵

3. 建立 FAISS 索引
   ├─ 收集所有特徵向量
   ├─ 建立 IndexFlatL2
   └─ 儲存索引檔

4. 訓練 HiFiGAN
   ├─ 輸入: 特徵 + F0
   ├─ 輸出: 音訊波形
   ├─ 損失: L1 + 對抗損失
   └─ 訓練 epochs: 200-500

5. 儲存模型
   ├─ model.pth (HiFiGAN 權重)
   ├─ model.index (FAISS 索引)
   └─ config.json (配置)
```

### 訓練參數

```yaml
sample_rate: 40000  # 或 48000
batch_size: 8
learning_rate: 2e-4
epochs: 500
f0_method: "rmvpe"
embedder: "contentvec"
```

---

## 推論過程

### 完整推論流程

```python
# 1. 載入模型
model = ContentVec()
net_g = HiFiGAN()
index = faiss.read_index("model.index")

# 2. 處理音訊
audio = load_audio("input.wav")
audio = resample(audio, 16000)
audio = highpass_filter(audio)

# 3. 提取音高
f0 = extract_f0(audio, method="rmvpe")

# 4. 提取特徵
feats = model(audio)

# 5. 檢索相似特徵
feats_retrieved = retrieve_features(feats, index, k=8)
feats = mix(feats_retrieved, feats, index_rate=0.75)

# 6. 合成音訊
output = net_g(feats, f0, speaker_id)

# 7. 後處理
output = adjust_rms(output, audio)
output = denoise(output)

# 8. 儲存
save_audio("output.wav", output, 40000)
```

### 關鍵參數

| 參數 | 範圍 | 說明 |
|------|------|------|
| `pitch` | -12~+12 | 音高調整（半音） |
| `index_rate` | 0.0~1.0 | 檢索混合比例 |
| `protect` | 0.0~0.5 | 音高保護程度 |
| `volume_envelope` | 0.0~1.0 | 音量包絡混合 |
| `f0_autotune` | true/false | 自動調音開關 |

---

## 技術優勢與限制

### 優勢 ✅

1. **高品質**: 檢索機制保留細節
2. **少量資料**: 10 分鐘即可訓練
3. **音調保留**: 保持原始表現力
4. **靈活控制**: 多種參數調整

### 限制 ⚠️

1. **計算量**: FAISS 檢索需要時間
2. **記憶體**: 需要載入完整索引
3. **即時性**: 優化前難以達到即時
4. **相似度依賴**: 需要足夠相似的訓練資料

---

## 創新點總結

### 1. 檢索機制 ★★★★★

**傳統方法**: 直接學習映射 `Input → Output`
**RVC 方法**: 檢索相似特徵 `Input → Retrieve → Output`

**優勢**:
- 保留訓練資料的細節
- 避免過度平滑
- 更自然的聲音轉換

### 2. 多尺度 F0 提取

支援多種音高提取方法，適應不同場景。

### 3. 自監督特徵提取

使用 ContentVec/HuBERT，無需大量標註資料。

---

## 參考資源

### 論文

- [VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech](https://arxiv.org/abs/2106.06103)
- [HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis](https://arxiv.org/abs/2010.05646)
- [HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units](https://arxiv.org/abs/2106.07447)

### 開源專案

- [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- [ContentVec](https://github.com/auspicious3000/contentvec)
- [FAISS](https://github.com/facebookresearch/faiss)

---

**最後更新**: 2025-10-04
**版本**: Ultimate RVC 0.5.13
**作者研究**: 基於 RVC 原始論文和實作代碼分析
