import subprocess
import Inputs
import Action_file
import Post_processing
import os

subprocess.run('python', 'Inputs')

subprocess.run('python', 'Action_file')

subprocess.run('python', 'Post_processing')


