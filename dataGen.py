import os
import csv
import re
from datetime import datetime
import pandas as pd

timestamp_regex = r"--(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})--"
transfer_rate_regex = r"(\d+,\d+|\d+) (KB/s|MB/s)"


with open('resultats.csv', mode='w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(['Expé', 'Date', 'Etape', 'SF', 'Volume MB', 'Nb de cœurs', 'Temps d\'exécution (s)', 'Somme (W/s)', 'CPU (W/s)', 'GPU (W/s)', 'Temps d\'exécution (s)', 'Somme (W/s)', 'CPU (W/s)', 'RAM (W/s)', 'SD (W/s)', 'NIC (W/s)'])

######## PowerJoular ########
# PowerJoular --> Chargement --> textes
"""
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
        etape = "Chargement"
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
"""



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


# Métriques "maison" --> Chargement --> textes
for scale in (1, 3, 5):
    for cores in range(1,6):
        dictionnaire = {}
        for file in os.listdir(f"Metrics/generation/textes/scale{scale}/{cores}cores"):
            if "CPU" in file:
                ommitComposant = re.search(r'(?<=-).*', file).group()

                dictionnaire[ommitComposant] = []
                cpu=0
                ram=0
                tempsExec=0
                with open(f"Metrics/generation/textes/scale{scale}/{cores}cores/CPU-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S") and float(line.split(" ")[1]) > tempsExec:
                            tempsExec = float(line.split(" ")[1])
                        if line.startswith("energy_J"):
                            try:
                                cpu = float(line.split(" ")[1])
                            except:
                                cpu = 0
                            break
                with open(f"Metrics/generation/textes/scale{scale}/{cores}cores/RAM-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            try:
                                if float(line.split(" ")[1]) > tempsExec:
                                    tempsExec = float(line.split(" ")[1])
                            except:
                                pass
                        if line.startswith("energy_J"):
                            try:
                                ram = float(line.split(" ")[1])
                            except:
                                ram = 0
                            break
                dictionnaire[ommitComposant].append(tempsExec)
                dictionnaire[ommitComposant].append(cpu)
                dictionnaire[ommitComposant].append(ram)

        nic = 0
        sd = 0
        
        for file in os.listdir(f"Metrics/generation/textes/resultatsTransferRate/scale{scale}/{cores}cores"):
            # Mettre tout le contenu du fichier dans une variable
            with open(f"Metrics/generation/textes/resultatsTransferRate/scale{scale}/{cores}cores/{file}", "r") as f:
                contenu = f.read()

                # Extraction des timestamps
                timestamps = re.findall(timestamp_regex, contenu)
                timestamp_debut = datetime.strptime(timestamps[0], "%Y-%m-%d %H:%M:%S")
                timestamp_fin = datetime.strptime(timestamps[-1], "%Y-%m-%d %H:%M:%S")

                # Calcul de la différence de temps
                duree = timestamp_fin - timestamp_debut

                # Extraction du taux de transfert moyen
                try:
                    transfer_rate = re.search(transfer_rate_regex, contenu).group(1)
                
                    nic = nic + 0.55 * (float(transfer_rate.replace(',', '.')) / 150.5) * (duree.total_seconds() + 1)
                    sd = sd + 0.45 * (float(transfer_rate.replace(',', '.')) / 150.5) * (duree.total_seconds() +1)
                except:
                    pass

            
        # Supprimer chaque élément du dictionnaire qui n'a pas les 3 composants
        for i in list(dictionnaire):
            if len(dictionnaire[i]) != 3:
                del dictionnaire[i]
        


        tempsExecMax = max([dictionnaire[i][0] for i in dictionnaire])
        sommeCPU = sum([dictionnaire[i][1] for i in dictionnaire])
        sommeNIC = nic
        sommeRAM = sum([dictionnaire[i][2] for i in dictionnaire])
        sommeSD = sd
        sommeTotal = sommeCPU + sommeNIC + sommeRAM + sommeSD

        numeroExperience = 2
        date = "12-05-2023"
        
        etape = "Chargement"
        donnees = [
            [numeroExperience, date, etape, scale, "", cores, "", "", "", "", tempsExecMax, sommeTotal, sommeCPU, sommeRAM, sommeSD, sommeNIC]
        ]

        with open('resultats.csv', mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerows(donnees)


for scale in (1, 3, 5):
    for cores in range(1,6):
        liste_paths = [f"Metrics/ingestion/scale{scale}/{cores}cores", f"Metrics/scripts/script1/scale{scale}/{cores}cores", f"Metrics/scripts/script2/scale{scale}/{cores}cores", f"Metrics/scripts/script3/scale{scale}/{cores}cores"]
        for path in liste_paths:
            dictionnaire = {}
            for file in os.listdir(path):
                ommitComposant = re.search(r'(?<=-).*', file).group()

                dictionnaire[ommitComposant] = []
                cpu=0
                nic=0
                ram=0
                sd=0
                tempsExec=0
                with open(path+f"/CPU-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            if float(line.split(" ")[1]) > tempsExec:
                                tempsExec = float(line.split(" ")[1])
                        if line.startswith("energy_J"):
                            try :
                                cpu = float(line.split(" ")[1])
                            except:
                                cpu = 0
                with open(path+f"/NIC-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            if float(line.split(" ")[1]) > tempsExec:
                                tempsExec = float(line.split(" ")[1])
                        if line.startswith("energy_J"):
                            try:
                                nic = float(line.split(" ")[1])
                            except:
                                nic = 0
                with open(path+f"/RAM-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            try:
                                if float(line.split(" ")[1]) > tempsExec:
                                    tempsExec = float(line.split(" ")[1])
                            except:
                                pass
                        if line.startswith("energy_J"):
                            try:
                                ram = float(line.split(" ")[1])
                            except:
                                ram = 0
                with open(path+f"/SD-{ommitComposant}", "r") as f:
                    for line in f:
                        if line.startswith("time_S"):
                            if float(line.split(" ")[1]) > tempsExec:
                                tempsExec = float(line.split(" ")[1])
                        if line.startswith("energy_J"):
                            try :
                                sd = float(line.split(" ")[1])
                            except:
                                sd = 0
                dictionnaire[ommitComposant].append(tempsExec)
                dictionnaire[ommitComposant].append(cpu)
                dictionnaire[ommitComposant].append(nic)
                dictionnaire[ommitComposant].append(ram)
                dictionnaire[ommitComposant].append(sd)

            tempsExecMax = max([dictionnaire[i][0] for i in dictionnaire])
            sommeCPU = sum([dictionnaire[i][1] for i in dictionnaire])
            sommeNIC = sum([dictionnaire[i][2] for i in dictionnaire])
            sommeRAM = sum([dictionnaire[i][3] for i in dictionnaire])
            sommeSD = sum([dictionnaire[i][4] for i in dictionnaire])
            if sommeSD == 0:
                sommeSD = 0
            sommeTotal = sommeCPU + sommeNIC + sommeRAM + sommeSD

            numeroExperience = 2
            date = "12-05-2023"
            
            if "ingestion" in path:
                etape = "Ingestion"
            else:
                etape = re.search(r'(script1|script2|script3)', path).group()
                
            donnees = [
                [numeroExperience, date, etape, scale, "", cores, "", "", "", "", tempsExecMax, sommeTotal, sommeCPU, sommeRAM, sommeSD, sommeNIC]
            ]

            with open('resultats.csv', mode='a', newline='') as fichier_csv:
                writer = csv.writer(fichier_csv)
                writer.writerows(donnees)

df = pd.read_csv("resultats.csv")
df = df.sort_values(by=["Etape", "SF", "Nb de cœurs"])
df.to_csv("resultats.csv", index=False)

