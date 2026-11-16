# DevOps GenAI Lab — Projeto Integrador (Unidade V)

Mini-projeto que integra CI/CD, falha controlada e análise automática com GenAI.
A atividade da Unidade V foi originalmente descrita para GitLab; este repositório
implementa o mesmo fluxo pedagógico em **GitHub + GitHub Actions**.

## Arquitetura do laboratório

1. Um Pull Request para `main` dispara o workflow.
2. O job `unit_test` executa `pytest` e captura o trace em `pytest.log`.
3. Existe uma falha lógica intencional em `calculate_shipping`: soma de `float` com `str`.
4. Quando `unit_test` falha, o job `ai_debugger` baixa o log, obtém o diff do PR,
   envia ambos à OpenAI e publica o diagnóstico como comentário no Pull Request.
5. A correção deve ser revisada por uma pessoa antes de ser aplicada.

## Arquivos principais

- `app.py` — OrderService em FastAPI com falha controlada.
- `test_app.py` — testes unitários.
- `genai_analyst.py` — agente que analisa log + diff e comenta no PR.
- `.github/workflows/ci.yml` — pipeline GitHub Actions.
- `requirements.txt` — dependências Python.

## Pré-requisito: segredo da OpenAI

No GitHub, acesse **Settings > Secrets and variables > Actions > Secrets > New repository secret**
e crie:

- Nome: `OPENAI_API_KEY`
- Valor: sua chave da OpenAI API.

Não coloque a chave no código, README, commit ou log.

Opcionalmente, em **Variables**, crie `OPENAI_MODEL`. Se não existir, o laboratório usa
`gpt-4.1-mini`.

> A assinatura do ChatGPT e o uso da OpenAI API são serviços de cobrança separados.

## Como executar a demonstração

O repositório já contém a falha controlada. Para reproduzir o fluxo:

```bash
git checkout -b feature/nova-logica
# faça uma alteração trivial no README para criar um novo commit
git add .
git commit -m "test: trigger GenAI incident analysis"
git push -u origin feature/nova-logica
```

Depois, abra um Pull Request de `feature/nova-logica` para `main`.

### Resultado esperado

- `unit_test`: **falha**, devido ao `TypeError` intencional.
- `ai_debugger`: **sucesso**, desde que `OPENAI_API_KEY` esteja configurada.
- O Pull Request recebe um comentário `DevOps-AI Bot` contendo causa-raiz,
  evidência do log, sugestão de correção e observações de segurança.

## Correção esperada após a demonstração

A falha está nesta operação:

```python
return base_price + tax_rate
```

A correção didática esperada é converter a taxa para número antes da soma:

```python
return base_price + float(tax_rate)
```

A correção não deve ser aplicada antes de capturar as evidências do pipeline e do
comentário da IA, pois a falha controlada faz parte da demonstração.

## Segurança e governança

O agente recebe logs e diffs como conteúdo não confiável e é instruído a tratá-los
somente como dados, reduzindo risco de prompt injection. O token nativo do GitHub é
usado apenas durante o workflow, e a resposta da IA é apresentada como recomendação
para revisão humana.
