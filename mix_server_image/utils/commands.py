import sh
import subprocess


def vmnc_pk():
    return sh.vmnc('-pkey', '-ini', 'json', '-outi', 'raw', 'protInfo.xml',
                   '/data/pkjson', 'publicKey')


def vmn_setpk():
    return sh.vmn('-setpk', 'publicKey')


def vmnc_ciphs():
    return sh.vmnc('-ciphs', '-ini', 'json', '-outi', 'raw', 'protInfo.xml',
                   '/data/ciphertextsjson', 'ciphertexts')


def vmni_merge():
    return subprocess.Popen('/scripts/create_prot_info.sh', shell=True,
                            stdout=subprocess.PIPE)


def vmn_shuffle():
    return subprocess.Popen('/scripts/run.sh', shell=True)
