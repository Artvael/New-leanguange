"""
Entry point utama untuk Interpreter Bahasa Pemrograman Core (.cr).
Mendukung eksekusi file sumber .cr dan mode interaktif REPL.
"""

import sys
import os

# Memastikan output terminal Windows mendukung UTF-8
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

from src.lexer import Lexer, CoreLexerError
from src.parser import Parser, CoreParserError
from src.interpreter import Interpreter, CoreRuntimeError


def run_code(source_code: str, interpreter: Interpreter = None) -> bool:
    """Menjalankan kode sumber Core dari string."""
    if interpreter is None:
        interpreter = Interpreter()

    try:
        # 1. Analisis Leksikal (Tokenisasi)
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # 2. Analisis Sintaksis (Parsing ke AST)
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. Eksekusi Program (Interpreter)
        interpreter.run(ast)
        return True

    except CoreLexerError as err:
        print(f"\n❌ {err}")
        return False
    except CoreParserError as err:
        print(f"\n❌ {err}")
        return False
    except CoreRuntimeError as err:
        print(f"\n❌ {err}")
        return False
    except Exception as err:
        print(f"\n❌ [Kesalahan Sistem]: {err}")
        return False


def run_file(filepath: str):
    """Membaca dan mengeksekusi file .cr."""
    if not os.path.exists(filepath):
        print(f"❌ Kesalahan: File '{filepath}' tidak ditemukan.")
        sys.exit(1)

    if not filepath.endswith(".cr"):
        print(f"⚠️  Peringatan: File '{filepath}' bukan berekstensi .cr (Core). Tetap melanjutkan...")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        print(f"❌ Gagal membaca file '{filepath}': {e}")
        sys.exit(1)

    success = run_code(source_code)
    if not success:
        sys.exit(1)


def run_repl():
    """Mode interaktif REPL (Read-Eval-Print Loop) untuk bahasa Core."""
    print("=" * 60)
    print("🌟 Selamat Datang di Interpreter Bahasa Pemrograman Core (.cr) 🌟")
    print("Ketik kode Core Anda secara langsung.")
    print("Ketik 'keluar' untuk mengakhiri sesi.")
    print("=" * 60)

    interpreter = Interpreter()

    while True:
        try:
            line = input("Core > ")
            if not line.strip():
                continue
            if line.strip().lower() in ("keluar", "exit", "quit"):
                print("Sampai jumpa!")
                break

            # Jika baris adalah awal dari blok (misal: jika, selama, fungsi)
            if line.rstrip().endswith(":") or line.strip().startswith(("jika", "selama", "fungsi")):
                lines = [line]
                while True:
                    sub_line = input("...    ")
                    if sub_line == "":
                        break
                    lines.append(sub_line)
                code = "\n".join(lines)
            else:
                code = line

            run_code(code, interpreter)
        except (KeyboardInterrupt, EOFError):
            print("\nSampai jumpa!")
            break


def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()


if __name__ == "__main__":
    main()
