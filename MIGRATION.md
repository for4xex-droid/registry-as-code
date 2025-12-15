# 別のPCへの移行ガイド

このプロジェクトを別のPCで動かすための手順です。

## 1. 準備 (移行元のPCでやること)
もしGitHubへのアップロードがまだなら、以下のコマンドでアップロードします。
(このファイルを見ている時点で既に完了しているはずです)

```bash
git push origin main
```

## 2. セットアップ (移行先のPCでやること)

### 手順A: コードの取得
Gitを使ってコードをダウンロードします。

```bash
git clone https://github.com/for4xex-droid/registry-as-code.git
cd registry-as-code
```

### 手順B: 必須ファイルの配置 (重要！)
以下の2つのファイルは**Gitに含まれていません（セキュリティとライセンスの理由）**。
手動でコピーするか、元のPCからUSBメモリや安全なチャットツール等で送ってください。

1. **`company_data.json`** (あなたの個人情報設定ファイル)
   - プロジェクトのルートフォルダに置いてください。
2. **`ipaexg.ttf`** (日本語フォントファイル)
   - プロジェクトのルートフォルダに置いてください。

### 手順C: 環境構築
Pythonがインストールされていることを確認後、以下のコマンドでセットアップします。

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化 (Windows)
.\.venv\Scripts\Activate.ps1
# (Mac/Linuxの場合: source .venv/bin/activate)

# ライブラリのインストール
pip install reportlab
```

## 3. 実行確認
以下のコマンドでPDFが生成されれば完了です！

```bash
python registry_generator.py
```
