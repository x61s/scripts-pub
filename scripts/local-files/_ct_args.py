#!/usr/bin/env python3

'''
Add docker build args in Docker compose YAML file.
'''

import yaml
import sys
import shutil
import os.path

filename = ''

try:
    filename = sys.argv[1]
except:
    print("Filename is not set")
    print("Usage: {0} <filename>".format(sys.argv[0]))
    exit()


# To write YAML structure with new lines between nodes
class customDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

def argShow(yamlContent):
    
    node = yamlContent['services']
    
    print('Services:')
    
    for service in node:
        print(service + ':')
        
        try:
            
            for item in node[service]['build']:
                if item == 'args':
                    print('\t' + item + ':')

            for arg in node[service]['build']['args']:
                print('\t' + arg)

        except:
            pass
    
    print('---')


def argAddEverywhere(yamlContent, arg):
    
    node = yamlContent['services']
    
    for service in node:
        if 'build' in node[service]:
            if 'args' not in node[service]['build']:
                node[service]['build']['args'] = []
            if arg not in node[service]['build']['args']:
                print('add', arg, 'to', service, 'service')
                node[service]['build']['args'].append(arg)
            else:
                print('arg', arg, 'already in', service, 'service')


# main scenario
with open(filename, "r") as stream:
    try:
        yamlContent = yaml.safe_load(stream)
        
        argShow(yamlContent)
        
        argAddEverywhere(yamlContent, 'REGISTRY_URL=${REGISTRY_URL}')
        
        if os.path.exists(filename):
            print('{0} exist, renaming...'.format(filename))
            shutil.copy(filename, filename + '.bak')
        
        with open(filename + '.new', 'w') as file:
            document = yaml.dump(yamlContent, file, sort_keys=False, Dumper=customDumper, width=40)
        
    except yaml.YAMLError as exc:
        print(exc)

