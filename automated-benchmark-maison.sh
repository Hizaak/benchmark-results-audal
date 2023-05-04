#!/bin/bash

clear

function on_sigint {
    echo "Signal SIGINT reçu. Terminaison des processus en cours..."
    pkill -P $$
    exit
}

trap on_sigint SIGINT

delete_all_files() {
    #Document
    find /home/amaurice/Bureau/Stage/DLBench/Documents/benchmarkHumberto -type f -name "*.txt" -delete
    find /home/amaurice/Bureau/Stage/DLBench/Documents/benchmarkHumberto -type f -name "*.csv" -delete

    #Ingestion
    find /home/amaurice/Bureau/Stage/AudalMetadata/BasicMetadata/benchmarkHumberto -type f -name "*.txt" -delete
    find /home/amaurice/Bureau/Stage/AudalMetadata/BasicMetadata/benchmarkHumberto -type f -name "*.csv" -delete

    #Scripts
    find /home/amaurice/Bureau/Stage/AudalMetadata/AdvancedMetadata/benchmarkHumberto -type f -name "*.txt" -delete
    find /home/amaurice/Bureau/Stage/AudalMetadata/AdvancedMetadata/benchmarkHumberto -type f -name "*.csv" -delete
}

surveiller(){
    parent=$1
    nomParent=$(ps -p $parent -o comm=)
    chemin=$2
    echelle=$3
    coeurs=$4

    metrics $parent "$chemin/scale$echelle/$((coeurs))cores" "parent-$nomParent-$parent" &
    listePIDSurveilles=""

    while ps -p $parent > /dev/null; do
        for fils in $(pstree -p $parent | grep -o '([0-9]\+)' | grep -o '[0-9]\+'); do
            if [[ ! "$listePIDSurveilles" =~ $fils ]]; then
                    nomFils=$(ps -p $fils -o comm=)

                    metrics $fils "$chemin/scale$echelle/$((coeurs))cores" "fils-$nomFils-$fils" &
                    listePIDSurveilles="$listePIDSurveilles $fils"
            fi
        done
    done

    du -hs "data" >> "$chemin/scale$echelle/$((coeurs))cores/parent-$nomParent-$parent.txt"
    find "data" -type f | wc -l >> "$chemin/scale$echelle/$((coeurs))cores/parent-$nomParent-$parent.txt"
    find "$chemin" -type f -name "*--*.txt" -delete
}

ingestion_maison(){
    echelle=$1
    nombreCoeurs=$2

    for coeur in $(seq 0 $((nombreCoeurs-1)))
    do
        coeurs=""
        for k in $(seq 0 $coeur)
        do
            coeurs="$coeurs$k,"
        done
        coeurs=$(echo "$coeurs" | sed 's/.$//')

        echo "Ingestion de $echelle*200 documents avec $coeur coeur(s)."

        racine=$(pwd)

        cd /home/amaurice/Bureau/Stage/AudalMetadata/BasicMetadata || exit;
        JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
        taskset -c $coeurs  /usr/lib/apache-netbeans/java/maven/bin/mvn "-Dexec.args=-classpath %classpath com.datalake.basicmetadata.Main" -Dexec.executable=/usr/lib/jvm/java-11-openjdk-amd64/bin/java -Dexec.vmArgs= -Dexec.appArgs= --no-transfer-progress org.codehaus.mojo:exec-maven-plugin:1.5.0:exec &

        parent=$!

        cd $racine || exit

        echo "Mesure de l'ingestion des documents sur le PID $parent."
        surveiller $parent "/home/amaurice/Bureau/Stage/AudalMetadata/BasicMetadata/benchmarkHumberto" $echelle $((coeur+1))

    done
}

generation_maison(){
    echelle=$1
    coeurs=$2
    
    for i in $(seq 1 $echelle)
    do
        for j in $(seq 1 $coeurs)
        do
            echo "Génération de $i*200 documents avec $j coeur(s)."

            racine=$(pwd)
            cd /home/amaurice/Bureau/Stage/DLBench/Documents/ || exit;
            python3 /home/amaurice/Bureau/Stage/DLBench/Documents/DocumentDataGen.py -S $i -J $j -B 1 &
            parent=$!
            cd $racine || exit
            echo "Mesure de la génération des documents sur le PID $parent."
            surveiller $parent "/home/amaurice/Bureau/Stage/DLBench/Documents/benchmarkHumberto" $i $j
        done

        ingestion_maison $i $j

        echo "
        racine=$(pwd)
        cd /home/amaurice/Bureau/Stage/AudalMetadata/AdvancedMetadata/
        bash lancementScriptsPowerJoular.sh $echelle $coeurs
        cd $racine"
    done
}

main() {
    delete_all_files
    generation_maison $1 $2
}

if [ $# -eq 0 ]; then
    echo "Entrez l'échelle : "
    read echelle
    echo "Entrez le nombre de coeurs : "
    read coeurs
else
    echelle=$1
    coeurs=$2
fi

main $echelle $coeurs