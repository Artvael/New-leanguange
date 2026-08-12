"""
Lexer (Tokenizer) untuk Bahasa Pemrograman Core (.cr).
Bertugas memecah teks sumber menjadi aliran token dengan penanganan sistem indentasi otomatis.
"""

from typing import List
from .tokens import Token, TokenType, KEYWORDS


class CoreLexerError(Exception):
    """Exception khusus untuk error leksikal dengan pesan berbahasa Indonesia."""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"[Kesalahan Leksikal] Baris {line}, Kolom {column}: {message}")


class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        self.indent_stack: List[int] = [0]

    def tokenize(self) -> List[Token]:
        lines = self.source_code.splitlines()
        
        for line_num, line_raw in enumerate(lines, start=1):
            self._process_line(line_raw, line_num)

        # Di akhir file, selesaikan blok indentasi yang masih terbuka
        if self.tokens and self.tokens[-1].type not in (TokenType.NEWLINE, TokenType.DEDENT):
            last_line = len(lines) if lines else 1
            self.tokens.append(Token(TokenType.NEWLINE, "\n", last_line, 1))

        last_line = len(lines) + 1
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, "", last_line, 1))

        self.tokens.append(Token(TokenType.EOF, None, last_line, 1))
        return self.tokens

    def _process_line(self, line: str, line_num: int):
        # Hitung spasi indentasi di awal baris
        stripped_left = line.lstrip(" ")
        
        # Abaikan baris kosong atau baris yang hanya berisi komentar
        if not stripped_left or stripped_left.startswith("#"):
            return

        indent_level = len(line) - len(stripped_left)
        
        # Konversi jika ada tab (1 tab = 4 spasi standar)
        if "\t" in line[:indent_level]:
            indent_level = len(line[:indent_level].replace("\t", "    "))

        current_indent = self.indent_stack[-1]

        if indent_level > current_indent:
            self.indent_stack.append(indent_level)
            self.tokens.append(Token(TokenType.INDENT, indent_level, line_num, 1))
        elif indent_level < current_indent:
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, indent_level, line_num, 1))
            
            if not self.indent_stack or self.indent_stack[-1] != indent_level:
                raise CoreLexerError(
                    f"Indentasi tidak konsisten. Tingkat indentasi {indent_level} tidak cocok dengan blok sebelumnya.",
                    line_num,
                    1
                )

        # Tokenisasi konten baris
        col = indent_level + 1
        i = indent_level
        line_len = len(line)

        has_line_tokens = False

        while i < line_len:
            char = line[i]

            # Lewati spasi di dalam baris
            if char in " \t\r":
                i += 1
                col += 1
                continue

            # Komentar satu baris (#) -> abaikan sisa baris
            if char == "#":
                break

            # String literal ("..." atau '...')
            if char in ('"', "'"):
                str_val, new_i, str_cols = self._read_string(line, i, line_num, col)
                self.tokens.append(Token(TokenType.STRING, str_val, line_num, col))
                i = new_i
                col += str_cols
                has_line_tokens = True
                continue

            # Angka (Integer / Float)
            if char.isdigit():
                num_val, new_i, num_cols = self._read_number(line, i, line_num, col)
                self.tokens.append(Token(TokenType.NUMBER, num_val, line_num, col))
                i = new_i
                col += num_cols
                has_line_tokens = True
                continue

            # Operator 2 karakter
            if i + 1 < line_len:
                two_chars = line[i:i+2]
                if two_chars == "==":
                    self.tokens.append(Token(TokenType.EQUAL, "==", line_num, col))
                    i += 2
                    col += 2
                    has_line_tokens = True
                    continue
                elif two_chars == "!=":
                    self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", line_num, col))
                    i += 2
                    col += 2
                    has_line_tokens = True
                    continue
                elif two_chars == ">=":
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", line_num, col))
                    i += 2
                    col += 2
                    has_line_tokens = True
                    continue
                elif two_chars == "<=":
                    self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", line_num, col))
                    i += 2
                    col += 2
                    has_line_tokens = True
                    continue

            # Operator 1 karakter
            if char == "+":
                self.tokens.append(Token(TokenType.PLUS, "+", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == "-":
                self.tokens.append(Token(TokenType.MINUS, "-", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == "*":
                self.tokens.append(Token(TokenType.MULTIPLY, "*", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == "/":
                self.tokens.append(Token(TokenType.DIVIDE, "/", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == "%":
                self.tokens.append(Token(TokenType.MODULO, "%", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == "=":
                self.tokens.append(Token(TokenType.ASSIGN, "=", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == ">":
                self.tokens.append(Token(TokenType.GREATER, ">", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == "<":
                self.tokens.append(Token(TokenType.LESS, "<", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            elif char == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", line_num, col))
                i += 1
                col += 1
                has_line_tokens = True
            # Identifier atau Kata Kunci (Keywords)
            elif char.isalpha() or char == "_":
                ident_val, new_i, ident_cols = self._read_identifier(line, i)
                token_type = KEYWORDS.get(ident_val.lower(), TokenType.IDENTIFIER)
                
                # Nilai boolean dan null
                if token_type == TokenType.KEYWORD_BENAR:
                    self.tokens.append(Token(TokenType.KEYWORD_BENAR, True, line_num, col))
                elif token_type == TokenType.KEYWORD_SALAH:
                    self.tokens.append(Token(TokenType.KEYWORD_SALAH, False, line_num, col))
                elif token_type == TokenType.KEYWORD_KOSONG:
                    self.tokens.append(Token(TokenType.KEYWORD_KOSONG, None, line_num, col))
                else:
                    self.tokens.append(Token(token_type, ident_val, line_num, col))
                    
                i = new_i
                col += ident_cols
                has_line_tokens = True
            else:
                raise CoreLexerError(f"Karakter tidak dikenal atau dilarang '{char}'", line_num, col)

        if has_line_tokens:
            self.tokens.append(Token(TokenType.NEWLINE, "\n", line_num, col))

    def _read_string(self, line: str, start_idx: int, line_num: int, col: int):
        quote_char = line[start_idx]
        result = []
        i = start_idx + 1
        line_len = len(line)

        while i < line_len and line[i] != quote_char:
            if line[i] == "\\":
                i += 1
                if i >= line_len:
                    raise CoreLexerError("String tidak tertutup (escape sequence menggantung)", line_num, col)
                esc = line[i]
                if esc == "n":
                    result.append("\n")
                elif esc == "t":
                    result.append("\t")
                elif esc == "r":
                    result.append("\r")
                elif esc == "\\":
                    result.append("\\")
                elif esc in ('"', "'"):
                    result.append(esc)
                else:
                    result.append(esc)
            else:
                result.append(line[i])
            i += 1

        if i >= line_len:
            raise CoreLexerError(f"String teks tidak ditutup dengan tanda petik {quote_char}", line_num, col)

        i += 1  # Lewati tanda petik penutup
        return "".join(result), i, (i - start_idx)

    def _read_number(self, line: str, start_idx: int, line_num: int, col: int):
        i = start_idx
        line_len = len(line)
        is_float = False

        while i < line_len and (line[i].isdigit() or line[i] == "."):
            if line[i] == ".":
                if is_float:
                    raise CoreLexerError("Format angka desimal tidak valid (terdapat lebih dari satu titik)", line_num, col)
                is_float = True
            i += 1

        raw_num = line[start_idx:i]
        num_val = float(raw_num) if is_float else int(raw_num)
        return num_val, i, (i - start_idx)

    def _read_identifier(self, line: str, start_idx: int):
        i = start_idx
        line_len = len(line)
        while i < line_len and (line[i].isalnum() or line[i] == "_"):
            i += 1
        return line[start_idx:i], i, (i - start_idx)
