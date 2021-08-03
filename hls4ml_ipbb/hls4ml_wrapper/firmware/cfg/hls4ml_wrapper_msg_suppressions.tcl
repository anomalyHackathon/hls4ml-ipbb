
# Suppress warnings for unconnected ports (as null payload doesn't use many ports)
set_msg_config -severity warning  -id {[Synth 8-3331]} -string "design emp_payload has unconnected port" -new_severity info