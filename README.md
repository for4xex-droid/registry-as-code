# Registry as Code (登記をコードで管理する)

これはgemini3.0と壁打ちした結果生まれたプロジェクトです。エンジニアによる、エンジニアのための、Git管理できる登記ツールです。
「設定ファイル（Config）を書き換えれば、決定論的に完璧なPDFが出力される」Pythonスクリプトを提供します。

## 主な機能
- **決定論的PDF生成**: 設定ファイルを元に、常に同じ結果を出力します。
- **Git管理**: コードと設定で履歴管理が可能。ただし機密情報はJSONに分離してGit対象外としています。
- **マルチモード対応**: 以下の2パターンに対応しています。
  1. **代表社員の交代**: 旧代表が辞任し、新代表が就任する（旧代表は社員として残る）。
  2. **持分譲渡と退社**: 旧代表が持分を全て譲渡し、会社から完全に離脱する。

## 必要なもの
1. **Python 3.10+**
2. **ReportLab**: PDF生成ライブラリ (インストール済み)
3. **IPAexゴシックフォント (`ipaexg.ttf`)**
   - [ダウンロード](https://moji.or.jp/ipafont/ipaex00401/) して同階層に配置してください。

## 使い方

### 1. 設定ファイル (`company_data.json`) の準備
Git追跡対象外の `company_data.json` をルートディレクトリに作成し、以下の形式で保存してください。

```json
{
    "mode": "withdrawal", 
    "corporate_number": "1300-03-004457",
    "name": "合同会社あなたの会社",
    "address": "京都市北区...",
    "capital": "10,000",
    "legal_bureau": "京都地方法務局 本局",
    "new_rep_name": "新代表の名前",
    "new_rep_address": "新代表の住所",
    "old_rep_name": "旧代表の名前",
    "old_rep_address": "旧代表の住所",
    "change_date": "令和7年12月15日",
    "filing_date": "令和7年12月17日",
    "phone_number": "090-0000-0000"
}
```

### 2. モードの切り替え (`mode`)
`company_data.json` の `mode` キーで書類の種類を制御します。

| モード値 | 説明 | 生成される書類 |
| :--- | :--- | :--- |
| `"change_rep"` | **代表社員の交代**<br>(旧代表は残留) | ・登記申請書 (辞任)<br>・総社員の同意書<br>・就任承諾書<br>・**辞任届** |
| `"withdrawal"` | **持分譲渡と退社**<br>(完全離脱) | ・登記申請書 (退社)<br>・総社員の同意書 (**持分譲渡契約含む**)<br>・就任承諾書<br>(× 辞任届は不要) |

### 3. 実行
```bash
# Windows (PowerShell)
.\.venv\Scripts\python registry_generator.py
```
実行すると、PDFファイルが生成されます。

## ライセンス
Open Source (Future Plan)
