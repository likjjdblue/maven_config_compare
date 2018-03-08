# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import walk
from os.path import isdir,isfile,abspath,join
import os
import re
import codecs

class MavenConfigDiffer:
    def __init__(self,srcpath='source/',targetpath='target/'):
        if not isdir(srcpath):
            raise Exception('文件夹路径不存在:'+str(srcpath))
        if not isdir(targetpath):
            raise Exception('文件夹路径不存在:'+str(targetpath))

        self.BaseSrcDir=srcpath
        self.BaseTargetDir=targetpath

    def differFileContent(self,fileA,fileB):
        #### 检查对应的文件内容是否一致，由于是检查maven配置，所以检查只限于key=value的形式  ###
        print ('即将对比文件：'+str(fileA)+' & '+str(fileB))
        with codecs.open(fileA,'r','utf-8') as f:
            FileContentA=f.read()
        with codecs.open(fileB,'r','utf-8') as f:
            FileContentB=f.read()

        TmpDictA={}
        for item in re.findall(r'^\s*[^#]*?$',FileContentA,flags=re.UNICODE|re.MULTILINE):
            TmpList=item.split('=')
            if len(TmpList)>=2:
                TmpKey,TmpValue=TmpList[0].strip(),''.join(TmpList[1:]).strip()
                TmpDictA.setdefault(TmpKey,TmpValue)

        TmpDictB={}
        for item in re.findall(r'^\s*[^#]*?$',FileContentB,flags=re.UNICODE|re.MULTILINE):
            TmpList=item.split('=')
            if len(TmpList)>=2:
                TmpKey,TmpValue=TmpList[0].strip(),''.join(TmpList[1:]).strip()
                TmpDictB.setdefault(TmpKey,TmpValue)
        TmpDifferA=TmpDictA.viewitems()-TmpDictB.viewitems()
        TmpDifferB=TmpDictB.viewitems()-TmpDictA.viewitems()
        print ('+++ echo 文件内容检查结果：'+fileA+' && '+fileB+' #####')
        for item in TmpDifferA:
            print (fileA+u'内容异常：'+item[0])

        for item in TmpDifferB:
            print (fileB+u'内容异常：'+item[0])
        print ('+++++++++   END    #######')



    def differFolderStructure(self):
        TmpPathSep=os.sep
        self.SrcDirectoriesSet=set()
        self.SrcFilesSet=set()
        self.TargetDirectoriesSet=set()
        self.TargetFilesSet=set()
        self.CommonFilesSet=set()

        #### 提取source文件夹下面的目录结构(文件夹信息，文件信息)  ###
        for TmpBasePath,TmpSubDirectoriesList,TmpFilesList in walk(self.BaseSrcDir):
            for TmpSubDirectory in TmpSubDirectoriesList:
                TmpPath=join(TmpBasePath,TmpSubDirectory)
                TmpPath=TmpPath.replace(TmpPathSep,'/')
                TmpPath=TmpPath.replace(self.BaseSrcDir,'',1)
                self.SrcDirectoriesSet.add(TmpPath)

            for TmpFile in TmpFilesList:
                TmpPath=join(TmpBasePath,TmpFile)
                TmpPath=TmpPath.replace(TmpPathSep,'/')
                TmpPath=TmpPath.replace(self.BaseSrcDir,'',1)
                self.SrcFilesSet.add(TmpPath)

        #### 提取target文件夹下面的目录结构（文件夹信息，文件信息）  ###
        for TmpBasePath,TmpSubDirectoriesList,TmpFilesList in walk(self.BaseTargetDir):
            for TmpSubDirectory in TmpSubDirectoriesList:
                TmpPath=join(TmpBasePath,TmpSubDirectory)
                TmpPath=TmpPath.replace(TmpPathSep,'/')
                TmpPath=TmpPath.replace(self.BaseTargetDir,'',1)
                self.TargetDirectoriesSet.add(TmpPath)

            for TmpFile in TmpFilesList:
                TmpPath=join(TmpBasePath,TmpFile)
                TmpPath=TmpPath.replace(TmpPathSep,'/')
                TmpPath=TmpPath.replace(self.BaseTargetDir,'',1)
                self.TargetFilesSet.add(TmpPath)

        TmpSetA=self.SrcDirectoriesSet-self.TargetDirectoriesSet
        TmpSetB=self.TargetDirectoriesSet-self.SrcDirectoriesSet
        print ('++++++ 检查目录结构   ++++++')
        for item in TmpSetA:
            print ('文件夹异常:'+join(self.BaseSrcDir,item))
        for item in TmpSetB:
            print ('文件夹异常:'+join(self.BaseTargetDir,item))
        print ('+++++++ 目录结构检查完毕++++++\n')

        TmpSetA=self.SrcFilesSet-self.TargetFilesSet
        TmpSetB=self.TargetFilesSet-self.SrcFilesSet
        print ('++++ 检查文件路径结构 ###')
        for item in TmpSetA:
            print ('文件异常：'+join(self.BaseSrcDir,item))
        for item in TmpSetB:
            print ('文件异常:'+join(self.BaseTargetDir,item))
        print ('+++++ 文件路径结构检查完毕.+++++\n')

        ###   对具有相同路径的文件的内容进行检查 ####
        self.CommonFilesSet=self.SrcFilesSet & self.TargetFilesSet
        for subfile in self.CommonFilesSet:
            self.differFileContent(join(self.BaseSrcDir,subfile),join(self.BaseTargetDir,subfile))
            print ('\n')




tmpObj=MavenConfigDiffer()
tmpObj.differFolderStructure()


