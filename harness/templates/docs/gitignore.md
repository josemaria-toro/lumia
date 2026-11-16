# Fragmentos de .gitignore por tecnología

Usa siempre estas entradas comunes y añade las de los tipos seleccionados.

```gitignore
# Secretos (nunca al repositorio; se permite .env.example)
.env
.env.*
!.env.example
*.pem
*.key
*.snk
*.pfx
secrets/

# Python
.venv/
__pycache__/
*.py[cod]
.mypy_cache/
.ruff_cache/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/

# C#
bin/
obj/
*.user
TestResults/
coverage*.xml

# React / Node
node_modules/
dist/
coverage/
playwright-report/
test-results/
.vite/

# IDE / SO
.idea/
.vscode/
.DS_Store
```
