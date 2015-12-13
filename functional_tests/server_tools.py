from os import path
import subprocess
THIS_FOLDER = path.dirname(path.abspath(__file__))
print("This folder path is {}".format(THIS_FOLDER)
# use the subprocess module to call some Fabric functions using the fab command.
def create_session_on_server(host, email):
    return subprocess.check_output(
        [
            'fab',
            # command-line syntax for arguments to fab functions
            'create_session_on_server:email={}'.format(email),
            '--host={}'.format(host),
            '--hide=everything,status',
        ],
        cwd=THIS_FOLDER
    #  be quite careful about extracting the session key as a string from the
    # output of the command as it gets run on the server. 
    ).decode().strip()


def reset_database(host):
    subprocess.check_call(
        ['fab', 'reset_database', '--host={}'.format(host)],
        cwd=THIS_FOLDER
    )