import os
import csv
import re


with open('resultats.csv', mode='w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(['Expé', 'Date', 'Etape', 'SF', 'Volume MB', 'Nb de cœurs', 'Temps d\'exécution (s)', 'Somme (W/s)', 'CPU (W/s)', 'GPU (W/s)', 'Temps d\'exécution (s)', 'Somme (W/s)', 'CPU', 'RAM', 'SD', 'NIC'])

######## PowerJoular ########
# PowerJoular --> Génération --> textes
for scale in (1, 3, 5):
    for cores in range(1,6):
        dictionnaire = {}
        for file in os.listdir(f"PowerJoular/generation/textes/scale{scale}/{cores}cores"):
            with open(f"PowerJoular/generation/textes/scale{scale}/{cores}cores/{file}", "r") as f:
                dictionnaire[file] = []
                tempsExec=0
                mesurePJ=0
                cpu=0
                gpu=0
                for line in f:
                    if line.startswith("2023"):
                        tempsExec+=1
                        values = line.split(",")
                        values[-1] = values[-1].replace("\n", "")
                        values = values[1:]
                        values = [float(i) for i in values[1:]]
                        mesurePJ+=values[0]
                        cpu+=values[1]
                        gpu+=values[2]
                    elif "data" in line:
                        volume = line.split("\t")[0]
                dictionnaire[file].append(tempsExec)
                dictionnaire[file].append(mesurePJ)
                dictionnaire[file].append(cpu)
                dictionnaire[file].append(gpu)
        numeroExperience = 1
        date = "27-04-2023"
        etape = "Génération"
        tempsExecMax = max([dictionnaire[i][0] for i in dictionnaire])
        sommeMesurePJ = sum([dictionnaire[i][1] for i in dictionnaire])
        sommeCPU = sum([dictionnaire[i][2] for i in dictionnaire])
        sommeGPU = sum([dictionnaire[i][3] for i in dictionnaire])
        
        donnees = [
            [numeroExperience, date, etape, scale, volume, cores, tempsExecMax, sommeMesurePJ, sommeCPU, sommeGPU]
        ]

        with open('resultats.csv', mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerows(donnees)

# PowerJoular --> Ingestion
for scale in (1, 3, 5):
    for cores in range(1,6):
        dictionnaire = {}
        for file in os.listdir(f"PowerJoular/ingestion/scale{scale}/{cores}cores"):
            with open(f"PowerJoular/ingestion/scale{scale}/{cores}cores/{file}", "r") as f:
                dictionnaire[file] = []
                tempsExec=0
                mesurePJ=0
                cpu=0
                gpu=0
                for line in f:
                    if line.startswith("2023"):
                        tempsExec+=1
                        values = line.split(",")
                        values[-1] = values[-1].replace("\n", "")
                        values = values[1:]
                        values = [float(i) for i in values[1:]]
                        mesurePJ+=values[0]
                        cpu+=values[1]
                        gpu+=values[2]
                    elif "data" in line:
                        volume = line.split("\t")[0]
                dictionnaire[file].append(tempsExec)
                dictionnaire[file].append(mesurePJ)
                dictionnaire[file].append(cpu)
                dictionnaire[file].append(gpu)
        numeroExperience = 1
        date = "27-04-2023"
        
        etape = "Ingestion"
        tempsExecMax = max([dictionnaire[i][0] for i in dictionnaire])
        sommeMesurePJ = sum([dictionnaire[i][1] for i in dictionnaire])
        sommeCPU = sum([dictionnaire[i][2] for i in dictionnaire])
        sommeGPU = sum([dictionnaire[i][3] for i in dictionnaire])
        
        donnees = [
            [numeroExperience, date, etape, scale, volume, cores, tempsExecMax, sommeMesurePJ, sommeCPU, sommeGPU]
        ]

        with open('resultats.csv', mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerows(donnees)




########################
########################
########################
########################
########################
########################
########################
########################
########################
########################
########################
########################
########################
########################
########################











######## Métriques "maison" ########

# Métriques "maison" --> Génération --> textes
for scale in (1, 3, 5):
    for cores in range(1,6):
        dictionnaire = {}
        for file in os.listdir(f"Metrics/generation/textes/scale{scale}/{cores}cores"):
            if "CPU" in file:
                ommitComposant = re.search(r'(?<=-).*', file).group()

                dictionnaire[ommitComposant] = []
                cpu=0
                nic=0
                ram=0
                sd=0
                with open(f"Metrics/generation/textes/scale{scale}/{cores}cores/CPU-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            tempsExec = float(line.split(" ")[1])
                            if tempsExec > 0:
                                for line in f:
                                    if line.startswith("energy_J"):
                                        try:
                                            cpu = float(line.split(" ")[1])
                                        except:
                                            cpu = 0
                                        break
                                with open(f"Metrics/generation/textes/scale{scale}/{cores}cores/NIC-{ommitComposant}", "r") as f:
                                    for line in f:
                                        if line.startswith("energy_J"):
                                            try :
                                                nic = float(line.split(" ")[1])
                                            except:
                                                nic = 0
                                            break
                                with open(f"Metrics/generation/textes/scale{scale}/{cores}cores/RAM-{ommitComposant}", "r") as f:
                                    for line in f:
                                        if line.startswith("energy_J"):
                                            try:
                                                ram = float(line.split(" ")[1])
                                            except:
                                                ram = 0
                                            break
                                with open(f"Metrics/generation/textes/scale{scale}/{cores}cores/SD-{ommitComposant}", "r") as f:
                                    for line in f:
                                        if line.startswith("energy_J"):
                                            try:
                                                sd = float(line.split(" ")[1])
                                            except:
                                                sd = 0
                                            break
                                dictionnaire[ommitComposant].append(tempsExec)
                                dictionnaire[ommitComposant].append(cpu)
                                dictionnaire[ommitComposant].append(nic)
                                dictionnaire[ommitComposant].append(ram)
                                dictionnaire[ommitComposant].append(sd)
                                break

        # Supprimer chaque élément du dictionnaire qui n'a pas les 5 composants
        for i in list(dictionnaire):
            if len(dictionnaire[i]) != 5:
                del dictionnaire[i]
        
        # Afficher tous les éléments dont nic n'est pas égal à 0
        # for i in dictionnaire:
        #     if dictionnaire[i][2] != 0:
        #         print(i, dictionnaire[i][2])


        # Afficher proprement le dictionnaire
        
        # for i in dictionnaire:
        #     print(i, dictionnaire[i])


        tempsExecMax = max([dictionnaire[i][0] for i in dictionnaire])
        sommeCPU = sum([dictionnaire[i][1] for i in dictionnaire])
        sommeNIC = sum([dictionnaire[i][2] for i in dictionnaire])
        sommeRAM = sum([dictionnaire[i][3] for i in dictionnaire])
        sommeSD = sum([dictionnaire[i][4] for i in dictionnaire])
        sommeTotal = sommeCPU + sommeNIC + sommeRAM + sommeSD

        # Afficher proprement toutes les valeurs
        # print(f"scale{scale} - {cores}cores")
        # print(f"Temps d'exécution max : {tempsExecMax}")
        # print(f"Somme CPU : {sommeCPU}")
        # print(f"Somme NIC : {sommeNIC}")
        # print(f"Somme RAM : {sommeRAM}")
        # print(f"Somme SD : {sommeSD}")
        # print(f"SOMME TOTALE : {sommeTotal} JOULES ou W/s")
        # print("\n")

        numeroExperience = 1
        date = "28-04-2023"
        
        etape = "Génération"
        donnees = [
            [numeroExperience, date, etape, scale, "", cores, "", "", "", "", tempsExecMax, sommeTotal, sommeCPU, sommeRAM, sommeNIC, sommeSD]
        ]

        with open('resultats.csv', mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerows(donnees)


# Métriques "maison" --> Ingestion
for scale in (1, 3):
    for cores in range(1,6):
        dictionnaire = {}
        for file in os.listdir(f"Metrics/ingestion/scale{scale}/{cores}cores"):
            if "CPU" in file:
                ommitComposant = re.search(r'(?<=-).*', file).group()

                dictionnaire[ommitComposant] = []
                cpu=0
                nic=0
                ram=0
                sd=0
                with open(f"Metrics/ingestion/scale{scale}/{cores}cores/CPU-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            tempsExec = float(line.split(" ")[1])
                            if tempsExec > 0:
                                for line in f:
                                    if line.startswith("energy_J"):
                                        try :
                                            cpu = float(line.split(" ")[1])
                                        except:
                                            cpu = 0
                                        break
                                with open(f"Metrics/ingestion/scale{scale}/{cores}cores/NIC-{ommitComposant}", "r") as f:
                                    for line in f:
                                        if line.startswith("energy_J"):
                                            try:
                                                nic = float(line.split(" ")[1])
                                            except:
                                                nic = 0
                                            break
                                with open(f"Metrics/ingestion/scale{scale}/{cores}cores/RAM-{ommitComposant}", "r") as f:
                                    for line in f:
                                        if line.startswith("energy_J"):
                                            try:
                                                ram = float(line.split(" ")[1])
                                            except:
                                                ram = 0
                                            break
                                with open(f"Metrics/ingestion/scale{scale}/{cores}cores/SD-{ommitComposant}", "r") as f:
                                    for line in f:
                                        if line.startswith("energy_J"):
                                            try :
                                                sd = float(line.split(" ")[1])
                                            except:
                                                sd = 0
                                            break
                                dictionnaire[ommitComposant].append(tempsExec)
                                dictionnaire[ommitComposant].append(cpu)
                                dictionnaire[ommitComposant].append(nic)
                                dictionnaire[ommitComposant].append(ram)
                                dictionnaire[ommitComposant].append(sd)
                                break

        # Supprimer chaque élément du dictionnaire qui n'a pas les 5 composants
        for i in list(dictionnaire):
            if len(dictionnaire[i]) != 5:
                del dictionnaire[i]
        


        # Afficher proprement le dictionnaire
        
        # for i in dictionnaire:
        #     print(i, dictionnaire[i])

        tempsExecMax = max([dictionnaire[i][0] for i in dictionnaire])
        sommeCPU = sum([dictionnaire[i][1] for i in dictionnaire])
        sommeNIC = sum([dictionnaire[i][2] for i in dictionnaire])
        sommeRAM = sum([dictionnaire[i][3] for i in dictionnaire])
        sommeSD = sum([dictionnaire[i][4] for i in dictionnaire])
        sommeTotal = sommeCPU + sommeNIC + sommeRAM + sommeSD

        # Afficher proprement toutes les valeurs
        # print(f"scale{scale} - {cores}cores")
        # print(f"Temps d'exécution max : {tempsExecMax}")
        # print(f"Somme CPU : {sommeCPU}")
        # print(f"Somme NIC : {sommeNIC}")
        # print(f"Somme RAM : {sommeRAM}")
        # print(f"Somme SD : {sommeSD}")
        # print(f"SOMME TOTALE : {sommeTotal} JOULES ou W/s")
        # print("\n")

        numeroExperience = 1
        date = "28-04-2023"
        
        etape = "Ingestion"
        donnees = [
            [numeroExperience, date, etape, scale, "", cores, "", "", "", "", tempsExecMax, sommeTotal, sommeCPU, sommeRAM, sommeNIC, sommeSD]
        ]

        with open('resultats.csv', mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerows(donnees)