import os


def create_project_directory(directory):
    if not os.path.exists(directory):
        print("Creating Project " + directory)
        os.makedirs(directory)


def create_project_files(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled)


def write_file(file_name, data=""):
    f = open(file_name, "w")
    f.write(data)


def append_to_file(file_name, data):
    with open(file_name, "a") as file:
        file.write(data + "\n")


def delete_file_contents(file_name):
    with open(file_name, "w"):
        pass


def file_to_set(file_name):
    results = set()
    with open(file_name, "rt") as file:
        for line in file:
            results.add(line.replace("\n", ""))
    return results


def set_to_file(file_name, links):
    delete_file_contents(file_name)
    with open(file_name, "w") as f:
        for link in sorted(links):
            f.write(link + "\n")


