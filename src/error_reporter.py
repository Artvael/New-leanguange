"""
Modul Pelaporan Error & Diagnostik Cerdas Bahasa Core (.cr).
Menyediakan deteksi typo (Did You Mean?), cuplikan baris kode visual dengan tanda panah (^),
serta penjelasan penyebab dan solusi perbaikan dalam Bahasa Indonesia yang ramah pemula.
"""

import difflib
from typing import List, Optional, Dict, Any


class CoreDiagnosticError(Exception):
    """Exception dasar yang membawa metadata diagnostik lengkap."""
    def __init__(
        self,
        error_type: str,
        message: str,
        line: int,
        column: int = 1,
        source_code: str = "",
        cause: str = "",
        solution: str = "",
        suggestion: Optional[str] = None
    ):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.column = column
        self.source_code = source_code
        self.cause = cause
        self.solution = solution
        self.suggestion = suggestion
        super().__init__(self.format_report())

    def format_report(self) -> str:
        border = "═" * 60
        sub_border = "─" * 60
        lines = [
            "",
            f"❌ [{self.error_type}] pada Baris {self.line}, Kolom {self.column}",
            f"   {self.message}",
            sub_border
        ]

        # Tampilkan cuplikan baris kode jika source_code tersedia
        if self.source_code:
            code_lines = self.source_code.splitlines()
            start_line = max(1, self.line - 1)
            end_line = min(len(code_lines), self.line + 1)

            for l_num in range(start_line, end_line + 1):
                idx = l_num - 1
                if 0 <= idx < len(code_lines):
                    line_text = code_lines[idx]
                    prefix = f"👉 {l_num:3d} | " if l_num == self.line else f"   {l_num:3d} | "
                    lines.append(prefix + line_text)
                    
                    # Tambahkan penunjuk panah (^) di bawah baris yang bermasalah
                    if l_num == self.line:
                        col_pos = max(1, self.column)
                        arrow_spacing = " " * (len(prefix) + col_pos - 1)
                        lines.append(f"{arrow_spacing}^^^")

            lines.append(sub_border)

        # Informasi Saran Typo
        if self.suggestion:
            lines.append(f"💡 Apakah maksud Anda: '{self.suggestion}' ?")

        # Penjelasan Penyebab
        if self.cause:
            lines.append(f"🔍 Penyebab: {self.cause}")

        # Solusi Konkret
        if self.solution:
            lines.append(f"🔧 Saran Solusi: {self.solution}")

        lines.append(border)
        return "\n".join(lines)


def suggest_keyword(word: str, valid_keywords: List[str]) -> Optional[str]:
    """Mencari kemiripan kata kunci (detektor typo)."""
    matches = difflib.get_close_matches(word.lower(), valid_keywords, n=1, cutoff=0.6)
    return matches[0] if matches else None


def suggest_variable(var_name: str, available_vars: List[str]) -> Optional[str]:
    """Mencari kemiripan nama variabel atau fungsi yang sudah dideklarasikan."""
    matches = difflib.get_close_matches(var_name, available_vars, n=1, cutoff=0.5)
    return matches[0] if matches else None
