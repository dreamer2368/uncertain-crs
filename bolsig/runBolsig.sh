waitall() {
local rc=0
local rcsum=0
flux queue drain
local k=0
for job in $@
do
    flux job status ${job} || rc=$?
    echo "${k}-th job id: ${job}, FAIL: ${rc}"
    if [ $rc -ne 0 ]; then
        flux job attach ${job}
        flux job info ${job} R
        let "rcsum+=1"
    fi
    let "k+=1"; rc=0
done
if [ $rcsum -gt 0 ]; then
    return 1
else
    return 0
fi
}

JOBIDS=""
for proc in {0..71}
do
JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=/p/lustre1/chung28/lxcat-review/bolsig/out/bolsig_result_${proc}.out ./bolsigminus-linux${proc} /p/lustre1/chung28/lxcat-review/bolsig/forward-propagate/input/rate300K.${proc}.dat)"
JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=/p/lustre1/chung28/lxcat-review/bolsig/out/bolsig_result_${proc}.out ./bolsigminus-linux${proc} /p/lustre1/chung28/lxcat-review/bolsig/forward-propagate/input/transport300K.${proc}.dat)"
JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=/p/lustre1/chung28/lxcat-review/bolsig/out/bolsig_result_${proc}.out ./bolsigminus-linux${proc} /p/lustre1/chung28/lxcat-review/bolsig/forward-propagate/input/transport77K.${proc}.dat)"
JOBIDS="$JOBIDS $(flux mini submit -n 1 --output=/p/lustre1/chung28/lxcat-review/bolsig/out/bolsig_result_${proc}.out ./bolsigminus-linux${proc} /p/lustre1/chung28/lxcat-review/bolsig/forward-propagate/input/transport90K.${proc}.dat)"
done

waitall ${JOBIDS}
if [ $? -ne 0 ]; then
   echo "running bolsig failed."
   exit -1
else
   echo "running bolsig succeeded."
fi

