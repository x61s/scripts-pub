#!/usr/bin/env python3

'''
Add/Remove/Replace CI/CD blocks in gitlab-ci.yml file.
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


def showIncludes(yamlContent):
    
    node = yamlContent['include']
    
    print()
    print("Includes:")
    
    for nodeItem in node:
        print(nodeItem)


def findInclude(yamlContent, includePath):
    
    node = yamlContent['include']
    
    found = False
    
    for nodeItem in node:
        for key, value in nodeItem.items():
            if key == 'file' and value == includePath:
                found = True
    
    return found


# remove from includes
# assumed that we have no duplicate files included
# TODO: all 3 fields, now this works with 'file' only
def removeIncludes(yamlContent, removeList):

    node = yamlContent['include']
    
    newNode = []
    
    print()
    print("Processing includes removal...")
    print(removeList)
    
    includesRemoved = 0
    
    for nodeItem in node:
    
        print(nodeItem)
        
        nodeItemChanged = {}
        found = False
        
        for key, value in nodeItem.items():
            #print("{0} {1}".format(key, value))
            if key == 'file' and value in removeList:
                print('^^^ ITEM FOUND ^^^')
                found = True
                includesRemoved += 1
            else:
                nodeItemChanged[key] = value
        
        if found != True:
            newNode.append(nodeItemChanged)
        
        yamlContent['include'] = newNode
        
    print("Processing complete. Removed: {0}".format(includesRemoved))
    
    return yamlContent


# this function can add one dict and once to the include block
def addInclude(yamlContent, newNode):
    
    print()
    print("Include appending...")
    
    if newNode not in yamlContent['include']:
        yamlContent['include'].append(newNode)
        print("Include {0} added.".format(newNode))
    else:
        print("Include {0} already exist, skipping...".format(newNode))
    
    return yamlContent


def showStages(yamlContent):
    
    node = yamlContent['stages']
    
    print()
    print("Stages:")
    
    for nodeItem in node:
        print(" - " + nodeItem)
    

def addStage(yamlContent, newStage, prevStage = None):
    
    node = yamlContent['stages']
    
    if prevStage == None:
        node.insert(0, newStage)
    else:
        for n in range(len(node)):
            if node[n] == prevStage:
                node.insert(n + 1, newStage)
                break
    
    yamlContent['stages'] = node

    print("Stages added.")
    
    return yamlContent


def removeStages(yamlContent, stages):
    
    node = yamlContent['stages']
    
    newNode = []
    
    print()
    print("Processing stages...")
    
    for nodeItem in node:
    
        print(" - " + nodeItem)
        
        if nodeItem not in stages:
            newNode.append(nodeItem)
        
    yamlContent['stages'] = newNode
        
    print("Stages removed.")
    
    return yamlContent


def showJobs(yamlContent):
    
    print()
    print("Processing jobs...")
    
    for item in yamlContent:
        if item != "include" and item != "stages":
            print("  " + item)
    
    print()
    

def showJob(yamlContent, jobName):
    
    job = yamlContent[jobName]
    
    print()
    
    for item in job.items():
        print(item)
    
    print()


def removeJob(yamlContent, jobName):
    
    print()
    print("Removing job {0}...".format(jobName))
    
    yamlContent.pop(jobName)
    
    return yamlContent


def createJob(yamlContent, jobName,
              extends = None,
              stage = None,
              variables = None,
              beforeScript = None,
              script = None,
              afterScript = None,
              rules = None,
              tags = None):
    
    job = {}
    
    if stage != None:
        job['stage'] = stage
    
    if variables != None:
        job['variables'] = variables
    
    if extends != None:
        job['extends'] = extends

    if beforeScript != None:
        job['before_script'] = beforeScript
    
    if script != None:
        job['script'] = script
    
    if afterScript != None:
        job['afterScript'] = afterScript
    
    if rules != None:
        job['rules'] = rules
    
    if tags != None:
        job['tags'] = tags
    
    yamlContent[jobName] = job
    
    print()
    
    return yamlContent

# remove from jobs


# main scenario
with open(filename, "r") as stream:
    try:
        yamlContent = yaml.safe_load(stream)
        
        # Prep stage - check out migrator includes/jobs
        migratorFound = findInclude(yamlContent, '/repo/master/build-migrator.yml')
        
        print()
        
        if migratorFound:
            print('Migrator include found')
        else:
            print('Migrator include not found')
        
        # Remove include blocks which contain this files
        removeIncludeList = [
            '/repo/master/build-app.yml',
            ]
        
        if migratorFound:
            removeIncludeList.append('/repo/master/build-migrator.yml')
        
        yamlContent = removeIncludes(yamlContent, removeIncludeList)
        
        # Add new 0.1 version build template in the include block
        addIncludeDict = {
            'project': 'project/dir/cicd',
            'ref': 'master',
            'file': '/repo/master/0.1/build.yml',
            }
        
        yamlContent = addInclude(yamlContent, addIncludeDict)
        
        # EXAMPLES:
        
        # showIncludes(yamlContent)
        # showStages(yamlContent)
        # showJobs(yamlContent)
        # showJob(yamlContent, 'build_app_master')
        # showJob(yamlContent, 'deploy_master_test')
        
        # Add new stage example
        
        # yamlContent = addStage(yamlContent, 'NEW STAGE', 'comptest')
        
        # Remove stages example
        # removeStageList = [
            # 'lint',
            # 'test',
            # ]
        # yamlContent = removeStages(yamlContent, removeStageList)
        
        
        # Remove old template implemented jobs 
        
        try:
            removeJob(yamlContent, 'build_app_master')
        except:
            pass
        
        if migratorFound:
            try:
                removeJob(yamlContent, 'build_migrator_master')
            except:
                pass
        
        
        # New build app job preparation
        
        jobName = 'build_app_master'
        jobExtends = '.podman_build_script'
        jobStage = 'build_master'
        jobVariables = {
            'name': 'app',
            'containerfile': './deploy/build/App.Dockerfile',
            }
        jobBeforeScript = None
        #jobScript = [
            #'echo "Hello!"',
            #'uname -a',
            #]
        jobScript = None
        jobAfterScript = None
        jobRules = None
        jobTags = [
            's5604.j-shell',
            ]
        
        createJob(yamlContent,
                  jobName,
                  jobExtends,
                  jobStage,
                  jobVariables,
                  jobBeforeScript,
                  jobScript,
                  jobAfterScript,
                  jobRules,
                  jobTags)
        
        
        if migratorFound:
            # New build migrator job preparation
            jobName = 'build_migrator_master'
            jobExtends = '.podman_build_script'
            jobStage = 'build_master'
            jobVariables = {
                'name': 'migrator',
                'containerfile': './deploy/build/Migrator.Dockerfile',
                }
            jobBeforeScript = None
            jobScript = None
            jobAfterScript = None
            jobRules = None
            jobTags = [
                's5604.j-shell',
                ]
            
            createJob(yamlContent,
                    jobName,
                    jobExtends,
                    jobStage,
                    jobVariables,
                    jobBeforeScript,
                    jobScript,
                    jobAfterScript,
                    jobRules,
                    jobTags)
        
        
        # NOTE: Dockerfile and Migrator cannot be deleted because it can be found in CT and elsewhere
        
        df = './deploy/build/App.Dockerfile'
        if not os.path.exists(df):
            print('{0} does not exist, creating from "Dockerfile"...'.format(df))
            shutil.copyfile('./deploy/build/Dockerfile', df)
        
        if migratorFound:
            df = './deploy/build/Migrator.Dockerfile'
            if not os.path.exists(df):
                print('{0} does not exist, creating from "Migrator" file...'.format(df))
                shutil.copyfile('./deploy/build/Migrator', df)
        
        showJobs(yamlContent)
        
        # NOTE: renaming .gitlab-ci.yml if exist
        
        if os.path.exists(filename):
            print('{0} exist, renaming...'.format(filename))
            shutil.move(filename, filename + '.bak')
        
        newFilename = filename + ".new"
        
        with open(newFilename, 'w') as file:
            document = yaml.dump(yamlContent, file, sort_keys=False, Dumper=customDumper, width=40)
        
    except yaml.YAMLError as exc:
        print(exc)
