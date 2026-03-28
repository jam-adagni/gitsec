rule Suspicious_File_Write
{
    strings:
        $a = "open(" nocase
        $b = "write(" nocase
    condition:
        $a and $b
}

rule Suspicious_Exec
{
    strings:
        $a = "os.system" nocase
        $b = "subprocess" nocase
    condition:
        any of them
}

rule Data_Exfiltration
{
    strings:
        $a = "socket" nocase
        $b = "connect" nocase
        $c = "requests" nocase
    condition:
        any of them
}

rule Keylogger_Advanced
{
    strings:
        $a = "pynput" nocase
        $b = "keyboard" nocase
        $c = "keylogger" nocase
        $d = "log_keys" nocase
    condition:
        any of them
}