from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Caminho para o Microsoft Edge WebDriver
EDGE_DRIVER_PATH = "C:/automacao_python/msedgedriver.exe"  # Ajuste o caminho do driver

# Credenciais de login
EMAIL = ""  # Substitua pelo seu e-mail
SENHA = ""  # Substitua pela sua senha

# URL do Bitrix24
BITRIX_URL = "https://b24-1tvrpu.bitrix24.com.br/crm/deal/kanban/"

# Função para fazer login
def login_bitrix(driver, email, senha):
    # Esperar pelo campo de e-mail e inserir o valor
    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b24-network-auth-form-field-input-phone')))
    email_input.send_keys(email)
    time.sleep(3)
    # Clicar no botão para continuar
    botao_email = driver.find_element(By.CLASS_NAME, 'ui-btn-success')
    botao_email.click()
    
    # Tempo de espera de 3 segundos antes de inserir a senha
    time.sleep(3)

    # Esperar pelo campo de senha e inserir o valor
    senha_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b24-network-auth-form-field-input')))
    senha_input.send_keys(senha)

    # Clicar no botão para fazer login
    botao_senha = driver.find_element(By.CLASS_NAME, 'ui-btn-success')
    botao_senha.click()

# Informações do cliente (mantidas as mesmas do exemplo anterior)
cliente_info = {
    'nome': 'João Silva',
    'telefones': ['(11) 99999-9999'],
    'emails': ['joao.silva@email.com'],
    'endereco': {
        'rua': 'Av. Paulista',
        'numero': '1000',
        'complemento': 'Apt. 101',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01310-000'
    },
    'vinculos_empregaticios': 'Empresa A, Empresa B',
    'cpf': '123.456.789-00',
    'rg': '12.345.678-9',
    'sexo': 'Masculino',
    'informacoes_relevantes': 'Cliente VIP'
}

# Função para preencher o formulário do Kanban
def criar_item_kanban(driver, cliente_info):
    # Passo 1: Encontrar a coluna "Consulta assertiva" pelo nome
    coluna_elemento = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "' + cliente_info['coluna'] + '")]'))
    )
    
    # Passo 2: Subir para o container da coluna
    parent_coluna = coluna_elemento.find_element(By.XPATH, './ancestor::div[contains(@class, "crm-kanban-column")]')

    # Passo 3: Encontrar o botão 'Adicionar Item' dentro da coluna
    botao_adicionar = parent_coluna.find_element(By.CLASS_NAME, 'crm-kanban-column-add-item-button')
    botao_adicionar.click()

    # Passo 4: Aguardar o card ser gerado (esperar que a div 'crm-kanban-quick-form-container' apareça)
    form_container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'crm-kanban-quick-form-container'))
    )

    # Passo 5: Aguarde 3 segundos para garantir a renderização do formulário
    time.sleep(3)

    # Passo 6: Encontrar o botão 'Salvar' dentro do card e clicar
    botao_salvar = form_container.find_element(By.CLASS_NAME, 'ui-btn.ui-btn-xs.ui-btn-primary')
    botao_salvar.click()

    print("Item criado com sucesso na coluna:", cliente_info['coluna'])

# Função principal
def automacao_bitrix():
    # Inicializando o WebDriver para o Edge
    service = EdgeService(executable_path=EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)

    # Acessar o Bitrix e realizar login
    driver.get(BITRIX_URL)
    
    # Fazer login no Bitrix
    login_bitrix(driver, EMAIL, SENHA)

    # Tempo para garantir que a página tenha carregado após o login
    time.sleep(5)

    # Criar novo item no Kanban
    criar_item_kanban(driver, cliente_info)

    # Fechar o navegador
    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    automacao_bitrix()
