#!/bin/bash

clear

function on_sigint {
    echo "Signal SIGINT reçu. Terminaison des processus en cours..."
    pkill -P $$
    exit
}

trap on_sigint SIGINT


delete_all_files() {
    find /home/amaurice/Bureau/benchmark-results-audal/Scaphandre -type f -name "*.txt" -delete
}
surveiller(){
    parent=$1
    nomParent=$(ps -p $parent -o comm=)
    chemin=$2
    echelle=$3
    coeurs=$4

    listePIDSurveilles=""
    while ps -p $parent > /dev/null; do
        for fils in $(pstree -p $parent | grep -o '([0-9]\+)' | grep -o '[0-9]\+'); do
            if [[ ! "$listePIDSurveilles" =~ $fils ]]; then
                nomFils=$(ps -p $fils -o comm=)

                echo $fils $nomFils >> "$chemin/scale$echelle/$((coeurs))cores/listePIDSurveilles.txt"

                listePIDSurveilles="$listePIDSurveilles $fils"
            fi
        done
    done

    du -hs "data" >> "$chemin/scale$echelle/$((coeurs))cores/parent-$nomParent-$parent.txt"
    find "data" -type f | wc -l >> "$chemin/scale$echelle/$((coeurs))cores/parent-$nomParent-$parent.txt"
}


lancement_scripts() {

    racine=$(pwd)
    cd /home/amaurice/Bureau/Stage/AudalMetadata/AdvancedMetadata/ || exit

    echelle=$1
    nombreCoeurs=$2

    for doc in $(seq 1 1 3); do
        for i in $(seq 0 1 $((nombreCoeurs-1))); do
            cores=""
            for j in $(seq 0 1 $cores); do
                cores="$cores$j,"
            done
            cores=$(echo "$cores" | sed 's/.$//')
            case $doc in
            1)
                scriptdir="/home/amaurice/Bureau/benchmark-results-audal/Scaphandre/scripts/script1"
                scriptname="1- Documents - Groupings.py"
                ;;
            2)
                scriptdir="/home/amaurice/Bureau/benchmark-results-audal/Scaphandre/scripts/script2"
                scriptname="2- Documents - Similarities-2 - CLASSIC vocabulary.py"
                ;;
            3)
                scriptdir="/home/amaurice/Bureau/benchmark-results-audal/Scaphandre/scripts/script3"
                scriptname="3- Documents - Similarities-4 - EMBEDDINGS.py"
                ;;
            esac


            echo "Exécution de la requête $doc avec $((i+1)) coeur(s) sur $((echelle))*200 documents."
            taskset -c $cores python3 -W ignore "$scriptname" &

            pere=$!

            surveiller $pere $scriptdir $echelle $((i+1))
        done
    done
    cd $racine || exit
}

ingestion(){
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


        echo "Mesure de l'ingestion des documents sur le PID $parent."
        surveiller $parent "/home/amaurice/Bureau/benchmark-results-audal/Scaphandre/ingestion" $echelle $((coeur+1))
        cd $racine || exit

    done
}

generation(){
    echelle=$1
    coeurs=$2
    
    #for i in $(seq 1 $echelle)
    for i in 1 3 5
    do
        for j in $(seq 1 $coeurs)
        do
            echo "Génération de $i*200 documents avec $j coeur(s)."

            racine=$(pwd)
            cd /home/amaurice/Bureau/Stage/DLBench/Documents/ || exit;
            python3 /home/amaurice/Bureau/Stage/DLBench/Documents/DocumentDataGen.py -S $i -J $j -B 0 &
            parent=$!
            echo "Mesure de la génération des documents sur le PID $parent."
            surveiller $parent /home/amaurice/Bureau/benchmark-results-audal/Scaphandre/generation/textes $i $j
            cd $racine || exit

        done

        ingestion $i $j

        lancement_scripts $i $j
    done
}

main() {

    scaphandre json -t 172800 -s 0 -n 100000 -m 10000 -f benchmarkScaphandre.json &
    pidScaphandre=$!
    delete_all_files
    
    generation $1 $2

    kill -9 $pidScaphandre
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
