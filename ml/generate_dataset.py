import pandas as pd
import random

safe_examples = [
    "print('hola mundo')",
    "x = 5; y = 10; z = x + y",
    "def suma(a,b): return a+b",
    "for i in range(10): print(i)",
    "import math; math.sqrt(25)",
    "result = ''.join(['a','b','c'])",
    "with open('archivo.txt','r') as f: data=f.read()",
    "numbers=[1,2,3]; [n*2 for n in numbers]",
    "def login(user): return f'Bienvenido {user}'",
    "usuarios = ['a', 'b']",
    "total = sum([1,2,3,4])",
    "mydict={'a':1,'b':2}",
    "import os; path=os.getcwd()",
    "sorted([5,3,1])",
    "int('5')",
    "lambda x: x*2",
    "def greet(): return 'hi'",
    "import time; time.sleep(0.1)",
    "hash('hola')",
    "json_data = {'a':1}",
    "r = requests.get('https://api.com')",
    "for k,v in {'a':1}.items(): print(k)",
    "''.strip()",
    "print('codigo seguro')",
    "list(range(5))",
]

vuln_examples = [
    "eval('2+2')",
    "exec('import os')",
    "__import__('os').system('ls')",
    "os.system('rm -rf /')",
    "subprocess.call(['rm','-rf','/'])",
    "cursor.execute('SELECT * FROM users WHERE id='+user)",
    "query = 'DELETE FROM tabla WHERE id=' + userinput",
    "password = input(); os.system(password)",
    "import pickle; pickle.loads(userinput)",
    "yaml.load(user_data)",
    "eval(user_input)",
    "exec(user_input)",
    "open('/etc/passwd')",
    "import subprocess; subprocess.Popen(usercmd)",
    "pickle.load(open(malfile))",
    "os.popen(cmd)",
    "f = open(userfile,'w'); f.write(hack)",
    "template = Template(userinput); template.render()",
    "danger = __import__(module)",
    "command = 'ping '+host; os.system(command)",
    "cursor.execute('SELECT * FROM x WHERE name=' + nombre)",
    "marshal.loads(usercode)",
    "tarfile.open(userfile)",
    "zipfile.ZipFile(userfile)",
    "pickle.loads(code)",
]

data = []

# Crear 250 seguros y 250 vulnerables
for _ in range(250):
    data.append([random.choice(safe_examples), 0])

for _ in range(250):
    data.append([random.choice(vuln_examples), 1])

df = pd.DataFrame(data, columns=["code", "label"])
df.to_csv("dataset.csv", index=False)

print("Dataset generado con éxito: 500 filas.")
