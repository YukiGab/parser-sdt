import os
import sys

SRC_ROOT = os.path.dirname(os.path.abspath(__file__))
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

import lexer.lector as lector
import parser_sdt.syntax_parser as parser
from parser_sdt.sdt import tabla_simbolos


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parser & SDT - Team 05 Compiler")
        self.root.geometry("1300x750")
        self.root.configure(bg='#2b2b2b')
        
        self.create_widgets()
        
    def create_widgets(self):
        # PanedWindow para dividir izquierda/derecha
        main_pane = tk.PanedWindow(self.root, bg='#2b2b2b', sashwidth=5, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (Entrada)
        left_frame = tk.Frame(main_pane, bg='#3c3f41')
        main_pane.add(left_frame, width=500)
        
        tk.Label(left_frame, text="📝 Code Editor", bg='#3c3f41', fg='white',
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=5, pady=5)
        
        self.code_input = scrolledtext.ScrolledText(left_frame, height=20,
                                                      font=('Consolas', 11),
                                                      bg='#2b2b2b', fg='#e6e6e6',
                                                      insertbackground='white')
        self.code_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.code_input.insert('1.0', 'float y = (2 + 3) * 4;')
        
        # Botones
        button_frame = tk.Frame(left_frame, bg='#3c3f41')
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.compile_btn = tk.Button(button_frame, text="🔨 Compile", 
                                      command=self.compile_code,
                                      bg='#4caf50', fg='white',
                                      font=('Arial', 10, 'bold'),
                                      padx=20, pady=5)
        self.compile_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = tk.Button(button_frame, text="🗑 Clear All", 
                                    command=self.clear_all,
                                    bg='#f44336', fg='white',
                                    font=('Arial', 10, 'bold'),
                                    padx=20, pady=5)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Panel derecho (Resultados)
        right_frame = tk.Frame(main_pane, bg='#3c3f41')
        main_pane.add(right_frame, width=700)
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestañas
        self.create_output_tab(notebook)
        self.create_symbol_table_tab(notebook)
        self.create_ast_tab(notebook)
        self.create_parse_table_tab(notebook)
        
    def create_output_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#3c3f41')
        notebook.add(tab, text="📤 Output")
        
        self.output_text = scrolledtext.ScrolledText(tab, font=('Consolas', 10),
                                                       bg='#1e1e1e', fg='#d4d4d4')
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.status_label = tk.Label(tab, text="✅ Ready", bg='#3c3f41', fg='#4caf50',
                                      font=('Arial', 10), anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=(0, 5))
        
    def create_symbol_table_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#3c3f41')
        notebook.add(tab, text="📋 Symbol Table")
        
        columns = ('Variable', 'Type', 'Value')
        self.symbol_tree = ttk.Treeview(tab, columns=columns, show='headings', height=18)
        
        self.symbol_tree.heading('Variable', text='Variable Name')
        self.symbol_tree.heading('Type', text='Type')
        self.symbol_tree.heading('Value', text='Value')
        
        self.symbol_tree.column('Variable', width=150)
        self.symbol_tree.column('Type', width=100)
        self.symbol_tree.column('Value', width=150)
        
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.symbol_tree.yview)
        self.symbol_tree.configure(yscrollcommand=scrollbar.set)
        
        self.symbol_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
    def create_ast_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#3c3f41')
        notebook.add(tab, text="🌲 AST (Text)")
        
        self.ast_text = scrolledtext.ScrolledText(tab, font=('Consolas', 10),
                                                    bg='#1e1e1e', fg='#d4d4d4')
        self.ast_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_parse_table_tab(self, notebook):
        tab = tk.Frame(notebook, bg='#3c3f41')
        notebook.add(tab, text="📊 Parse Table")
        
        self.parse_table_text = scrolledtext.ScrolledText(tab, font=('Consolas', 9),
                                                            bg='#1e1e1e', fg='#d4d4d4')
        self.parse_table_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def compile_code(self):
        self.output_text.delete('1.0', tk.END)
        self.ast_text.delete('1.0', tk.END)
        self.clear_symbol_table()
        
        code = self.code_input.get('1.0', tk.END).strip()
        
        if not code:
            self.append_output("[ERROR] No code to compile.\n")
            self.update_status("❌ No code to compile", 'error')
            return
            
        self.append_output(f"{'='*60}\n")
        self.append_output(f"📄 INPUT:\n{code}\n")
        self.append_output(f"{'='*60}\n\n")
        
        try:
            tokens = lector.analizeterminal(code)
            
            if tokens is None:
                self.append_output("[ERROR] Lexical analysis failed.\n")
                self.update_status("❌ Lexical Error", 'error')
                return
                
            self.append_output("[✓] Lexical analysis: SUCCESS\n\n")
            
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = parser.analizar(tokens)
            
            output = f.getvalue()
            self.append_output(output)
            
            if "Parse/AST tree:" in output:
                ast_part = output.split("Parse/AST tree:")[1].split("AST DOT generated")[0]
                self.ast_text.insert(tk.END, ast_part.strip())
            
            if result:
                self.update_status("✅ Parsing Success! SDT Verified!", 'success')
                self.append_output("\n[✓] COMPILATION SUCCESSFUL\n")
                self.load_symbol_table()
                self.load_parse_table()
            else:
                self.update_status("❌ Compilation failed", 'error')
                
        except Exception as e:
            self.append_output(f"[ERROR] {str(e)}\n")
            self.update_status(f"❌ Error: {str(e)}", 'error')
            
    def append_output(self, text):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        
    def clear_symbol_table(self):
        for item in self.symbol_tree.get_children():
            self.symbol_tree.delete(item)
            
    def load_symbol_table(self):
        from parser_sdt.sdt import tabla_simbolos
        
        self.clear_symbol_table()
        
        for name, data in tabla_simbolos.simbolos.items():
            self.symbol_tree.insert('', tk.END, values=(
                name,
                data.get('tipo', 'unknown'),
                data.get('valor', 'None')
            ))
            
        if len(tabla_simbolos.simbolos) == 0:
            self.symbol_tree.insert('', tk.END, values=('(empty)', '(empty)', '(empty)'))
            
    def load_parse_table(self):
        from parser_sdt.parsertable import tabla_action, tabla_goto
        
        self.parse_table_text.delete('1.0', tk.END)
        
        self.parse_table_text.insert(tk.END, "="*60 + "\n")
        self.parse_table_text.insert(tk.END, "ACTION TABLE (LALR)\n")
        self.parse_table_text.insert(tk.END, "="*60 + "\n\n")
        
        for state, actions in list(tabla_action.items())[:40]:
            self.parse_table_text.insert(tk.END, f"State {state}: {actions}\n")
            
        if len(tabla_action) > 40:
            self.parse_table_text.insert(tk.END, f"\n... and {len(tabla_action)-40} more states\n")
            
        self.parse_table_text.insert(tk.END, "\n" + "="*60 + "\n")
        self.parse_table_text.insert(tk.END, "GOTO TABLE\n")
        self.parse_table_text.insert(tk.END, "="*60 + "\n\n")
        
        for state, gotos in list(tabla_goto.items())[:40]:
            self.parse_table_text.insert(tk.END, f"State {state}: {gotos}\n")
            
    def update_status(self, message, status_type='normal'):
        self.status_label.config(text=message)
        
        if status_type == 'error':
            self.status_label.config(fg="#f44336")
        elif status_type == 'success':
            self.status_label.config(fg="#4caf50")
        else:
            self.status_label.config(fg="#e6e6e6")
            
    def clear_all(self):
        self.code_input.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)
        self.ast_text.delete('1.0', tk.END)
        self.clear_symbol_table()
        self.parse_table_text.delete('1.0', tk.END)
        self.update_status("✅ Ready", 'success')


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()