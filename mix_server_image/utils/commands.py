import sh
import subprocess


def vmnc_pk(path):
    return sh.vmnc('-pkey', '-ini', 'json', '-outi', 'raw', 'protInfo.xml',
                   path + '/pkjson', 'publicKey')


def vmn_setpk():
    return sh.vmn('-setpk', 'publicKey')


def vmnc_ciphs(path):
    return sh.vmnc('-ciphs', '-ini', 'json', '-outi', 'raw', 'protInfo.xml',
                   path + '/ciphertextsjson', 'ciphertexts')


def vmni_merge(path):
    # FIXME
    return subprocess.Popen('/scripts/create_prot_info.sh', shell=True,
                            stdout=subprocess.PIPE)


def vmn_shuffle():
    # FIXME
    return subprocess.Popen('/scripts/run.sh', shell=True)
