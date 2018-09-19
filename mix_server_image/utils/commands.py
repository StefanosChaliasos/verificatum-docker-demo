import sh


def process_output(line, stdin, process):
    print(line)
    if "ERROR" in line:
        process.kill()
        return True


def vmnc_pk(path):
    return sh.vmnc('-pkey', '-ini', 'json', '-outi', 'raw', 'protInfo.xml',
                   path + '/pkjson', 'publicKey')


def vmn_setpk():
    return sh.vmn('-setpk', 'publicKey')


def vmnc_ciphs(path):
    return sh.vmnc('-ciphs', '-ini', 'json', '-outi', 'raw', 'protInfo.xml',
                   path + '/ciphertextsjson', 'ciphertexts')


def vmni_merge(path):
    sh.cd(path)
    sh.vmni('-merge', sh.glob('protInfo*.xml'), 'protInfo.xml')


def vmn_shuffle():
    p = sh.vmn("-shuffle", "privInfo.xml", "protInfo.xml", "ciphertexts",
               "ciphertextsout", _out=process_output, _bg=True)
    p.wait()
