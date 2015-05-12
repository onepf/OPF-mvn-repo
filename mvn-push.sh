#!/bin/bash
set -o nounset
set -o errexit

readonly MVN_REPO=$(dirname $(readlink -e $0))
GROUP_ID=""
ARTIFACT_ID=""
VERSION=""
FILE=""
SOURCES=""
JAVADOC=""

CLEANUP=""

# Handle arguments
while [[ $# > 0 ]]; do
    key="$1"

    case $key in
        -h|--help)
            echo "mvn-push --group package --id package --version version --file file [--javadoc file|path] [--sources file]"
            exit 0
        ;;
        --group)
            shift
            readonly GROUP_ID="$1"
        ;;
        --id)
            shift
            readonly ARTIFACT_ID="$1"
        ;;
        --version)
            shift
            readonly VERSION="$1"
        ;;
        --file)
            shift
            readonly FILE=$(readlink -e $1)
        ;;
        --sources)
            shift
            readonly SOURCES=$(readlink -e $1)
        ;;
        --javadoc)
            shift
            JAVADOC=$(readlink -e $1)
        ;;
        *)
            echo "Unknown option $1"
            exit 1
        ;;
    esac
    shift
done

# Validate arguments
if [[ -z ${GROUP_ID} ]]; then
    echo "group is empty or invalid."
    exit 1
elif [[ -z ${ARTIFACT_ID} ]]; then
    echo "id is empty or invalid."
    exit 1
elif [[ -z ${VERSION} ]]; then
    echo "version is empty or invalid."
    exit 1
elif [[ -z ${FILE} ]]; then
    echo "file is empty or invalid."
    exit 1
fi

# Detect packaging
if [[ ${FILE: -4} == ".aar" ]]; then
    PACKAGING="aar"
else
    PACKAGING="jar"
fi
readonly PACKAGING

# Pack docs in jar if necessary
if [[ -d ${JAVADOC} ]]; then
    tempJar=$(basename ${FILE})
    tempJar="${MVN_REPO}/${tempJar/.jar/-javadoc.jar}"
    cd ${JAVADOC}
    jar cf ${tempJar} ./*
    cd -
    JAVADOC=${tempJar}
    CLEANUP="${CLEANUP} ${tempJar}"
    unset tempJar
fi
readonly JAVADOC


MVN_DEPLOY="deploy:deploy-file
        -Durl=file://${MVN_REPO} \
        -DgroupId=${GROUP_ID} \
        -DartifactId=${ARTIFACT_ID} \
        -Dversion=${VERSION} \
        -Dpackaging=${PACKAGING} \
        -Dfile=${FILE}"
if [[ -n ${SOURCES} ]]; then
    MVN_DEPLOY="${MVN_DEPLOY} \
    -Dsources=${SOURCES}"
fi
if [[ -n ${JAVADOC} ]]; then
    MVN_DEPLOY="${MVN_DEPLOY} \
    -Djavadoc=${JAVADOC}"
fi
readonly MVN_DEPLOY

mvn ${MVN_DEPLOY}

if [[ -n ${CLEANUP} ]]; then
    rm ${CLEANUP}
fi

exit 0