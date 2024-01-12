import pandas as pd
import os 
#crear dataframes para testear

os.system("cls")

names_to_find_path = 'namesFix.xlsx'
dfNamesToSearch = pd.read_excel(names_to_find_path)
deleted_names =[]

dfMasterTest = pd.read_excel('masterTest.xlsx')
dfAD = pd.read_excel('alreadyAdded.xlsx')

# clean the already added data sheet
# by setting the dfAD as a clean data frame and sync the excel
dfAD = pd.DataFrame([])
dfAD.to_excel('alreadyAdded.xlsx')





# desde rules, nombre por nombre, buscar en masterTest

# obtener los nombres para buscar
nameListToSearch = [name for name in dfNamesToSearch['school_nm']]

# por cada nombre, buscar en masterTest
for index_of_name_in_rules in range(len(nameListToSearch)):
    name_in_rules = nameListToSearch[index_of_name_in_rules]
    print("~"*60)
    
    
    
    # filtrar lo que no sea un string
    names_master = list(
        map(
            lambda name_in_master: str(name_in_master)
            , list(dfMasterTest['school_nm'])
        )
    )
    # buscar en masterTest
    if isinstance(name_in_rules,float): name_in_rules = str(name_in_rules)
    print("looking for " + name_in_rules + "...")
    
    
    #comparar con cada elemento (de lista y lista) estandarizado con .strip() y .lower() 
    
    exists_in_masterTest = any(
        [ name_in_master.strip().lower() == name_in_rules.strip().lower() 
         for name_in_master in names_master]
    )
    
    
    if exists_in_masterTest:
        print('found:' + name_in_rules)
        # obtener el index de la fila
        row = [ name_in_master.strip().lower() for name_in_master in names_master].index(name_in_rules.strip().lower())
        
        # hacer la modificación del archivo (pegarlooo):
        # se obtienen el nombre de las filas para pegarlas en el nuevo df
        columns = list(dfMasterTest.keys())
                                 
        try: last_index = int(dfAD.last_valid_index())+1
        except: last_index = 0
        for column in columns:
            dfAD.at[last_index, column] = dfMasterTest[column][row]
        # se actualiza el excel con la data en la ultima row disponible
        dfAD.to_excel('alreadyAdded.xlsx', index=False)
        print('modified!')
        
    else:
        print('not found')
        deleted_names.append(name_in_rules)
    
    # apartir del numero de fila, agrego una calumna found con un valor ya sea true o false
    dfNamesToSearch.at[index_of_name_in_rules,'found_column'] = str(exists_in_masterTest)
    dfNamesToSearch.to_excel(names_to_find_path)
    
    


print('done!')
print("~"*60)
print("\n"*3)
