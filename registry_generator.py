import json
import os
from dataclasses import dataclass
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# --- 1. 設定（Config）: ここを書き換えるだけで全ての書類が変わります ---


@dataclass
class CompanyConfig:
    name: str = "合同会社サンプル"  # 会社名
    address: str = "京都市北区..."  # 本店所在地
    capital: str = "1,000,000"  # 資本金（円）

    # 法務局（管轄）
    legal_bureau: str = "京都地方法務局 本局"

    # 新しい代表社員
    new_rep_name: str = "サンプル 太郎"
    new_rep_address: str = "京都市左京区..."

    # 辞任する旧代表社員
    old_rep_name: str = "サンプル 次郎"
    old_rep_address: str = "京都市北区..."

    # 日付関係
    change_date: str = "令和7年12月15日"  # 効力発生日（変更日）
    filing_date: str = "令和7年12月17日"  # 登記申請日

    # 連絡先
    phone_number: str = "090-0000-0000"

    @classmethod
    def from_json(cls, json_path: str) -> "CompanyConfig":
        if not os.path.exists(json_path):
            print(
                f"⚠️ 設定ファイル {json_path} が見つかりません。デフォルト値を使用します。"
            )
            return cls()
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)


# --- 2. エンジン（Vibe Coding Logic） ---


class RegistryGenerator:
    def __init__(self, config: CompanyConfig) -> None:
        self.c = config
        self.font_name = "IPAexGothic"
        self.font_path = "ipaexg.ttf"  # 同じフォルダにフォントファイルを置くこと

        # フォントの登録（なければエラー回避のためデフォルトを使用するが文字化けする）
        if os.path.exists(self.font_path):
            pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))
        else:
            print(
                f"警告: {self.font_path} が見つかりません。"
                "日本語が表示されない可能性があります。"
            )

    def _create_canvas(self, filename: str) -> Any:
        c = canvas.Canvas(filename, pagesize=A4)
        c.setFont(self.font_name, 11)
        return c

    def _draw_title(self, c: Any, text: str, y: float) -> None:
        c.setFont(self.font_name, 16)
        c.drawCentredString(A4[0] / 2, y, text)
        c.setFont(self.font_name, 11)  # 戻す

    def _save_pdf(self, c: Any, filename: str) -> None:
        try:
            c.save()
            print(f"Generated: {filename}")
        except PermissionError:
            print(
                f"❌ エラー: '{filename}' を保存できません。\n"
                "ファイルを開いている場合は閉じてください。"
            )

    def generate_all(self) -> None:
        self.generate_application()
        self.generate_consent()
        self.generate_acceptance()
        self.generate_resignation()
        print("✅ 全ての書類生成が完了しました。")

    # --- 書類1: 登記申請書 ---
    def generate_application(self) -> None:
        filename = "1_登記申請書.pdf"
        c = self._create_canvas(filename)

        # タイトル
        self._draw_title(c, "合同会社変更登記申請書", 270 * mm)

        y = 240 * mm
        line_height = 10 * mm

        # 記載事項
        items = [
            ("1. 商号", self.c.name),
            ("1. 本店", self.c.address),
            ("1. 登記の事由", "代表社員の変更"),
            ("1. 登記すべき事項", "別紙のとおり"),
            ("1. 課税標準金額", "金10,000円"),
            ("1. 登録免許税", "金10,000円"),
            ("1. 添付書類", "総社員の同意書　1通"),
            ("", "代表社員の就任承諾書　1通"),
            ("", "辞任届　1通"),
            ("", "印鑑証明書　1通"),  # 新代表の分
        ]

        for label, content in items:
            c.drawString(25 * mm, y, label)
            c.drawString(65 * mm, y, content)
            y -= line_height

        # 申請日と宛先
        y -= 10 * mm
        c.drawString(25 * mm, y, self.c.filing_date)
        y -= 7 * mm
        c.drawString(25 * mm, y, f"{self.c.address}")
        y -= 7 * mm
        c.drawString(25 * mm, y, f"申請人　{self.c.name}")
        y -= 7 * mm
        c.drawString(25 * mm, y, f"代表社員　{self.c.new_rep_name}")
        c.drawString(100 * mm, y, "(印)")  # ハンコ場所

        y -= 10 * mm
        c.drawString(25 * mm, y, f"連絡先の電話番号：{self.c.phone_number}")

        y -= 15 * mm
        c.setFont(self.font_name, 12)
        c.drawString(25 * mm, y, f"{self.c.legal_bureau}　御中")

        # 捨印エリア
        c.setFont(self.font_name, 10)
        c.drawString(170 * mm, 280 * mm, "捨印")

        # 別紙（OCR用シートイメージ）
        c.showPage()  # 改ページ
        self._draw_title(c, "別紙（登記すべき事項）", 270 * mm)
        c.setFont(self.font_name, 12)
        y = 240 * mm
        c.drawString(25 * mm, y, "「役員に関する事項」")
        y -= 8 * mm
        c.drawString(25 * mm, y, "「資格」代表社員")
        c.drawString(80 * mm, y, "「氏名」" + self.c.old_rep_name)
        c.drawString(140 * mm, y, "「原因年月日」" + self.c.change_date + "辞任")

        y -= 8 * mm
        c.drawString(25 * mm, y, "「資格」代表社員")
        c.drawString(80 * mm, y, "「氏名」" + self.c.new_rep_name)
        c.drawString(140 * mm, y, "「原因年月日」" + self.c.change_date + "就任")

        y -= 8 * mm
        c.drawString(25 * mm, y, "「住所」" + self.c.new_rep_address)

        self._save_pdf(c, filename)

    # --- 書類2: 総社員の同意書 ---
    def generate_consent(self) -> None:
        filename = "2_総社員の同意書.pdf"
        c = self._create_canvas(filename)

        self._draw_title(c, "総社員の同意書", 250 * mm)

        text_lines = [
            f"令和{self.c.change_date[2:]}、当会社の本店において総社員が同意し、",
            "下記のとおり代表社員を選任し、被選任者は即時その就任を承諾した。",
            "",
            "記",
            "",
            "1. 選任された代表社員",
            f"   住所　{self.c.new_rep_address}",
            f"   氏名　{self.c.new_rep_name}",
            "",
            "上記の決定を明確にするため、この同意書を作成し、総社員がこれに記名押印する。",
            "",
            f"{self.c.change_date}",
            "",
            f"{self.c.name}",
            "",
            f"社員　{self.c.old_rep_name}  (印)",
            f"社員　{self.c.new_rep_name}  (印)",
        ]

        y = 210 * mm
        for line in text_lines:
            c.drawString(30 * mm, y, line)
            y -= 10 * mm

        self._save_pdf(c, filename)

    # --- 書類3: 就任承諾書 ---
    def generate_acceptance(self) -> None:
        filename = "3_就任承諾書.pdf"
        c = self._create_canvas(filename)

        self._draw_title(c, "就任承諾書", 250 * mm)

        text_lines = [
            f"私は、令和{self.c.change_date[2:]}開催の総社員の同意により、貴社の代表社員に",
            "選任されたので、その就任を承諾します。",
            "",
            f"{self.c.change_date}",
            "",
            f"住所　{self.c.new_rep_address}",
            f"氏名　{self.c.new_rep_name}  (実印)",
            "",
            "",
            f"{self.c.name}　御中",
        ]

        y = 200 * mm
        for line in text_lines:
            c.drawString(30 * mm, y, line)
            y -= 10 * mm

        self._save_pdf(c, filename)

    # --- 書類4: 辞任届 ---
    def generate_resignation(self) -> None:
        filename = "4_辞任届.pdf"
        c = self._create_canvas(filename)

        self._draw_title(c, "辞任届", 250 * mm)

        text_lines = [
            f"私は、令和{self.c.change_date[2:]}をもって、都合により貴社の代表社員を",
            "辞任いたします。",
            "",
            f"{self.c.change_date}",
            "",
            f"住所　{self.c.old_rep_address}",
            f"氏名　{self.c.old_rep_name}  (印)",
            "",
            "",
            f"{self.c.name}　御中",
        ]

        y = 200 * mm
        for line in text_lines:
            c.drawString(30 * mm, y, line)
            y -= 10 * mm

        self._save_pdf(c, filename)


# --- 3. 実行 ---
if __name__ == "__main__":
    # ここでデータを注入（Injection）
    # company_data.json から設定を読み込む（なければデフォルト）
    my_config = CompanyConfig.from_json("company_data.json")

    generator = RegistryGenerator(my_config)
    generator.generate_all()
