# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import traceback

def captcha(driver):
	resposta = input('Digite o captcha: ')
	resposta_field = driver.find_element_by_xpath('/html/body/div[3]/form/div[3]/div[4]/div[2]/div/div/table/tbody/tr[1]/td/div/div[2]/label/input')
	resposta_field.send_keys(resposta)
	captcha_send =  driver.find_element_by_xpath('//*[@id="ctl00_cphContent_gdvResultadoBusca_btEntrar"]')
	captcha_send.click()

def is_captcha(driver):
	try:
		WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath('/html/body/div[3]/form/div[3]/div[4]/div[2]/div/div/table/tbody/tr[1]/td/div/div[2]/label'))
	except Exception:
		return False
	return True
	
def get_link(driver):
	list = []
	count = 2
	while count <= 16:
		if count >= 10:
			i = str(count)
		else:
			i = '0' + str(count)
		try:
			list.append(WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl%s_lbtSelecionar"]' % i).text))
		except Exception:
			print("Exception no get_link")
			return list
		count += 1
	return list

def next_page(driver):
	print('entrei no next_page')
	# texto_antigo = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="jo_encontrados"]'))
		# prox_pagina = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText"]'))
	prox_pagina = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText"]')
	prox_pagina.click()

	#Check if there is a captcha 
	if(is_captcha(driver)):
		captcha(driver)

	# if current text is different from previous, means the new items of the new page have loaded
	# while True:
	# 	controle_de_espera = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="jo_encontrados"]'))
	# 	if controle_de_espera.text != texto_antigo.text:
	# 		break
	# print('saiu do break')


def get_company_info(driver):
	try:
		nome = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblEmpresa"]').text
		cnpj = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblCnpj"]').text
		tipo = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblObjeto"]').text
		atividade = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblAtividade"]').text
		logradouro = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblLogradouro"]').text
		num = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblNumero"]').text
		complemento = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblComplemento"]').text
		cep = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblCep"]').text
		municipio = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblMunicipio"]').text
		uf = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblUf"]').text
	except Exception:
		input('Preencha o captcha e digite qualquer coisa ')
		nome = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblEmpresa"]').text
		cnpj = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblCnpj"]').text
		tipo = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblObjeto"]').text
		atividade = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblAtividade"]').text
		logradouro = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblLogradouro"]').text
		num = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblNumero"]').text
		complemento = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblComplemento"]').text
		cep = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblCep"]').text
		municipio = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblMunicipio"]').text
		uf = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblUf"]').text

	try:
		objeto = re.search('(.*)\n',tipo).group(1)
	except Exception:
		try:
			objeto = re.search('(.*),',link).group(1)
		except Exception:
			objeto = " "

	with open('Empresas.xlsx','a') as f:
		f.write(nome + '|' + cnpj + '|' + objeto + '|' + atividade + '|' + logradouro + ' - ' + num + ' - ' + complemento + '|' + 
			cep + '|' +	municipio + '|' + uf + "\n")




# open browser and navigate to URL
driver = webdriver.Firefox()
driver.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx')

# Fill the form with Vila Olímpia in field Bairro and submit
bairro = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmBuscaAvancada_txtBairro"]'))
data_abertura = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio"]'))
cidade = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmBuscaAvancada_txtMunicipio"]')
pesquisar = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmBuscaAvancada_btPesquisar"]'))
data_abertura.send_keys('11/09/2018') #feito dia 17/12
bairro.send_keys('Vila Olímpia')
cidade.send_keys('Sao Paulo')

pesquisar.click()

#Check if there is a captcha 
if(is_captcha(driver)):
	captcha(driver)
	
lista_nire = []

num_pag = 1

while True:
	print('pagina ' + str(num_pag))
	lista_nire.append(get_link(driver))
	try:
		next_page(driver)
	except Exception:
		traceback.print_exc()
		print('Exception next_page')
		break

	num_pag += 1

for pagina in lista_nire:
	for elemento in pagina:
		driver.get('https://www.jucesponline.sp.gov.br/Pre_Visualiza.aspx?nire=%s&idproduto=' % str(elemento)) # str to be sure
		get_company_info(driver)
#		try:
#			get_company_info(driver)
#		except Exception:
#			if(is_captcha(driver)):
#				captcha(driver)
#			get_company_info(driver)




# link = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl02_lbtSelecionar"]'))
# link.click()

# for x in get_link(driver):
# 	print(x)

# #Check if there is a captcha 
# if(is_captcha(driver)):
# 	captcha(driver)

# print('passou pelo segundo ')

# Nome_restaurante = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblEmpresa"]').text)
# Cnpj = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblCnpj"]').text)
# Rua = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblLogradouro"]').text)
# Numero = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblNumero"]').text)
# Bairro = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblBairro"]').text)
# Cidade = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblMunicipio"]').text)
# CEP = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath('//*[@id="ctl00_cphContent_frmPreVisualiza_lblCep"]').text)

# print('Nome do Restaurante: ' + Nome_restaurante + "\n" +
# 	' CNPJ: ' + Cnpj + '\n' +
# 	' Endereço: ' + Rua + ',' + Numero + '-' + Bairro + ',' + Cidade + '\n' +
# 	' CEP: ' + CEP )


# itens de links na tabela de resultados 
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl02_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl03_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl04_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl05_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl06_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl07_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl08_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl09_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl10_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl11_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl12_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl13_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl14_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl15_lbtSelecionar"]
# //*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl16_lbtSelecionar"]
