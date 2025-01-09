# Code Analysis Assistant

Um assistente de código Python que utiliza IA para ajudar desenvolvedores com análise, depuração e documentação de código. O projeto integra Streamlit para interface gráfica e se conecta a um modelo de linguagem (Ollama) através de ngrok.

## 🚀 Funcionalidades

- **Análise de Código**: Identificação de bugs potenciais e problemas de código
- **Documentação Automática**: Geração de documentação técnica em formato Markdown
- **Sugestões de Refatoração**: Recomendações para melhorar performance e legibilidade
- **Debug Interativo**: Integração com pdb para depuração de código
- **Interface Amigável**: UI intuitiva construída com Streamlit
- **Histórico de Análises**: Mantém registro das análises realizadas

## 📋 Pré-requisitos

- Python 3.12
- pip (gerenciador de pacotes Python)
- Acesso a um servidor Ollama através de ngrok

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone 
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure a URL do ngrok:
Abra o arquivo `main.py` e atualize a variável `NGROK_URL` com sua URL do ngrok:
```python
NGROK_URL = "sua-url-ngrok-aqui"
```

## 💻 Uso

1. Inicie a aplicação:
```bash
streamlit run main.py
```

2. Acesse a interface web através do navegador (geralmente em `http://localhost:8501`)

3. Cole seu código na área de texto

4. Selecione o tipo de análise desejada:
   - Debug: Para encontrar e corrigir bugs
   - Document: Para gerar documentação
   - Refactor: Para sugestões de melhorias

5. Clique em "Analisar" para obter os resultados

## 📚 Exemplos de Uso

### Análise de Bugs
```python
def calcular_media(notas):
    total = 0
    for nota in notas:
        total += nota
    return total/len(notas)  # Potencial divisão por zero
```

### Geração de Documentação
```python
class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = {}
        self.contador_id = 0
    
    def adicionar_tarefa(self, titulo, descricao, prioridade=1):
        # Adiciona uma nova tarefa
        pass
```

## 🛠️ Estrutura do Projeto

```
code-analysis-assistant/
├── main.py              # Arquivo principal
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
└── tests/              # Testes unitários
```

## 📦 Dependências Principais

- `streamlit`: Interface gráfica web
- `requests`: Comunicação HTTP com o servidor Ollama
- `markdown`: Processamento de documentação Markdown

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚠️ Limitações Conhecidas

- Requer conexão ativa com servidor Ollama
- Análise de código limitada ao tamanho máximo aceito pelo modelo
- Algumas sugestões de refatoração podem precisar de revisão manual


## ✨ Próximos Passos

- [ ] Adicionar suporte a mais linguagens de programação
- [ ] Implementar cache de respostas frequentes
- [ ] Melhorar a análise estática de código
- [ ] Adicionar exportação de relatórios
- [ ] Implementar testes automatizados
