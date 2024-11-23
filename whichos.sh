if [ "${RUNNER_OS}" == "Linux" ]; then
    echo "::set-output name=os::linux"
elif [ "${RUNNER_OS}" == "Windows" ]; then
    echo "::set-output name=os::windows"
else
    echo "::set-output name=os::macos"
fi