import os
import subprocess
import sys
import xml.etree.ElementTree as ET
plantUML_path=''
repo_path=''
plantUML_res_path=""
hash_path=''
def get_commit_dependencies(file_hash):
    result = subprocess.run(f"git -C {repo_path} log --pretty=format:%H --all --find-object={file_hash}", shell=True, capture_output=True, text=True)
    commit_list = result.stdout.strip().splitlines()
    
    dependencies = {}
    for commit in commit_list:
        dependencies[commit]=[]
        parent_cmd = f"git -C {repo_path}  log --pretty=%P -n 1 {commit}"
        parents = subprocess.run(parent_cmd, shell=True, capture_output=True, text=True).stdout.strip().split()

        for parent in parents:
            dependencies[commit].append(parent)

    return dependencies


def create_plantuml_file(dependencies):

    with open(f"{plantUML_res_path}/graph.puml", "w") as f:

        f.write("@startuml\n")
        f.write("skinparam style strictuml\n")

        # Определяем узлы для коммитов

        for commit in dependencies.keys():
            f.write(f'entity "{commit[:6]}"\n')
            for parent in dependencies[commit]:
                if not(list(dependencies.keys()).count(parent)):
                    f.write(f'entity "{parent[:6]}" #red\n')
        # Определяем зависимости между коммитами
        for commit in dependencies:
            for parent in dependencies[commit]:
                f.write(f'"{commit[:6]}" --> "{parent[:6]}"\n')

        f.write("@enduml\n")


def generate_graph_image():

    result = subprocess.run(f"java -jar {plantUML_path} {plantUML_res_path}/graph.puml", shell=True)
    return result.returncode == 0


def main():
    global plantUML_path,repo_path,plantUML_res_path,hash_path
    tree = ET.parse('C:/Users/vlaso_n8/PycharmProjects/pythonProject/konfig/dz2/konfig.xml')
    root = tree.getroot()
    plantUML_path=str(root.findall("plantUML")[0].text.encode('utf8'))[2:-1]
    repo_path=str(root.findall("repo")[0].text.encode('utf8'))[2:-1]
    plantUML_res_path=str(root.findall("plantUML_res")[0].text.encode('utf8'))[2:-1]
    hash_path=str(root.findall("hash")[0].text.encode('utf8'))[2:-1]


    file_hash =open(hash_path,"r").readline()


    dependencies= get_commit_dependencies(file_hash)
    
    create_plantuml_file(dependencies)

    print("Генерация изображения графа...")
    if generate_graph_image():
        print("Граф успешно сгенерирован в файле graph.png")



if __name__ == "__main__":
    main()
