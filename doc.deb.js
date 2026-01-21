dockerd --validate --config-file=/tmp/valid-config.json
configuration OK

echo $?
0

dockerd --validate --config-file /tmp/invalid-config.json
unable to configure the Docker daemon with file /tmp/invalid-config.json: the following directives don't match any configuration option: unknown-option

echo $?
1
