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
    sh.cd(path)
    sh.vmni('-merge', sh.glob('protInfo*.xml'), 'protInfo.xml')


def vmn_shuffle():
    # FIXME
    #  sh.cd('/verificatum')
    #  sh.vmn('-shuffle', 'privInfo.xml', 'protInfo.xml', 'ciphertexts',
           #  'ciphertextsout')
    return subprocess.Popen('/scripts/run.sh', shell=True)
