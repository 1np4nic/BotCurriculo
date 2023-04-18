from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import pyperclip
import csv
from tqdm import tqdm

# define links e acessa

opt = webdriver.ChromeOptions()
opt.headless = False
opt.add_argument('--disable-gpu')
opt.add_argument('start-maximized')
opt.add_argument('--disable-notifications')
opt.add_argument('--disable-extensions')
opt.add_argument('--log-level=3')
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--ignore-ssl-errors')
opt.add_experimental_option("excludeSwitches", ["enable-automation", "load-extension"])
path = r'C:/Users/Home/Contacts/Desktop/lincoln/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path=path, chrome_options=opt)

# listas vazias para apennd
anuncios_vagas = []
anuncios_vagas_externas = []
acesso_forms = []
erros_forms = []


# acessa páginas de buscas das keywords
def buscarvagas():
    raizdeurl = ('https://riovagas.com.br/?s=')
    if kw_escolha == 1:
        keywords = funcao
    elif kw_escolha == 2:
        keywords = localidade
    elif kw_escolha == 3:
        keywords = funcao + localidade

    for key in keywords:
        print(' buscando vagas para: ', key)
        loop = 1
        vagasporkw = (raizdeurl + key)
        driver.get(vagasporkw)

        # define a quatidade de páginas a serem acessadas para copia dos links de vagas
        # e classifica entre vagas internas e externas ao site
        while loop <= qt_paginas:  # <-- define a quantidade páginas a serem raspadas
            time.sleep((1)/2)
            elems = driver.find_elements_by_xpath('//h2/a[@href]')
            busca_vagas = [elem.get_attribute('href') for elem in elems]
            for i in busca_vagas:
                extract = i.split('/')
                if extract[3] == 'riovagas':
                    anuncios_vagas.append(i)
                else:
                    anuncios_vagas_externas.append(i)
            try:
                proxima_pagina = driver.find_element_by_css_selector('.next')
                driver.get(proxima_pagina.get_attribute('href'))
            except:
                pass
            loop = loop + 1
            
# depois de coletado o link de vagas de cada keyword nas páginas de busca, 
# adciona os links à lista 'anuncio_vagas'
def buscarlinksforms():
    anuncios_vagas_unicos = list(dict.fromkeys(anuncios_vagas))
    print('\n', 'Links de anúncios internos: ', len(anuncios_vagas_unicos))
    
    for link in tqdm(anuncios_vagas_unicos):
        driver.get(link)
        encontrarbotao = driver.find_elements_by_css_selector('.candidatar')
        listabotao = [elem.get_attribute('href') for elem in encontrarbotao]
        try:
            for link in listabotao:
                acesso_forms.append(str(link + '/'))
        except:
            pass

# depois de coletado o link de vagas de cada keyword na página de busca, 
# salva o link de acesso à vagas externas ao site em um arquivo csv.
def linksvagasexterna():    
    # cria variável date para inserir no nome do arquivo csv.
    date = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')

    # cria e mantém aberto arquivo csv
    csv_file = open(date+'.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['titulo', 'link_de_acesso'])

    # acessa os links da lista 'anuncios_vagas_externas' e copia o link da vaga externa no csv
    anuncios_vagas_externas_unicos = list(dict.fromkeys(anuncios_vagas_externas))
    print('\n', 'Links de anúncios externas: ', len(anuncios_vagas_externas_unicos))
    for link in tqdm(anuncios_vagas_externas_unicos):
        driver.get(link)
        try:
            titulo = driver.find_element_by_tag_name('h1').text
        except:
            titulo = 'None'
        try:
            link_vaga_externa = driver.find_element_by_xpath("//*[contains(text(), 'CANDIDATE-SE NO SITE EXTERNO')]")
            link_externo = link_vaga_externa.get_attribute('href')
        except:
            link_externo = link
        csv_writer.writerow([titulo, link_externo])
    csv_file.close()
    
# preenche o formulário de candidatura de acordo com a ordem em que estão exportos os campos
def preencherform(lista):
    lista_limpa = list(dict.fromkeys(lista))
    print('\n', 'Preenchendo formulários: ', len(lista_limpa))
    for link in tqdm(lista):
        driver.get(link)
                
        try:
        #preenche nome
            buscar_nome = driver.find_element_by_css_selector("#nome_candidato")
            buscar_nome.clear()
            Nome = 'Lincoln Menezes'
            sentence = Nome
            for character in sentence:
                        buscar_nome.send_keys(character)
        except:
            anuncios_vagas_externas.append(str(link + '/'))
            pass
            
        try:
        # preenche email
            buscar_email = driver.find_element_by_css_selector("#email_candidato")
            buscar_email.clear()
            Email = 'lincolnmenezest@outlook.com'
            sentence = Email
            for character in sentence:
                    buscar_email.send_keys(character)
        except:
            anuncios_vagas_externas.append(str(link + '/'))
            pass    
        
        try:
        # preenche celular
            buscar_cel =  driver.find_element_by_css_selector("#celular_candidato")
            buscar_cel.clear()
            Celular = '21990679713'
            sentence = Celular
            for character in sentence:
                    buscar_cel.send_keys(character)
                    time.sleep((1)/5)
        except:
            anuncios_vagas_externas.append(str(link + '/'))
            pass
        
        try:
        # preenche telefone fixo
            buscar_tel =  driver.find_element_by_css_selector("#telefone_candidato")
            buscar_tel.clear()
            Telefone = '2126571421'
            sentence = Telefone
            for character in sentence:
                    buscar_tel.send_keys(character)
                    time.sleep((1)/5)
        except:
            anuncios_vagas_externas.append(str(link + '/'))
            pass

        try:
        # preenche pretenção salarial
            buscar_pretsal = driver.find_element_by_css_selector("#pretensao_salarial")
            buscar_pretsal.clear()
            Pret_Sal = '150000'
            sentence = Pret_Sal
            for character in sentence:
                    buscar_pretsal.send_keys(character)
                    time.sleep((1)/5)
        except:
            pass
       
        try:
         # anexa path do arquivo pdf do curriculo        
            anexo_curriculo = driver.find_element_by_xpath('//*[@value="anexo"]')
            anexo_curriculo.click()
            input = driver.find_element_by_id("anexo")
            input.send_keys(r'C:\Users\Home\Contacts\Desktop\lincoln\botcurriculo\Curriculo-LincolnMenezes.pdf')
        except:
            pass

        try:
        # seleciona e preenche o campo de curriculo em texto
            clicar_botao = driver.find_element_by_xpath('//*[@value="curriculo"]')
            clicar_botao.click()
            time.sleep((1)/4)
            buscar_curriculo = driver.find_element_by_xpath('//*[@id="curriculo_candidato"]')
            buscar_curriculo.clear()
            Curriculo = r'C:\Users\Home\Contacts\Desktop\lincoln\botcurriculo\curriculo.txt'
            copy_curr = open(Curriculo, 'r').read()
            pyperclip.copy(copy_curr)
            buscar_curriculo.send_keys(Keys.CONTROL+ "v")
        except:
            pass
                
        try:
        # preenche apresentação
            buscar_apresentacao = driver.find_element_by_css_selector("#apresentacao_candidato")
            time.sleep((1)/4)
            Apresentacao = r'C:\Users\Home\Contacts\Desktop\lincoln\botcurriculo\descricao.txt'
            copy_desc = open(Apresentacao, 'r').read()
            pyperclip.copy(copy_desc)
            buscar_apresentacao.send_keys(Keys.CONTROL+ "v")
            driver.execute_script('window.scrollTo(0, 950)')
        except:
            anuncios_vagas_externas.append(str(link + '/'))
            pass 
    
        time.sleep((1)/4)
      
        try:    
        #clica no botao enviar
            botao_enviar = driver.find_element_by_xpath('//button[contains(text(), "Enviar currículo")]')
            botao_enviar.click()            
        except:
            erros_forms.append(str(link + '/'))
            pass
        
        time.sleep((1)/4)

localidade = ['nova-iguacu',
              'nilopolis',
              'mesquita',
              'queimados',
              'belford-roxo',
              'sao-joao-de-meriti',
              'duque-de-caxias',
              'japeri',
              'paracambi',
              'seropedica',
              'baixada']

funcao = ['administrativo',
           'financeiro',
           'faturamento',
           'contas+a+pagar',
           'contas+a+receber',
           'cobranca',
           'fiscal',
           'analista+financeiro',
           'analista+administrativo',
           'home-office',
           'auxiliar',
           'atendimento',
           'operacional',
           'producao',
           'logistica',
           'e-commerce',
           'call-center',
           'telemarketing']

kw_escolha = int(input('''
 [1] Busca por função.
 [2] Busca por localidade.
 [3] Buscar por funçao e por localidade.
  
 Digite a modalidade de busca: '''))
qt_paginas = int(input('\n Insira a quantidade de páginas: '))
hora_inicio = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
print('\n', 'Inciado às', hora_inicio, '\n')
buscarvagas()
buscarlinksforms()
preencherform(acesso_forms)
linksvagasexterna()
hora_termino = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
print('\n', 'Encerrado às', hora_termino)
driver.close()