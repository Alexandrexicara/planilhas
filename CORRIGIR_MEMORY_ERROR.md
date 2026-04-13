# Como corrigir MemoryError ao compilar com PyInstaller

## Problema
```
MemoryError während der Importation von Click em Flask
```

Este erro ocorre quando PyInstaller tenta desempacotar todos os módulos Python em memória durante a inicialização do executável.

## Causa principal
- **`--onefile`**: Cria um arquivo único que precisa extrair TUDO em memória (problema!)
- Flask é pesado demais com suas dependências (Flask + Werkzeug + Click + Jinja2 = ~50MB)
- Máquinas com RAM limitada falham durante este processo

## Soluções

### ✅ Solução 1: Usar `build_exe.py` atualizado (RECOMENDADO)
O arquivo foi atualizado para usar `--onedir` em vez de `--onefile`:

```bash
python build_exe.py
```

**Benefícios:**
- ✓ Não extrai em memória
- ✓ Startup mais rápido
- ✓ Melhor debug
- ✓ Menos problemas de compatibilidade

**Resultado:** pasta `dist/SistemaPlanilhas/` com o executável e dependências

---

### ✅ Solução 2: Usar modo ultra-leve (para RAM muito limitada)
Se ainda tiver problemas:

```bash
python build_exe_light.py
```

Configurações adicionais:
- `--strip`: Remove símbolos de debug
- `--no-include-meta-files`: Remove metadados desnecessários
- `--bootloader-ignore-signals`: Menos overhead

---

## Se continuar tendo problemas

### Opção A: Aumentar RAM Virtual
```powershell
# Se RAM física é insuficiente, aumentar arquivo de paginação
# Painel de Controle > Sistema > Configurações Avançadas > Performance
```

### Opção B: Dividir a aplicação
Se a aplicação é muito grande, em vez de executável único:

```python
# Use uma versão simplificada para executável
# app_desktop.py (versão leve, sem features pesadas)
# app.py (versão web completa)
```

### Opção C: Compilar em máquina com mais RAM
- Máquinas virtuais com 8GB+ RAM para compilação
- Considerar CI/CD (GitHub Actions, GitLab CI)

---

## Verificação rápida

Antes de compilar, teste se Flask carrega sem problemas:

```python
python -c "from flask import Flask; print('✓ Flask está OK')"
```

Se isso falhar com MemoryError na interpretação normal, o problema é com a instalação do Python, não com PyInstaller.

---

## Estrutura de saída esperada

```
dist/
└── SistemaPlanilhas/
    ├── SistemaPlanilhas.exe
    ├── _internal/  (módulos Python aqui - não em memória!)
    ├── werkzeug/
    ├── flask/
    └── ... outras dependências
```

**Nota:** O executável é 2-3 vezes maior (função normal) porque as dependências estão como arquivos, não compactadas.

---

## Próximos passos

1. Execute: `python build_exe.py`
2. Teste o executável em `dist/SistemaPlanilhas/SistemaPlanilhas.exe`
3. Se funcionar, copiar para Desktop (automático)
4. Se tiver novo erro, resolvencer conforme descrito acima

**Dúvidas?** Verifique os logs no console durante a compilação.
