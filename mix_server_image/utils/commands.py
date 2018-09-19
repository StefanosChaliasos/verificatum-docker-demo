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


def vmnc_ciphs(path, infile='ciphertextsjson', outfile='ciphertexts',
               types=('json', 'raw')):
    sh.cd(path)
    sh.vmnc('-ciphs', '-ini', types[0], '-outi', types[1], 'protInfo.xml',
            infile, outfile)


def vmni_merge(path):
    sh.cd(path)
    sh.vmni('-merge', sh.glob('protInfo*.xml'), 'protInfo.xml')


def vmn_shuffle():
    p = sh.vmn("-shuffle", "privInfo.xml", "protInfo.xml", "ciphertexts",
               "ciphertextsout", _out=process_output, _bg=True)
    p.wait()
