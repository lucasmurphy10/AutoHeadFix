#! /usr/bin/python3
#-*-coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import os
import inspect
from collections import OrderedDict

# methods for classes and dictionaries


##################################################################################
# methods for base class for getting class names and importing classes

def AHF_class_from_file(fileName):
    """
    Imports a module from a fileName (stripped of the .py) and returns the class

    Assumes the class is named the same as the module. 
    """
    module = __import__(fileName)
    return getattr(module, fileName)


def AHF_file_from_user (nameStr, longName):
    """
    Static method that trawls through current folder looking for python files matching nameStr
    
    Allows user to choose from the list of files found. Files are recognized by names starting
    with 'AHF_' + nameStr' and ending with '.py'
    Raises: FileNotFoundError if no nameStr class files found
    """
    iFile=0
    files = ''
    startStr = 'AHF_' + nameStr + '_'
    #print (os.listdir(os.curdir))
    for f in os.listdir(os.curdir):
        if f.startswith (startStr) and f.endswith ('.py'):
            f= f.rstrip  ('.py')
            #print ('file = ' + str (f))
            try:
                moduleObj=__import__ (f)
                #print ('module=' + str (moduleObj))
                classObj = getattr(moduleObj, moduleObj.__name__)
                #print ('class obj = ' + str (classObj))
                isAbstractClass =inspect.isabstract (classObj)
                if isAbstractClass == False:
                    if iFile > 0:
                        files += ';'
                    files += f
                    iFile += 1
            except Exception as e: # exception will be thrown if imported module imports non-existant modules, for instance
                print (e)
                continue     
    if iFile == 0:
        print ('Could not find any %s files in the current or enclosing directory' % longName)
        raise FileNotFoundError
    else:
        if iFile == 1:
            ClassFile =  files.split('.')[0]
            print ('Class file found: ' + ClassFile)
            ClassFile =  files.split('.')[0]
        else:
            inputStr = '\nEnter a number from 0 to {} to Choose a {} class:\n'.format((iFile -1), longName)
            ii=0
            for file in files.split(';'):
                inputStr += str (ii) + ': ' + file + '\n'
                ii +=1
            inputStr += ':'
            ClassNum = -1
            while ClassNum < 0 or ClassNum > (iFile -1):
                ClassNum =  int(input (inputStr))
            ClassFile =  files.split(';')[ClassNum]
            ClassFile =  ClassFile.split('.')[0]
        return ClassFile


########################################################################################################################
## methods for user editing of a dictionary of settings containing strings, integers, floats, lists, tuples, booleans, and dictionaries of those types
def AHF_show_ordered_dict (anyDict, longName):
    """
    Dumps standard dictionary settings into an ordered dictionary, prints settings to screen in a numbered fashion from the ordered dictionary,
    making it easy to select a setting to change. Returns the ordered dictionary, used by edit_dict function
    """
    print ('*************** Current %s Settings *******************' % longName)
    showDict = OrderedDict()
    itemDict = {}
    nP = 0
    for key in anyDict:
        value = anyDict.get (key)
        showDict.update ({nP:{key: value}})
        nP += 1
    for ii in range (0, nP):
        itemDict.update (showDict [ii])
        kvp = itemDict.popitem()
        print(str (ii) +') ', kvp [0], ' = ', kvp [1])
    return showDict


def AHF_edit_dict (anyDict, longName):
    """
    Edits values in a passed in dict, in a generic way, not having to know ahead of time the name and type of each setting
    Assumption is made that lists/tuples contain only strings, ints, or float types, and that all members of any list/tuple are same type
    """
    while True:
        orderedDict = AHF_show_ordered_dict (anyDict, longName)
        updatDict = {}
        inputStr = input ('Enter number of setting to edit, or -1 to exit:')
        try:
            inputNum = int (inputStr)
        except ValueError as e:
            print ('enter a NUMBER for setting, please: %s\n' % str(e))
            continue
        if inputNum < 0:
            break
        else:
            itemDict = orderedDict.get (inputNum)
            kvp = itemDict.popitem()
            itemKey = kvp [0]
            itemValue = kvp [1]
            if type (itemValue) is str:
                inputStr = input ('Enter a new text value for %s, currently %s:' % (itemKey, str (itemValue)))
                updatDict = {itemKey: inputStr}
            elif type (itemValue) is int:
                inputStr = input ('Enter a new integer value for %s, currently %s:' % (itemKey, str (itemValue)))
                updatDict = {itemKey: int (inputStr)}
            elif type (itemValue) is float:
                inputStr = input ('Enter a new floating point value for %s, currently %s:' % (itemKey, str (itemValue)))
                updatDict = {itemKey: float (inputStr)}
            elif type (itemValue) is tuple or itemValue is list:
                outputList = []
                if type (itemValue [0]) is str:
                    inputStr = input ('Enter a new comma separated list of strings for %s, currently %s:' % (itemKey, str (itemValue)))
                    outputList = list (inputStr.split(','))
                elif type (itemValue [0]) is int:
                    inputStr = input ('Enter a new comma separated list of integer values for %s, currently %s:' % (itemKey, str (itemValue)))
                    for string in inputStr.split(','):
                        outputList.append (int (string))
                elif type (itemValue [0]) is float:
                    inputStr = input ('Enter a new comma separated list of floating point values for %s, currently %s:' % (itemKey, str (itemValue)))
                    for string in inputStr.split(','):
                        outputList.append (float (string))
                if type (itemValue) is tuple:
                    updatDict = {itemKey: tuple (outputList)}
                else:
                    updatDict = {itemKey: outputList}
            elif type (itemValue) is bool:
                inputStr = input ('%s, True for or False?, currently %s:' % (itemKey, str (itemValue)))
                if inputStr [0] == 'T' or inputStr [0] == 't':
                    updatDict = {itemKey: True}
                else:
                    updatDict = {itemKey: False}
            elif type (itemValue) is dict:
                AHF_edit_dict (itemValue, itemKey)
                anyDict[itemKey].update (itemValue)
            anyDict.update (updatDict)
            
