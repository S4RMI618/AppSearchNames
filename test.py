import pandas as pd
import requests
import levenshtein as lev

OptionIndexChosen = 'https://orgsearch.sheerid.net/rest/organization/search?type=UNIVERSITY,HIGH_SCHOOL,K12&country=US&name=High%20School%20For%20Construction%20Trades%20Engineering%20(Ozone%20Park,%20NY)'
dfPrueba = pd.read_excel('prueba.xlsx')
rowSelected = int(input("Select the row: "))

""" for i in range(8):
    print(dfPrueba['Name'][i]) """
    
nameRequired = dfPrueba['Name'][rowSelected]
print(nameRequired)
def hacer_peticion(url, query_parameters):
    try:
        # Realizar la solicitud GET con los parámetros de consulta
        response = requests.get(url, params=query_parameters)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Devolver el contenido de la respuesta en formato JSON
            return response.json()
        else:
            # Imprimir un mensaje de error si la solicitud no fue exitosa
            print(f"Error en la solicitud. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la solicitud
        print(f"Error en la solicitud: {e}")
        return None

# Ejemplo de uso
url = "https://orgsearch.sheerid.net/rest/organization/search"

parametros_consulta = {
    'type': 'UNIVERSITY,HIGH_SCHOOL,K12',
    'country': 'US',
    'name': nameRequired
}

responsexd = requests.get(url, parametros_consulta).json()

options = [ school['name'] for school in responsexd ]
options.insert(0 , 'None of the above')

for i in range(len(options)):
    print(str(i)+ ') ' + options[i])

OptionIndexChosen = int(input('Select the school: '))

if OptionIndexChosen == 0:
    print('School not found')

else: #todo: hacer que se pueda seleccionar la escuela
    print('School found')
    schoolSelected = options[OptionIndexChosen]
    dfPrueba.at[rowSelected, 'Name SheerID'] = schoolSelected
    dfPrueba.to_excel('prueba.xlsx', index=False)
    print('done')
    
dfMaster = pd.read_excel('masterTest.xlsx')
dfAD = pd.read_excel('alreadyAdded.xlsx')

columnForSeaching = dfMaster['school_nm']

if (schoolSelected in columnForSeaching):
    indexSelected = columnForSeaching.index(schoolSelected)
    copy = dfMaster.loc[indexSelected, 'A':'AJ']
    dfAD.at[dfAD.last_valid_index() + 1, 'A':'AJ'] = copy
    dfAD.to_excel('alreadyAdded.xlsx', index=False)
    
    print(schoolSelected, ' was copied to already added')
else: 
    print('School not found in master')

