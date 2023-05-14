# BDTMuonEnergyTrain_Test Tool script
# ------------------
import sys
import numpy as np
import pandas as pd
import tempfile
import random
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from array import array
from sklearn import datasets
from sklearn import metrics
from sklearn import model_selection
from sklearn import preprocessing
import sklearn
from sklearn.utils import shuffle
from sklearn import linear_model, ensemble
from sklearn.metrics import mean_squared_error
import pickle
from Tool import *

class BDTMuonEnergyTrain_Test(Tool):
    
    # declare member variables here
    E_threshold=ctypes.c_double()
    inputdatafilename=std.string("")
    weightsfilename=std.string("")
    inputBoostStorepathname = std.string("")
    
    def Initialise(self):
        self.m_log.Log(__file__+" Initialising", self.v_debug, self.m_verbosity)
        self.m_variables.Print()
        self.m_variables.Get("BDT_NuE_threshold", self.E_threshold)
        self.m_variables.Get("BDTMuonEnergyTrainingInputDataFile", self.inputdatafilename)
        self.m_variables.Get("BDTMuonEnergyWeightsFile", self.weightsfilename)
        self.m_variables.Get("BDTMuonEnergyTrainingInputBoostStoreFile", self.inputBoostStorepathname)
        return 1
    
    def Execute(self):
        self.m_log.Log(__file__+" Executing", self.v_debug, self.m_verbosity)
        # Set random seed to improve reproducibility                                                                                                                                                                   
        seed = 170
        np.random.seed(seed)

        E_low=0
        E_high=1000*self.E_threshold #convert to MeV                                                                                                                                                               
        div=100
        bins = int((E_high-E_low)/div)
        print('bins: ', bins)

        EnergyRecoBoostStore=cppyy.gbl.BoostStore(True, 2)#define the energy boost store class object to load the variables for the BDT training
        ok=EnergyRecoBoostStore.Initialise(self.inputBoostStorepathname)#read from disk
        print("Initiliased boost store successfully",ok)
        total_entries = ctypes.c_ulong(0)
        get_ok = EnergyRecoBoostStore.Header.Get("TotalEntries",total_entries)
        print("Get num of entries of Energy Reco Store: ",get_ok,", entries: ",total_entries.value)
        #i=0
        ievt=ctypes.c_ulong()
        ievt.value=0
        while True:
            get_ok=EnergyRecoBoostStore.GetEntry(ievt.value)
            print("There is an entry in the BoostStore",get_ok)
            if(not get_ok):
                break;
            #When there is no other entry GetEntry() returns false so the while loop stops
            #Retrieve the required variables from this entry
            EnergyRecoBoostStore.Print(False)
            ok = EnergyRecoBoostStore.Has("num_pmt_hits")
            num_pmt_hits=ctypes.c_int()
            num_pmt_hits.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry num_pmt_hits: ",ok)
             print("type of num_pmt_hits entry is :",EnergyRecoBoostStore.Type("num_pmt_hits"))
             print("Getting num_pmt_hits from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("num_pmt_hits",num_pmt_hits)
            print("Number of pmt hits is: ", num_pmt_hits.value)
            ok = EnergyRecoBoostStore.Has("num_lappd_hits")
            num_lappd_hits=ctypes.c_int()
            num_lappd_hits.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry num_lappd_hits: ",ok)
             print("type of num_lappd_hits entry is :",EnergyRecoBoostStore.Type("num_lappd_hits"))
             print("Getting num_lappd_hits from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("num_lappd_hits",num_lappd_hits)
            print("Number of lappd hits is: ", num_lappd_hits.value)
            ok = EnergyRecoBoostStore.Has("recoTrackLengthInMrd")
            recoTrackLengthInMrd=ctypes.c_double()
            recoTrackLengthInMrd.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry recoTrackLengthInMrd: ",ok)
             print("type of recoTrackLengthInMrd entry is :",EnergyRecoBoostStore.Type("recoTrackLengthInMrd"))
             print("Getting recoTrackLengthInMrd from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("recoTrackLengthInMrd",recoTrackLengthInMrd)
            print("The reconstructed track length in the MRD is: ", recoTrackLengthInMrd.value)
            ok = EnergyRecoBoostStore.Has("diffDirAbs2")
            diffDirAbs=ctypes.c_float()
            diffDirAbs.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry diffDirAbs: ",ok)
             print("type of diffDirAbs entry is :",EnergyRecoBoostStore.Type("diffDirAbs2"))
             print("Getting diffDirAbs from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("diffDirAbs2",diffDirAbs)
            print("DiffDirAbs is: ", diffDirAbs.value)
            ok = EnergyRecoBoostStore.Has("recoDWallR2")
            recoDWallR=ctypes.c_double()
            recoDWallR.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry recoDWallR: ",ok)
             print("type of recoDWallR entry is :",EnergyRecoBoostStore.Type("recoDWallR2"))
             print("Getting recoDWallR from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("recoDWallR2",recoDWallR)
            print("RecoDWallR is: ", recoDWallR.value)
            ok = EnergyRecoBoostStore.Has("recoDWallZ2")
            recoDWallZ=ctypes.c_double()
            recoDWallZ.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry recoDWallZ: ",ok)
             print("type of recoDWallZ entry is :",EnergyRecoBoostStore.Type("recoDWallZ2"))
             print("Getting recoDWallZ from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("recoDWallZ2",recoDWallZ)
            print("RecoDWallZ is: ", recoDWallZ.value)
            ok = EnergyRecoBoostStore.Has("vtxVec")
            vtx_vector=std.vector['double'](range(3))
            if(ok):
             print("EnergyRecoBoostStore has entry vtxVec: ",ok)
             print("type of vtxVec entry is :", EnergyRecoBoostStore.Type("vtxVec"))
             print("Getting vtxVec from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("vtxVec", vtx_vector)
            vtxX=vtx_vector.at(0)
            print("VtxX is: ", vtxX)
            vtxY=vtx_vector.at(1)
            print("VtxY is: ", vtxY)
            vtxZ=vtx_vector.at(2)
            print("VtxZ is: ", vtxZ)
            ok = EnergyRecoBoostStore.Has("trueE")
            trueE=ctypes.c_double()
            trueE.value=0
            if(ok):
             print("EnergyRecoBoostStore has entry trueE: ",ok)
             print("type of trueE entry is :",EnergyRecoBoostStore.Type("trueE"))
             print("Getting trueE from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("trueE",trueE)
            print("The MC muon energy is: ", trueE.value)
            #Create features and labels and preprocess data for the model
            features_list=[]
            features_list.append(recoTrackLengthInMrd.value/200.)
            features_list.append(diffDirAbs.value)
            features_list.append(recoDWallR.value)
            features_list.append(recoDWallZ.value)
            features_list.append(num_pmt_hits.value/200.)
            features_list.append(num_lappd_hits.value/200.)
            features_list.append(vtxX/150.)
            features_list.append(vtxY/200.)
            features_list.append(vtxZ/150.)
            #make the features and labels numpy array for this entry
            featuresforthisentry=np.array(features_list)
            labelsforthisentry=np.array([trueE.value])
        #Append each entry
            if(ievt.value==0):
                features=featuresforthisentry
                labels=labelsforthisentry
            else:
                features=np.c_[features,featuresforthisentry]
                labels=np.c_[labels,labelsforthisentry]
            ievt.value+=1
        features=features.reshape(features.shape[1],features.shape[0])#reshape for model
        labels=labels.reshape(labels.shape[1],labels.shape[0])
        print(features)
        print(features.shape)
        print(labels)
        print(labels.shape)

        np.random.shuffle(features)#shuffling the data sample to avoid any bias in the training
        np.random.shuffle(labels)
        print(features)
        print(labels)
        
        num_events, num_pixels = features.shape
        print(num_events, num_pixels)
        np.random.seed(0)
        #select the events for which we have the reconstructed track length from the DNN
        if(len(labels) % 2==0):
            a=int(len(labels)/2)
        else:
            a=int((len(labels)+1)/2)
        features= features[a:]
        labels = labels[a:]

        num_events, num_pixels = features.shape
        print("With DNN Reco Length",num_events, num_pixels)
        
        #Get the DNN reconstructed track length in the water tank from RecoLength boost store
        #Get the RecoLength Boost Store from DataModel
        DNNRecoLengthBoostStore = self.m_data.Stores.at("RecoLength")
        DNNRecoLengthBoostStore.Print(False)
        ok = DNNRecoLengthBoostStore.Has("DNNRecoLength")
            DNNRecoLength_vector=std.vector[float](range(features.shape[0]))
            if(ok):
             print("EnergyRecoBoostStore has entry DNNRecoLength: ",ok)
             print("type of DNNRecoLength entry is :", EnergyRecoBoostStore.Type("DNNRecoLength"))
             print("Getting DNNRecoLength from EnergyRecoBoostStore")
             EnergyRecoBoostStore.Get("DNNRecoLength", DNNRecoLength_vector)
            print("The DNNRecoLength for the first event: ", DNNRecoLength_vector.at(0))
        DNNRecoLength_list=[]
        for i in range(DNNRecoLength_vector.size()):
                 DNNRecoLength_list.append(DNNRecoLength_vector.at(i)/600.)
        DNNRecoLength=np.array(DNNRecoLength_list)
        features=np.c_[features,DNNRecoLength]
        print(features)
        print("Features shape after adding DNNRecoLength",features.shape)
        
        #discard events with no reconstructed mrd tracks                                                                                                                                                                   
        MRDTrackLength=features[:,0]
        i=0
        a=[]
        for y in MRDTrackLength:
            if y<0:
                print("MRDTrackLength:",y,"Event:",i)
                a.append(i)
            i=i+1
        features=features.drop(features.index[a])
        labels=labels.drop(labels.index[a])

        ########### BDTG ############                                                                                                                                                                                      
        n_estimators=500
        params = {'n_estimators':n_estimators, 'max_depth': 50,
          'learning_rate': 0.025, 'loss': 'absolute_error'}

        print("features.shape: ",features.shape)
        #--- select 70% of sample for training and 30% for testing:                                                                                                                                                        
        offset = int(features.shape[0] * 0.7)
        train_X, train_Y = features[:offset], labels[:offset] # train sample                                                                                                            
        test_X, test_Y   = features[offset:], labels[offset:] # test sample                                                                                                             

        print("train shape: ", train_X.shape," label: ", train_Y.shape)
        print("test shape: ", test_X.shape," label: ", test_Y.shape)

        print("training BDTG...")
        net_hi_E = ensemble.GradientBoostingRegressor(**params)
        model = net_hi_E.fit(train_X, train_Y)
        net_hi_E

        # save the model to disk                                                                                                                                                                                           
        filename = str(self.weightsfilename)
        pickle.dump(model, open(filename, 'wb'))

        mse = mean_squared_error(test_Y, net_hi_E.predict(test_X))
        print("MSE: %.4f" % mse)
        print("events at training & test samples: ", len(labels))
        print("events at train sample: ", len(train_Y))
        print("events at test sample: ", len(test_Y))

        test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

        for i, y_pred in enumerate(net_hi_E.staged_predict(test_X)):
             test_score[i] = net_hi_E.loss_(test_Y, y_pred)

        fig,ax=plt.subplots(ncols=1, sharey=True)
        ax.plot(np.arange(params['n_estimators']) + 1, net_hi_E.train_score_, 'b-', label='Training Set Error')
        ax.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-', label='Test Set Error')
        ax.set_ylim(0.,500.)
        ax.set_xlim(0.,n_estimators)
        ax.legend(loc='upper right')
        ax.set_ylabel('Absolute Errors [MeV]')
        ax.set_xlabel('Number of Estimators')
        ax.yaxis.set_label_coords(-0.1, 0.6)
        ax.xaxis.set_label_coords(0.85, -0.08)
        plt.savefig("error_train_test.png")
        return 1
    
    def Finalise(self):
        self.m_log.Log(__file__+" Finalising", self.v_debug, self.m_verbosity)
        return 1

###################
# ↓ Boilerplate ↓ #
###################

thistool = BDTMuonEnergyTrain_Test()

def SetToolChainVars(m_data_in, m_variables_in, m_log_in):
    return thistool.SetToolChainVars(m_data_in, m_variables_in, m_log_in)

def Initialise():
    return thistool.Initialise()

def Execute():
    return thistool.Execute()

def Finalise():
    return thistool.Finalise()
