# Registry as Code (登記をコードで管理する)

これはgemini3.0と壁打ちした結果生まれたプロジェクトです。エンジニアによる、エンジニアのための、Git管理できる登記ツールです。
「設定ファイル（Config）を書き換えれば、決定論的に完璧なPDFが出力される」Pythonスクリプトを提供します。

## 機能
- **決定論的PDF生成**: 設定ファイルを元に、常に同じ結果を出力します。
- **Git管理**: `CompanyConfig` の変更履歴＝会社の登記変更履歴になります。
- **MVP機能**: 代表社員の変更（辞任・就任）に必要な4つの書類を自動生成します。

## 必要なもの
1. **Python 3.10+**
2. **ReportLab**: PDF生成ライブラリ (インストール済み)
3. **IPAexゴシックフォント (`ipaexg.ttf`)**

## セットアップ手順

### 1. フォントの準備 (必須)
このツールは日本語フォント `ipaexg.ttf` を使用します。
1. [IPAexゴシック(ipaexg.ttf)のダウンロード](https://moji.or.jp/ipafont/ipaex00401/) にアクセスしてください。
2. `ipaexg00401.zip` (または最新版) をダウンロードして解凍します。
3. フォルダ内の `ipaexg.ttf` ファイルを、このプロジェクトのルートディレクトリ (`registry_generator.py` と同じ場所) にコピーしてください。

### 2. 書類の生成
以下のコマンドを実行すると、PDFが生成されます。

```bash
# Windows (PowerShell)
.\.venv\Scripts\python registry_generator.py
```

### 3. 設定の変更
`registry_generator.py` を開き、`CompanyConfig` クラスの値を変更して再実行してください。

```python
@dataclass
class CompanyConfig:
    name: str = "合同会社あなたの会社"
    # ... 他の設定 ...
```

## 生成される書類
1. 1_登記申請書.pdf
2. 2_総社員の同意書.pdf
3. 3_就任承諾書.pdf
4. 4_辞任届.pdf

## ライセンス
Open Source (Future Plan)
