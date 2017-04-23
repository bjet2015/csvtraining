import root_numpy as rootnp
import pandas as pd

variables=[
  'centralityBin','Jet_pt','Jet_eta', 'Jet_flavour','Jet_CSV','Jet_CSVV2','Jet_genpt',# not gonna use in training, no worries
  'TagVarCSV_jetNTracks', 'TagVarCSV_trackSip3dSig_0', 'TagVarCSV_trackSip3dSig_1', 'TagVarCSV_trackSip3dSig_2', 'TagVarCSV_trackSip3dSig_3', 
  'TagVarCSV_trackSip3dSigAboveCharm', 'TagVarCSV_trackPtRel_0', 'TagVarCSV_trackPtRel_1', 'TagVarCSV_trackPtRel_2', 'TagVarCSV_trackPtRel_3', 
  'TagVarCSV_trackEtaRel_0', 'TagVarCSV_trackEtaRel_1', 'TagVarCSV_trackEtaRel_2', 'TagVarCSV_trackEtaRel_3', 'TagVarCSV_trackDeltaR_0', 
  'TagVarCSV_trackDeltaR_1', 'TagVarCSV_trackDeltaR_2', 'TagVarCSV_trackDeltaR_3', 'TagVarCSV_trackPtRatio_0', 'TagVarCSV_trackPtRatio_1', 
  'TagVarCSV_trackPtRatio_2', 'TagVarCSV_trackPtRatio_3', 'TagVarCSV_trackJetDist_0', 'TagVarCSV_trackJetDist_1', 'TagVarCSV_trackJetDist_2', 
  'TagVarCSV_trackJetDist_3', 'TagVarCSV_trackDecayLenVal_0', 'TagVarCSV_trackDecayLenVal_1', 'TagVarCSV_trackDecayLenVal_2', 
  'TagVarCSV_trackDecayLenVal_3', 'TagVarCSV_trackSumJetEtRatio', 'TagVarCSV_trackSumJetDeltaR', 'TagVarCSV_vertexMass', 'TagVarCSV_vertexNTracks', 
  'TagVarCSV_vertexEnergyRatio', 'TagVarCSV_vertexJetDeltaR', 'TagVarCSV_flightDistance2dSig', 'TagVarCSV_jetNSecondaryVertices',
]

def limitpt(d, pTmin, pTmax):
    return d[(d.Jet_genpt>8) & (d.Jet_pt>=pTmin) & (d.Jet_pt<pTmax)]

print('Loading...')

print('qcd30...')
qcd30 =pd.DataFrame(rootnp.root2array('JetTaggingVariables_qcd30.root','tagVars/ttree',variables))
print('fcr30...')
fcr30 =pd.DataFrame(rootnp.root2array('JetTaggingVariables_fcr30.root','tagVars/ttree',variables))
print('qcd50...')
qcd50 =pd.DataFrame(rootnp.root2array('JetTaggingVariables_qcd50.root','tagVars/ttree',variables))
print('fcr50...')
fcr50 =pd.DataFrame(rootnp.root2array('JetTaggingVariables_fcr50.root','tagVars/ttree',variables))
print('qcd80...')
qcd80 =pd.DataFrame(rootnp.root2array('JetTaggingVariables_qcd80.root','tagVars/ttree',variables))
print('fcr80...')
fcr80 =pd.DataFrame(rootnp.root2array('JetTaggingVariables_fcr80.root','tagVars/ttree',variables))
print('qcd120...')
qcd120=pd.DataFrame(rootnp.root2array('JetTaggingVariables_qcd120.root','tagVars/ttree',variables))
print('fcr120...')  
fcr120=pd.DataFrame(rootnp.root2array('JetTaggingVariables_fcr120.root','tagVars/ttree',variables))
print('qcd170...')
qcd170=pd.DataFrame(rootnp.root2array('JetTaggingVariables_qcd170.root','tagVars/ttree',variables))
print('fcr170...')
fcr170=pd.DataFrame(rootnp.root2array('JetTaggingVariables_fcr170.root','tagVars/ttree',variables))

print('Limit pT in pThat...')
qcd30= limitpt(qcd30,30,50)
fcr30= limitpt(fcr30,30,50)
qcd50= limitpt(qcd50,50,80)
fcr50= limitpt(fcr50,50,80)
qcd80= limitpt(qcd80,80,120)
fcr80= limitpt(fcr80,80,120)
qcd120=limitpt(qcd120,120,170)
fcr120=limitpt(fcr120,120,170)
qcd170=limitpt(qcd170,170,300)
fcr170=limitpt(fcr170,170,300)

print('Putting into the bowl...')
fcr = pd.concat([fcr30, fcr50,fcr80,fcr120,fcr170])
qcd = pd.concat([qcd30, qcd50,qcd80,qcd120,qcd170])

print('Making some new columns')
fcr['flavor']=abs(fcr.Jet_flavour)==5
fcr['flavorC']=abs(fcr.Jet_flavour)==4

qcd['flavor']=abs(qcd.Jet_flavour)==5
qcd['flavorC']=abs(qcd.Jet_flavour)==4


print('Pickling...')
fcr.to_pickle('fcr3a.pkl')
qcd.to_pickle('qcd3a.pkl')







