# -*- coding: utf-8 -*-

__all__ = ["EventStore"]

from ROOT import gROOT
from ROOT import TFile, TTree


class EventStore( object ):
    
  __container_keys = [
                  "CaloClusterContainer_Clusters"     ,
                  "CaloCellContainer_Cells"           ,
                  "CaloRingsContainer_Rings"          ,
                  "EventInfoContainer_EventInfo"      ,
                  "TruthParticleContainer_Particles"  ,
                  "CaloDetDescriptorContainer_Cells"  ,
  ]

  #
  # Constructor
  #
  def __init__( self, filename, path):
    self.path = path
    self.filename = filename


    self.configure()

  def __del__(self):
    del self.__tree
    del self.__file

  #
  # Configure the event store
  #
  def configure(self):

    try:
        from ROOT import xAOD
    except:
        from lorenzetti_utils.dataframe import dataframe_h
        gROOT.ProcessLine(dataframe_h)

    self.__file = TFile(self.filename)
    self.__tree = self.__file.Get(self.path)



  #
  # Get the container
  #
  def retrieve(self, key):
    return getattr( self.__tree, key ) if key in self.__container_keys else list()


  #
  # Read the current event
  #
  def GetEntry(self, evt):
    return self.__tree.GetEntry(evt)

  #
  # Get the total number of events
  #
  def GetEntries(self):
    return self.__tree.GetEntries()

  #
  # Get all container keys available
  #
  def keys(self):
    return self.__container

