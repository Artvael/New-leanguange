"""
Parser untuk Bahasa Pemrograman Core (.cr).
Membangun Abstract Syntax Tree (AST) dari aliran token dengan penanganan blok indentasi tanpa simbol {}, (), ;.
"""

from typing import List, Optional, Tuple
from .tokens import Token, TokenType, KEYWORDS
from .error_reporter import CoreDiagnosticError, suggest_keyword
from .ast_nodes import (
    ASTNode, Program, Block, VarDecl, AssignStmt, PrintStmt,
    IfStmt, WhileStmt, ForRangeStmt, FunctionDef, ReturnStmt, FunctionCall,
    BinaryOp, UnaryOp, Literal, Variable, InputExpr
)


class CoreParserError(CoreDiagnosticError):
    """Exception khusus untuk error sintaksis dengan diagnostik cerdas."""
    def __init__(
        self,
        message: str,
        line: int,
        column: int = 1,
        source_code: str = "",
        cause: str = "",
        solution: str = "",
        suggestion: Optional[str] = None
    ):
        super().__init__(
            error_type="Kesalahan Sintaksis",
            message=message,
            line=line,
            column=column,
            source_code=source_code,
            cause=cause,
            solution=solution,
            suggestion=suggestion
        )


class Parser:
    def __init__(self, tokens: List[Token], source_code: str = ""):
        self.tokens = tokens
        self.source_code = source_code
        self.pos = 0

    def parse(self) -> Program:
        statements: List[ASTNode] = []
        self._skip_newlines()

        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()

        return Program(statements=statements)

    # --------------------------------------------------------------------------
    # Helper Navigasi Token
    # --------------------------------------------------------------------------

    def _peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self._previous()

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, error_message: str, cause: str = "", solution: str = "") -> Token:
        if self._check(token_type):
            return self._advance()
        curr = self._peek()
        suggestion = None
        if isinstance(curr.value, str):
            suggestion = suggest_keyword(curr.value, list(KEYWORDS.keys()))
        raise CoreParserError(
            error_message,
            curr.line,
            curr.column,
            source_code=self.source_code,
            cause=cause or f"Token '{curr.value}' tidak sesuai dengan sintaks yang diharapkan.",
            solution=solution or "Periksa kembali ejaan kata dan urutan instruksi pada baris ini.",
            suggestion=suggestion
        )

    def _skip_newlines(self):
        while self._match(TokenType.NEWLINE):
            pass

    # --------------------------------------------------------------------------
    # Parsing Pernyataan (Statements)
    # --------------------------------------------------------------------------

    def _parse_statement(self) -> Optional[ASTNode]:
        self._skip_newlines()
        if self._is_at_end():
            return None

        tok = self._peek()

        if tok.type == TokenType.KEYWORD_VARIABEL:
            return self._parse_var_decl()
        elif tok.type == TokenType.KEYWORD_CETAK:
            return self._parse_print()
        elif tok.type == TokenType.KEYWORD_JIKA:
            return self._parse_if()
        elif tok.type == TokenType.KEYWORD_SELAMA:
            return self._parse_while()
        elif tok.type == TokenType.KEYWORD_UNTUK:
            return self._parse_for_range()
        elif tok.type == TokenType.KEYWORD_FUNGSI:
            return self._parse_function_def()
        elif tok.type == TokenType.KEYWORD_KEMBALIKAN:
            return self._parse_return()
        elif tok.type == TokenType.KEYWORD_PANGGIL:
            return self._parse_explicit_call_stmt()
        elif tok.type == TokenType.KEYWORD_MASUKAN:
            expr = self._parse_input()
            self._match(TokenType.NEWLINE)
            return expr
        elif tok.type == TokenType.INDENT:
            raise CoreParserError(
                "Indentasi tidak terduga (spasi menjorok di luar blok pernyataan).",
                tok.line,
                tok.column,
                source_code=self.source_code,
                cause="Terdapat spasi menjorok ke dalam padahal baris sebelumnya bukan pernyataan pembuka blok (seperti 'jika', 'fungsi', 'untuk', atau 'selama').",
                solution="Hapus spasi di awal baris ini agar sejajar dengan baris lainnya."
            )
        elif tok.type == TokenType.DEDENT:
            raise CoreParserError(
                "Penutupan indentasi tidak sesuai dengan blok manapun.",
                tok.line,
                tok.column,
                source_code=self.source_code,
                cause="Tingkat spasi menjorok tidak cocok dengan tingkatan blok sebelumnya.",
                solution="Gunakan jumlah spasi yang konsisten (4 spasi per level indentasi)."
            )
        elif tok.type == TokenType.IDENTIFIER:
            # Periksa apakah nama identifier ini adalah typo dari kata kunci
            typo_kw = suggest_keyword(tok.value, list(KEYWORDS.keys()))
            
            # Jika berupa penugasan (nama = ...)
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.ASSIGN:
                return self._parse_assign()
            elif typo_kw and typo_kw != tok.value:
                # Menemukan kemungkinan typo kata kunci (misal: cetakk "halo")
                raise CoreParserError(
                    f"Pernyataan tidak dikenali '{tok.value}'.",
                    tok.line,
                    tok.column,
                    source_code=self.source_code,
                    cause=f"Kata '{tok.value}' bukan merupakan kata kunci resmi atau fungsi yang sah.",
                    solution=f"Perbaiki ejaan kata tersebut menjadi '{typo_kw}'.",
                    suggestion=typo_kw
                )
            else:
                return self._parse_implicit_call_stmt()
        else:
            raise CoreParserError(
                f"Pernyataan tidak valid atau tidak dikenali '{tok.value}'",
                tok.line,
                tok.column,
                source_code=self.source_code,
                cause="Struktur pernyataan ini tidak dikenali oleh interpreter Core.",
                solution="Periksa kembali sintaksis bahasa Core (lihat panduan di README.md)."
            )

    def _parse_var_decl(self) -> VarDecl:
        kw = self._consume(TokenType.KEYWORD_VARIABEL, "Diharapkan kata kunci 'variabel'")
        ident = self._consume(TokenType.IDENTIFIER, "Diharapkan nama variabel setelah kata kunci 'variabel'")
        self._consume(
            TokenType.ASSIGN,
            f"Diharapkan tanda '=' setelah nama variabel '{ident.value}'",
            cause=f"Variabel '{ident.value}' harus diberikan nilai awal.",
            solution=f"Gunakan tanda '=' lalu ketik nilainya, contoh: 'variabel {ident.value} = 0'."
        )
        
        value_expr = self._parse_expression()
        self._match(TokenType.NEWLINE)
        return VarDecl(name=ident.value, value_expr=value_expr, line=kw.line)

    def _parse_assign(self) -> AssignStmt:
        ident = self._consume(TokenType.IDENTIFIER, "Diharapkan nama variabel")
        self._consume(TokenType.ASSIGN, f"Diharapkan tanda '=' pada penugasan variabel '{ident.value}'")
        
        value_expr = self._parse_expression()
        self._match(TokenType.NEWLINE)
        return AssignStmt(name=ident.value, value_expr=value_expr, line=ident.line)

    def _parse_print(self) -> PrintStmt:
        kw = self._consume(TokenType.KEYWORD_CETAK, "Diharapkan kata kunci 'cetak'")
        exprs: List[ASTNode] = []

        if not self._check(TokenType.NEWLINE) and not self._is_at_end():
            exprs.append(self._parse_expression())

            while self._match(TokenType.COMMA) or (not self._check(TokenType.NEWLINE) and not self._is_at_end() and not self._check(TokenType.DEDENT)):
                if self._check(TokenType.NEWLINE) or self._is_at_end():
                    break
                exprs.append(self._parse_expression())

        self._match(TokenType.NEWLINE)
        return PrintStmt(expressions=exprs, line=kw.line)

    def _parse_if(self) -> IfStmt:
        kw = self._consume(TokenType.KEYWORD_JIKA, "Diharapkan kata kunci 'jika'")
        condition = self._parse_expression()
        self._consume(
            TokenType.NEWLINE,
            "Diharapkan baris baru setelah kondisi 'jika'",
            cause="Setelah menulis syarat 'jika', baris kode harus berpindah ke baris baru.",
            solution="Tekan tombol Enter setelah kondisi 'jika' lalu mulai blok isi dengan 4 spasi."
        )
        then_branch = self._parse_block()

        elif_branches: List[Tuple[ASTNode, Block]] = []
        else_branch: Optional[Block] = None

        self._skip_newlines()

        while self._match(TokenType.KEYWORD_LAINJIKA):
            elif_cond = self._parse_expression()
            self._consume(TokenType.NEWLINE, "Diharapkan baris baru setelah kondisi 'lainjika'")
            elif_body = self._parse_block()
            elif_branches.append((elif_cond, elif_body))
            self._skip_newlines()

        if self._match(TokenType.KEYWORD_SELAINITU):
            self._consume(TokenType.NEWLINE, "Diharapkan baris baru setelah 'selainitu'")
            else_branch = self._parse_block()

        # Deteksi kesalahan jika ada selainitu / lainjika ganda yang salah susunan
        self._skip_newlines()
        if self._check(TokenType.KEYWORD_SELAINITU):
            curr = self._peek()
            raise CoreParserError(
                "Ditemukan 'selainitu' ganda dalam satu percabangan.",
                curr.line,
                curr.column,
                source_code=self.source_code,
                cause="Dalam satu struktur 'jika', hanya diperbolehkan 1 'selainitu' di bagian paling akhir.",
                solution="Ubah 'selainitu' sebelumnya menjadi 'lainjika <kondisi>' jika Anda ingin menambah syarat pengecekan baru."
            )
        elif self._check(TokenType.KEYWORD_LAINJIKA):
            curr = self._peek()
            raise CoreParserError(
                "'lainjika' tidak boleh diletakkan setelah 'selainitu'.",
                curr.line,
                curr.column,
                source_code=self.source_code,
                cause="'selainitu' adalah penutup akhir. Semua kondisi 'lainjika' harus berada sebelum 'selainitu'.",
                solution="Pindahkan blok 'lainjika' ini ke atas sebelum blok 'selainitu'."
            )

        return IfStmt(
            condition=condition,
            then_branch=then_branch,
            elif_branches=elif_branches,
            else_branch=else_branch,
            line=kw.line
        )

    def _parse_while(self) -> WhileStmt:
        kw = self._consume(TokenType.KEYWORD_SELAMA, "Diharapkan kata kunci 'selama'")
        condition = self._parse_expression()
        self._consume(TokenType.NEWLINE, "Diharapkan baris baru setelah kondisi 'selama'")
        body = self._parse_block()
        return WhileStmt(condition=condition, body=body, line=kw.line)

    def _parse_for_range(self) -> ForRangeStmt:
        kw = self._consume(TokenType.KEYWORD_UNTUK, "Diharapkan kata kunci 'untuk'")
        var_ident = self._consume(TokenType.IDENTIFIER, "Diharapkan nama variabel pencacah setelah 'untuk'")
        self._consume(TokenType.KEYWORD_DARI, f"Diharapkan kata kunci 'dari' setelah variabel '{var_ident.value}'")
        start_expr = self._parse_addition()
        self._consume(TokenType.KEYWORD_HINGGA, "Diharapkan kata kunci 'hingga'")
        end_expr = self._parse_addition()
        self._consume(TokenType.NEWLINE, "Diharapkan baris baru setelah rentang 'untuk'")
        body = self._parse_block()
        return ForRangeStmt(var_name=var_ident.value, start_expr=start_expr, end_expr=end_expr, body=body, line=kw.line)

    def _parse_input(self) -> InputExpr:
        kw = self._consume(TokenType.KEYWORD_MASUKAN, "Diharapkan kata kunci 'masukan'")
        prompt_expr = None
        if not self._check(TokenType.NEWLINE) and not self._is_at_end() and not self._is_operator(self._peek().type):
            prompt_expr = self._parse_addition()
        return InputExpr(prompt_expr=prompt_expr, line=kw.line)

    def _parse_function_def(self) -> FunctionDef:
        kw = self._consume(TokenType.KEYWORD_FUNGSI, "Diharapkan kata kunci 'fungsi'")
        func_name = self._consume(TokenType.IDENTIFIER, "Diharapkan nama fungsi setelah kata kunci 'fungsi'")
        
        # Parameter fungsi (daftar identifier yang dipisah spasi atau koma tanpa tanda kurung)
        params: List[str] = []
        while not self._check(TokenType.NEWLINE) and not self._is_at_end():
            if self._match(TokenType.COMMA):
                continue
            param_tok = self._consume(TokenType.IDENTIFIER, f"Diharapkan nama parameter pada fungsi '{func_name.value}'")
            params.append(param_tok.value)

        self._consume(TokenType.NEWLINE, f"Diharapkan baris baru setelah deklarasi fungsi '{func_name.value}'")
        body = self._parse_block()
        return FunctionDef(name=func_name.value, params=params, body=body, line=kw.line)

    def _parse_return(self) -> ReturnStmt:
        kw = self._consume(TokenType.KEYWORD_KEMBALIKAN, "Diharapkan kata kunci 'kembalikan'")
        expr = None
        if not self._check(TokenType.NEWLINE) and not self._is_at_end():
            expr = self._parse_expression()
        self._match(TokenType.NEWLINE)
        return ReturnStmt(expr=expr, line=kw.line)

    def _parse_explicit_call_stmt(self) -> FunctionCall:
        kw = self._consume(TokenType.KEYWORD_PANGGIL, "Diharapkan kata kunci 'panggil'")
        func_name = self._consume(TokenType.IDENTIFIER, "Diharapkan nama fungsi setelah kata kunci 'panggil'")
        args = self._parse_call_arguments()
        self._match(TokenType.NEWLINE)
        return FunctionCall(name=func_name.value, args=args, line=kw.line)

    def _parse_implicit_call_stmt(self) -> FunctionCall:
        func_name = self._consume(TokenType.IDENTIFIER, "Diharapkan nama fungsi")
        args = self._parse_call_arguments()
        self._match(TokenType.NEWLINE)
        return FunctionCall(name=func_name.value, args=args, line=func_name.line)

    def _parse_call_arguments(self) -> List[ASTNode]:
        args: List[ASTNode] = []
        while not self._check(TokenType.NEWLINE) and not self._is_at_end() and not self._check(TokenType.DEDENT):
            self._match(TokenType.COMMA)
            if self._check(TokenType.NEWLINE) or self._is_at_end():
                break
            args.append(self._parse_primary_or_unary_arg())
        return args

    def _parse_primary_or_unary_arg(self) -> ASTNode:
        """Parse satu argumen pemanggilan fungsi tanpa memakan token operator liar."""
        return self._parse_comparison()

    def _parse_block(self) -> Block:
        self._consume(TokenType.INDENT, "Diharapkan blok indentasi (spasi menjorok ke dalam)")
        statements: List[ASTNode] = []

        while not self._check(TokenType.DEDENT) and not self._is_at_end():
            self._skip_newlines()
            if self._check(TokenType.DEDENT) or self._is_at_end():
                break
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()

        self._consume(TokenType.DEDENT, "Diharapkan akhir blok indentasi (dedent)")
        return Block(statements=statements)

    # --------------------------------------------------------------------------
    # Parsing Ekspresi & Presedensi Operator
    # --------------------------------------------------------------------------

    def _parse_expression(self) -> ASTNode:
        return self._parse_or()

    def _parse_or(self) -> ASTNode:
        expr = self._parse_and()
        while self._match(TokenType.KEYWORD_ATAU):
            op = self._previous()
            right = self._parse_and()
            expr = BinaryOp(left=expr, operator=op.value, right=right, line=op.line)
        return expr

    def _parse_and(self) -> ASTNode:
        expr = self._parse_not()
        while self._match(TokenType.KEYWORD_DAN):
            op = self._previous()
            right = self._parse_not()
            expr = BinaryOp(left=expr, operator=op.value, right=right, line=op.line)
        return expr

    def _parse_not(self) -> ASTNode:
        if self._match(TokenType.KEYWORD_BUKAN):
            op = self._previous()
            operand = self._parse_not()
            return UnaryOp(operator=op.value, operand=operand, line=op.line)
        return self._parse_comparison()

    def _parse_comparison(self) -> ASTNode:
        expr = self._parse_addition()
        while self._match(
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.GREATER, TokenType.LESS,
            TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL
        ):
            op = self._previous()
            right = self._parse_addition()
            expr = BinaryOp(left=expr, operator=op.value, right=right, line=op.line)
        return expr

    def _parse_addition(self) -> ASTNode:
        expr = self._parse_multiplication()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            right = self._parse_multiplication()
            expr = BinaryOp(left=expr, operator=op.value, right=right, line=op.line)
        return expr

    def _parse_multiplication(self) -> ASTNode:
        expr = self._parse_unary()
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self._previous()
            right = self._parse_unary()
            expr = BinaryOp(left=expr, operator=op.value, right=right, line=op.line)
        return expr

    def _parse_unary(self) -> ASTNode:
        if self._match(TokenType.MINUS, TokenType.PLUS):
            op = self._previous()
            operand = self._parse_unary()
            return UnaryOp(operator=op.value, operand=operand, line=op.line)
        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        tok = self._peek()

        if self._match(TokenType.NUMBER):
            return Literal(value=self._previous().value, line=tok.line)

        if self._match(TokenType.STRING):
            return Literal(value=self._previous().value, line=tok.line)

        if self._match(TokenType.KEYWORD_BENAR):
            return Literal(value=True, line=tok.line)

        if self._match(TokenType.KEYWORD_SALAH):
            return Literal(value=False, line=tok.line)

        if self._match(TokenType.KEYWORD_KOSONG):
            return Literal(value=None, line=tok.line)

        if self._match(TokenType.KEYWORD_MASUKAN):
            kw = self._previous()
            prompt_expr = None
            if not self._check(TokenType.NEWLINE) and not self._is_at_end() and not self._is_operator(self._peek().type):
                prompt_expr = self._parse_addition()
            return InputExpr(prompt_expr=prompt_expr, line=kw.line)

        if self._match(TokenType.KEYWORD_PANGGIL):
            kw = self._previous()
            func_name = self._consume(TokenType.IDENTIFIER, "Diharapkan nama fungsi setelah kata kunci 'panggil'")
            args = []
            # Baca argumen hingga operator atau akhir baris
            while not self._check(TokenType.NEWLINE) and not self._is_at_end() and not self._is_operator(self._peek().type):
                self._match(TokenType.COMMA)
                if self._check(TokenType.NEWLINE) or self._is_at_end() or self._is_operator(self._peek().type):
                    break
                args.append(self._parse_primary())
            return FunctionCall(name=func_name.value, args=args, line=kw.line)

        if self._match(TokenType.IDENTIFIER):
            return Variable(name=self._previous().value, line=tok.line)

        raise CoreParserError(f"Ekspresi tidak terduga '{tok.value}'", tok.line, tok.column)

    def _is_operator(self, t: TokenType) -> bool:
        return t in (
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.MODULO, TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER,
            TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
            TokenType.KEYWORD_DAN, TokenType.KEYWORD_ATAU
        )
