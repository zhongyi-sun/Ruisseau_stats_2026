# -*- coding: utf-8 -*-

#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the 
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.

#import shfjGlobals
from brainvisa import shelltools

from brainvisa.processes import *
#from neuroProcesses import *
import soma
from soma import aims
name = 'Create Region Bucket'
userLevel = 2

signature = Signature(
    'graph', ReadDiskItem( 'Cortical folds graph', 'Graph' ),
    'label_attributes', Choice( 'label', 'name' ),
    'bucket',Choice( 'Sulci', 'Simple Surfaces','Bottoms', 'Junctions with brain hull' ),

 

    'listRegion',Choice( 'all','CS','CSSyl','CSpreCS','PreCS','PreCSinfInter','PreCSsupMargiMed','PreCSinfInterCS',
                         'BrocaCS','BrocaCSExtend','BrocaSFinf','BrocaSFinfSPinf','FrontalSup',
                         'FrontalSupExtend','FrontalLobe','STS','STSant','STSandFCLp','STSandSTI','STSandSTIandFCLp',
                         'STSandSTIpost','STIandSOT','STSandFIPr','STSandSOT','Calc','CalcSOP', 
                         'FIP','FIPGSM','FIPandSTS', 'FIPandSTSandCS','FIPandSTSandFCLp',
                         'Cingulate','FCMantPost', 'CollRhLi','CollRhLiSOT', 'SOT', 'SOTantMedPost','SOTmedPost','RhSOT','CollSOT',
                         'Precuneus', 'FPOCalCu', 'FrontalOrbOrb', 'FrontalOrbOlf','FrontalInf','CollRh','CollRhSOT','CingulateSP',
                         'FCLp','FCLa','FCLpCS','FCLprAntAsc','FCLprAntAscCS','Olf','Orb','OlfOrb'),

    'regionDefinition_directory', ReadDiskItem( 'Directory', 'Directory' ),
    'output_directory', ReadDiskItem( 'Directory', 'Directory' )
)

def initialization( self ):
     self.bucket = 'Sulci'
     self.label_attributes = 'label'
     self.listRegion = 'all'
     self.regionDefinition_directory = os.getcwd()
     self.output_directory = os.getcwd()

def execution( self, context ):
        toRemove = "n"
        wholeRegionList = ['CSSyl','CS','CSpreCS','PreCS','PreCSinfInter','PreCSsupMargiMed','PreCSinfInterCS',
                           'BrocaCS','BrocaCSExtend','BrocaSFinf','BrocaSFinfSPinf','FrontalSup',
                           'FrontalSupExtend','FrontalLobe','STS','STSant','STSandFCLp','STSandSTI','STSandSTIandFCLp',
                           'STSandSTIpost','STIandSOT','STSandFIPr','STSandSOT','Calc','CalcSOP',  
                           'FIP','FIPGSM','FIPandSTS', 'FIPandSTSandCS','FIPandSTSandFCLp',
                           'Cingulate','FCMantPost', 'CollRhLi', 'CollRhLiSOT', 'SOT', 'SOTantMedPost','SOTmedPost','RhSOT','CollSOT',
                           'Precuneus', 'FPOCalCu', 'FrontalOrbOrb', 'FrontalOrbOlf','FrontalInf','CollRh','CollRhSOT','CingulateSP',
                           'FCLp','FCLa','FCLpCS','FCLprAntAsc','FCLprAntAscCS','Olf','Orb','OlfOrb']	
        subjName = self.graph.get('subject')


        ########################  copy transformation files  #########################
        talFolder = os.path.join(self.output_directory.fullPath() , 'tal')
        if (os.path.exists(talFolder)==0):
           os.mkdir(talFolder)
        talFile = ReadDiskItem( 'Transform Raw T1 MRI to Talairach-AC/PC-Anatomist', 'Transformation matrix' ).findValue(self.graph )
        outTalFileName = os.path.join(talFolder, subjName + '_tal.trm')
        cmd = [ 'cp', talFile, outTalFileName ] #copy transformation files
        if not os.path.exists(outTalFileName):
           context.system( *cmd )
	
        listRegion = []
        if (self.listRegion == 'all'):
            listRegion = wholeRegionList
        else:
            listRegion = [self.listRegion]
             
        context.write("The region(s): ",listRegion)  
        for element in listRegion:     

           regionBucketFolder = os.path.join(self.output_directory.fullPath() , element)
           if (os.path.exists(regionBucketFolder)==0):
              os.mkdir(regionBucketFolder)
              leftFolder = os.path.join(regionBucketFolder, 'left')
              rightFolder = os.path.join(regionBucketFolder, 'right')
              os.mkdir(leftFolder)
              os.mkdir(rightFolder)
	
           #call sigGraph2Label to generate images
           cmd = [ 'siGraph2Label', '-g', self.graph.fullPath() ]
           regionTranslationFile = 'trans' + element + '.trl'
           cmd += [ '-tr', os.path.join(self.regionDefinition_directory.fullPath(), regionTranslationFile) ]
           cmd += [ '-a', self.label_attributes ]
           sulcus = context.temporary( 'GIS Image' )
           cmd += [ '-o', sulcus ]
           if self.bucket in ('Sulci'):
              cmd += [ '-b', 'aims_ss', '-b', 'aims_bottom', '-b', 'aims_other' ]
           elif self.bucket in ('Bottoms'):
              cmd += [ '-b', 'aims_bottom' ]
           elif self.bucket in ('Junctions with brain hull'):
              cmd += [ '-b', 'aims_junction', '-s', 'hull_junction' ]
           elif self.bucket in ('Simple Surfaces'):
              cmd += [ '-b', 'aims_ss' ]
           context.system( *cmd )
  
           #call VipConnexFilter to remove central sulcus large non-connected pieces
           if (element == 'CSSyl'):
               context.write(subjName)
#               cmd = [ 'VipConnexFilter', '-i', sulcus, '-o', sulcus, '-m', 'b', '-b', 1 ]
               cmd = [ 'AimsConnectComp', '-i', sulcus, '-o', sulcus, '-b', 'true', '-n', 1 ]
               context.system( *cmd )

           #call AimsFileConvert to convert images to bucket files
           side = self.graph.get('side')
           if (side=='left'):
               letter='L'
           else:
               letter='R'
           sideSubjName = letter + subjName
           bucketPath =  os.path.join(regionBucketFolder, side)
           bucketFile =  os.path.join(bucketPath, sideSubjName)
           minfName = bucketFile + '.bck.minf'
           cmd = [ 'AimsFileConvert', '-i', sulcus, '-o', bucketFile, '-c', 'Bucket', '-t', 'VOID', '-e',  '1']         
           context.system( *cmd )
           
           #remove minf files
           rmMinf = "rm " + minfName
           os.system(rmMinf)

           #flag empty bucket files
           b = soma.aims.read(bucketFile)
           bckLine = b[0].size()
           context.write("The bck line number is: ",bckLine)
           if (bckLine == 0):
               context.write("subjet to be removed: ",subjName)
               toRemove = "y"  
        
        #remove all buckets of all regions generated for this subject
        if (toRemove == "y"):
            for element in listRegion:    
                #WIP  bucketFile as both left and right parts
                regionBucketFolder = os.path.join(self.output_directory.fullPath() , element)
                leftFolder = os.path.join(regionBucketFolder, 'left')
                rightFolder = os.path.join(regionBucketFolder, 'right')
                LsubjName = 'L' + subjName + '.bck'
                RsubjName = 'R' + subjName + '.bck'               
                leftBucketFileName =  os.path.join(leftFolder, LsubjName)
                rightBucketFileName =  os.path.join(leftFolder, RsubjName)

                rmLBck = "rm " + leftBucketFileName
                os.system(rmLBck)
                rmRBck = "rm " + rightBucketFileName
                os.system(rmRBck)
                context.write("subjet ",subjName," is removed in region ",element)


