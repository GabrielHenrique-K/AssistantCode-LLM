import streamlit as st
import requests
import json
import logging
import tempfile
import sys
import subprocess
import ast
from typing import Optional
import markdown

class CodeAnalysisBot:
    def __init__(self, ngrok_url: str, model_name: str = "mistral"):
        self.ngrok_url = ngrok_url
        self.model_name = model_name
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def query_ollama(self, prompt: str) -> str:
        """
        Envia requisição para o Ollama através do ngrok
        """
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        self.logger.debug(f"Enviando prompt: {prompt}")
        
        try:
            response = requests.post(
                f"{self.ngrok_url}/api/generate",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            self.logger.debug(f"Resposta bruta: {response.text}")
            json_response = json.loads(response.text)
            
            if 'response' in json_response:
                full_response = json_response['response']
                self.logger.debug(f"Resposta completa: {full_response}")
                return full_response
                
            return "Resposta vazia do servidor"
            
        except requests.RequestException as e:
            self.logger.error(f"Falha na requisição: {e}")
            return f"Erro ao fazer a requisição: {e}"

    def analyze_code(self, code: str, analysis_type: str) -> str:
        """
        Analisa o código baseado no tipo de análise solicitada
        """
        prompts = {
            "debug": (
                "Analise este código para encontrar possíveis bugs e problemas. "
                "Forneça sugestões específicas de debugging:\n\n"
                f"{code}"
            ),
            "document": (
                "Gere documentação técnica detalhada para este código, incluindo:\n"
                "- Descrição geral\n"
                "- Parâmetros e retornos\n"
                "- Exemplos de uso\n\n"
                f"{code}"
            ),
            "refactor": (
                "Analise este código e sugira melhorias específicas para:\n"
                "- Performance\n"
                "- Legibilidade\n"
                "- Boas práticas\n"
                "Forneça exemplos de código refatorado:\n\n"
                f"{code}"
            )
        }
        
        return self.query_ollama(prompts[analysis_type])

    def execute_code(self, code: str) -> tuple[str, Optional[str]]:
        """
        Executa o código com captura de saída e possíveis erros
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as temp_file:
            temp_file.write(code)
            temp_file.flush()
            
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pdb', temp_file.name],
                    capture_output=True,
                    text=True
                )
                return result.stdout, result.stderr
            except Exception as e:
                return "", str(e)

    def generate_markdown_doc(self, code: str) -> str:
        """
        Gera documentação em formato Markdown para o código
        """
        try:
            doc_prompt = (
                "Gere documentação em formato Markdown para este código. "
                "Inclua descrições detalhadas, exemplos e casos de uso:\n\n"
                f"{code}"
            )
            ai_doc = self.query_ollama(doc_prompt)
            
            tree = ast.parse(code)
            static_doc = "## Estrutura do Código\n\n"
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    static_doc += f"### {node.name}\n\n"
                    if ast.get_docstring(node):
                        static_doc += f"{ast.get_docstring(node)}\n\n"
            
            return f"{ai_doc}\n\n{static_doc}"
            
        except Exception as e:
            return f"Erro ao gerar documentação: {str(e)}"

def setup_streamlit(ngrok_url: str):
    st.set_page_config(
        page_title="Assistente de Código",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    st.title("Assistente de Código")
    
    with st.sidebar:
        st.markdown("### Configurações")
        analysis_type = st.selectbox(
            "Tipo de Análise",
            ["debug", "document", "refactor"],
            help="Escolha o tipo de análise que deseja realizar"
        )
        
        st.markdown("### Histórico")
        if st.session_state.messages:
            for msg in st.session_state.messages:
                st.text_area("", msg, height=100, disabled=True)
    
    code = st.text_area(
        "Cole seu código aqui:",
        height=200,
        help="Cole o código que deseja analisar neste campo"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Analisar", type="primary"):
            bot = CodeAnalysisBot(ngrok_url)
            
            with st.spinner("Analisando código..."):
                if analysis_type == "debug":
                    output, error = bot.execute_code(code)
                    if error:
                        st.error(f"Erro na execução: {error}")
                    else:
                        st.code(output)
                    analysis = bot.analyze_code(code, "debug")
                    
                elif analysis_type == "document":
                    analysis = bot.generate_markdown_doc(code)
                    
                else:  
                    analysis = bot.analyze_code(code, "refactor")
                
                st.markdown(analysis)
                st.session_state.messages.append(analysis)
    
    with col2:
        if st.button("Limpar Histórico"):
            st.session_state.messages = []
            st.experimental_rerun()

def main():
    # URL do ngrok 
    NGROK_URL = "https://driven-heron-typically.ngrok-free.app"
    
    setup_streamlit(NGROK_URL)

if __name__ == "__main__":
    main()