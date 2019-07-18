#!/bin/bash

remove_splunk_path() {
    local P=$1 D=${2:-:} path='' dir=''
    while IFS= read -r -d"$D" dir; do
        #[[ $dir$D =~ .*[Ss]plunk.* ]] || path+="$D$dir"
        [[ $dir$D =~ ${SPLUNK_HOME}.* ]] || path+="$D$dir"
    done <<< "$P$D"
    printf %s "${path#$D}"
}

unset SSL_CERT_FILE
unset LD_LIBRARY_PATH
unset PYTHONPATH

# Allow this script to be run independantly from Splunk
if [[ "$SPLUNK_HOME" ]]; then
    # Remove Splunk's python from PATH
    PATH=$(remove_splunk_path "$PATH")
    export PATH
fi

# Vary run times a bit to:
#  (1) Aide dashboard development by introducing inevitable variations within a small test deployment.
#  (2) Force time distribution (after a power outage, or sync deployment/restart, top of the min, ...)
# Allow bypassing for testing with NOSLEEP=1
[[ -z $NOSLEEP ]] && sleep $((RANDOM % 30)) >/dev/null 2>&1

# Launch the python script (same name, different extension)
exec "${0/.sh/.py}" "${@}"
