import random
from typing import Dict, Any, Optional, List
from .ast_nodes import (
    ASTNode, Program, Block, VarDecl, AssignStmt, PrintStmt,
    IfStmt, WhileStmt, ForRangeStmt, FunctionDef, ReturnStmt, FunctionCall,
    BinaryOp, UnaryOp, Literal, Variable, InputExpr
)


class CoreRuntimeError(Exception):
    """Exception khusus untuk error waktu eksekusi (runtime) berbahasa Indonesia."""
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"[Kesalahan Eksekusi] Baris {line}: {message}")


class ReturnSignal(Exception):
    """Sinyal kontrol alur internal untuk menangani 'kembalikan' dari fungsi."""
    def __init__(self, value: Any):
        self.value = value


class Environment:
    """Tabel simbol untuk mengelola variabel dan scope hierarkis."""
    def __init__(self, parent: Optional["Environment"] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: str, value: Any, line: int):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value, line)
            return
        raise CoreRuntimeError(f"Variabel '{name}' belum dideklarasikan. Gunakan 'variabel {name} = ...' terlebih dahulu.", line)

    def get(self, name: str, line: int) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name, line)
        raise CoreRuntimeError(f"Variabel atau fungsi '{name}' tidak ditemukan.", line)


class CoreFunction:
    """Representasi fungsi pengguna dalam bahasa Core."""
    def __init__(self, name: str, params: List[str], body: Block, closure: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def call(self, interpreter: "Interpreter", args: List[Any], line: int) -> Any:
        if len(args) != len(self.params):
            raise CoreRuntimeError(
                f"Fungsi '{self.name}' membutuhkan {len(self.params)} argumen, tetapi diberikan {len(args)} argumen.",
                line
            )

        # Buat scope lokal baru berdasarkan environment penutupan (closure)
        func_env = Environment(parent=self.closure)
        for param_name, arg_val in zip(self.params, args):
            func_env.define(param_name, arg_val)

        try:
            interpreter.execute_block(self.body, func_env)
        except ReturnSignal as ret:
            return ret.value

        return None


class CoreBuiltinFunction:
    """Representasi fungsi bawaan sistem dalam bahasa Core."""
    def __init__(self, name: str, arity: int, func):
        self.name = name
        self.arity = arity
        self.func = func

    def call(self, interpreter: "Interpreter", args: List[Any], line: int) -> Any:
        if self.arity != -1 and len(args) != self.arity:
            raise CoreRuntimeError(
                f"Fungsi bawaan '{self.name}' membutuhkan {self.arity} argumen, tetapi diberikan {len(args)}.",
                line
            )
        try:
            return self.func(*args)
        except Exception as e:
            raise CoreRuntimeError(f"Kesalahan pada fungsi bawaan '{self.name}': {e}", line)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self._register_builtins()

    def _register_builtins(self):
        # acak min max -> menghasilkan angka acak antara min dan max
        def _builtin_acak(a, b):
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise ValueError("Argumen 'acak' harus berupa angka.")
            a_int, b_int = int(a), int(b)
            return random.randint(min(a_int, b_int), max(a_int, b_int))

        # panjang val -> panjang string/teks
        def _builtin_panjang(val):
            return len(str(val))

        # angka val -> mengonversi string ke tipe angka
        def _builtin_angka(val):
            try:
                num = float(val)
                return int(num) if num.is_integer() else num
            except Exception:
                raise ValueError(f"Tidak dapat mengubah '{val}' menjadi angka.")

        # teks val -> mengonversi nilai ke teks
        def _builtin_teks(val):
            return self._format_value(val)

        self.global_env.define("acak", CoreBuiltinFunction("acak", 2, _builtin_acak))
        self.global_env.define("panjang", CoreBuiltinFunction("panjang", 1, _builtin_panjang))
        self.global_env.define("angka", CoreBuiltinFunction("angka", 1, _builtin_angka))
        self.global_env.define("teks", CoreBuiltinFunction("teks", 1, _builtin_teks))

    def run(self, program: Program):
        for stmt in program.statements:
            self.execute(stmt)

    def execute(self, stmt: ASTNode):
        if isinstance(stmt, VarDecl):
            val = self.evaluate(stmt.value_expr)
            self.current_env.define(stmt.name, val)

        elif isinstance(stmt, AssignStmt):
            val = self.evaluate(stmt.value_expr)
            self.current_env.assign(stmt.name, val, stmt.line)

        elif isinstance(stmt, PrintStmt):
            output_parts = []
            for expr in stmt.expressions:
                val = self.evaluate(expr)
                output_parts.append(self._format_value(val))
            print(" ".join(output_parts))

        elif isinstance(stmt, IfStmt):
            cond_val = self.evaluate(stmt.condition)
            if self._is_truthy(cond_val):
                self.execute_block(stmt.then_branch, Environment(parent=self.current_env))
                return

            # Cek setiap cabang lainjika
            executed = False
            for elif_cond, elif_body in stmt.elif_branches:
                if self._is_truthy(self.evaluate(elif_cond)):
                    self.execute_block(elif_body, Environment(parent=self.current_env))
                    executed = True
                    break

            if not executed and stmt.else_branch is not None:
                self.execute_block(stmt.else_branch, Environment(parent=self.current_env))

        elif isinstance(stmt, WhileStmt):
            while self._is_truthy(self.evaluate(stmt.condition)):
                self.execute_block(stmt.body, Environment(parent=self.current_env))

        elif isinstance(stmt, ForRangeStmt):
            start = self.evaluate(stmt.start_expr)
            end = self.evaluate(stmt.end_expr)
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                raise CoreRuntimeError("Batas rentang perulangan 'untuk' harus berupa angka.", stmt.line)
            start_int = int(start)
            end_int = int(end)
            step = 1 if start_int <= end_int else -1
            target_range = range(start_int, end_int + (1 if step == 1 else -1), step)

            for i in target_range:
                loop_env = Environment(parent=self.current_env)
                loop_env.define(stmt.var_name, i)
                self.execute_block(stmt.body, loop_env)

        elif isinstance(stmt, InputExpr):
            self.evaluate(stmt)

        elif isinstance(stmt, FunctionDef):
            func = CoreFunction(stmt.name, stmt.params, stmt.body, self.current_env)
            self.current_env.define(stmt.name, func)

        elif isinstance(stmt, ReturnStmt):
            val = self.evaluate(stmt.expr) if stmt.expr is not None else None
            raise ReturnSignal(val)

        elif isinstance(stmt, FunctionCall):
            self._call_function(stmt)

        else:
            raise CoreRuntimeError(f"Pernyataan tidak dikenal: {type(stmt).__name__}", getattr(stmt, "line", 1))

    def execute_block(self, block: Block, env: Environment):
        previous_env = self.current_env
        try:
            self.current_env = env
            for stmt in block.statements:
                self.execute(stmt)
        finally:
            self.current_env = previous_env

    def evaluate(self, expr: ASTNode) -> Any:
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Variable):
            return self.current_env.get(expr.name, expr.line)

        elif isinstance(expr, InputExpr):
            prompt = ""
            if expr.prompt_expr is not None:
                prompt = self._format_value(self.evaluate(expr.prompt_expr))
            try:
                raw = input(prompt)
            except (KeyboardInterrupt, EOFError):
                raw = ""
            stripped = raw.strip()
            # Coba konversi otomatis ke integer/float jika murni angka
            if stripped.lstrip("-").isdigit():
                return int(stripped)
            try:
                flt = float(stripped)
                return int(flt) if flt.is_integer() else flt
            except ValueError:
                return raw

        elif isinstance(expr, FunctionCall):
            return self._call_function(expr)

        elif isinstance(expr, UnaryOp):
            operand = self.evaluate(expr.operand)
            if expr.operator == "-":
                if not isinstance(operand, (int, float)):
                    raise CoreRuntimeError(f"Operator '-' hanya berlaku untuk angka, bukan '{type(operand).__name__}'", expr.line)
                return -operand
            elif expr.operator == "+":
                if not isinstance(operand, (int, float)):
                    raise CoreRuntimeError(f"Operator '+' hanya berlaku untuk angka, bukan '{type(operand).__name__}'", expr.line)
                return +operand
            elif expr.operator in ("bukan", "not"):
                return not self._is_truthy(operand)
            raise CoreRuntimeError(f"Operator unary '{expr.operator}' tidak didukung", expr.line)

        elif isinstance(expr, BinaryOp):
            # Logika hubung pendek (Short-circuit evaluation)
            if expr.operator in ("dan", "and"):
                left_val = self.evaluate(expr.left)
                if not self._is_truthy(left_val):
                    return False
                return self._is_truthy(self.evaluate(expr.right))

            if expr.operator in ("atau", "or"):
                left_val = self.evaluate(expr.left)
                if self._is_truthy(left_val):
                    return True
                return self._is_truthy(self.evaluate(expr.right))

            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            return self._evaluate_binary_op(expr.operator, left, right, expr.line)

        raise CoreRuntimeError(f"Ekspresi tidak dikenal: {type(expr).__name__}", getattr(expr, "line", 1))

    def _evaluate_binary_op(self, op: str, left: Any, right: Any, line: int) -> Any:
        if op == "+":
            # Penggabungan string ramah pemula (otomatis mengonversi jika salah satunya string)
            if isinstance(left, str) or isinstance(right, str):
                return self._format_value(left) + self._format_value(right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise CoreRuntimeError(f"Tidak dapat menjumlahkan tipe '{type(left).__name__}' dan '{type(right).__name__}'", line)

        elif op == "-":
            self._check_number_operands(op, left, right, line)
            return left - right

        elif op == "*":
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, int) and isinstance(right, str):
                return left * right
            self._check_number_operands(op, left, right, line)
            return left * right

        elif op == "/":
            self._check_number_operands(op, left, right, line)
            if right == 0:
                raise CoreRuntimeError("Kesalahan matematika: Pembagian dengan nol tidak diperbolehkan.", line)
            res = left / right
            # Jika hasil bagi adalah bilangan bulat murni, kembalikan integer
            return int(res) if res.is_integer() else res

        elif op == "%":
            self._check_number_operands(op, left, right, line)
            if right == 0:
                raise CoreRuntimeError("Kesalahan matematika: Modulo dengan nol tidak diperbolehkan.", line)
            return left % right

        elif op == "==":
            return left == right

        elif op == "!=":
            return left != right

        elif op == ">":
            self._check_comparable(op, left, right, line)
            return left > right

        elif op == "<":
            self._check_comparable(op, left, right, line)
            return left < right

        elif op == ">=":
            self._check_comparable(op, left, right, line)
            return left >= right

        elif op == "<=":
            self._check_comparable(op, left, right, line)
            return left <= right

        raise CoreRuntimeError(f"Operator biner '{op}' tidak didukung", line)

    def _call_function(self, call_node: FunctionCall) -> Any:
        func = self.current_env.get(call_node.name, call_node.line)
        if not isinstance(func, (CoreFunction, CoreBuiltinFunction)):
            raise CoreRuntimeError(f"'{call_node.name}' bukan sebuah fungsi yang dapat dipanggil.", call_node.line)
        
        args = [self.evaluate(arg) for arg in call_node.args]
        return func.call(self, args, call_node.line)

    def _check_number_operands(self, op: str, left: Any, right: Any, line: int):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise CoreRuntimeError(f"Operator '{op}' hanya dapat digunakan antar angka.", line)

    def _check_comparable(self, op: str, left: Any, right: Any, line: int):
        if type(left) != type(right) and not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
            raise CoreRuntimeError(f"Tidak dapat membandingkan '{op}' antara tipe yang berbeda ({type(left).__name__} dan {type(right).__name__}).", line)

    def _is_truthy(self, val: Any) -> bool:
        if val is None or val is False or val == 0 or val == "":
            return False
        return True

    def _format_value(self, val: Any) -> str:
        if val is True:
            return "benar"
        if val is False:
            return "salah"
        if val is None:
            return "kosong"
        return str(val)
