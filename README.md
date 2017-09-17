# CSVv2 training

The training consists of:

1. Exporting variables with BTagAnalyzer.
2. Training decision trees and exporting them into TMVA xml format.
3. Loading trees into new tagger.

## Forest side (export training variables)

This is the part that was probably screwed because some variables used subjet info rather than full jet info.

First, the modified forest is run (run with `crab`)

```sh
cd /data_CMS/cms/lisniak/btgtrain/CMSSW_7_5_8_patch3/src/RecoBTag/PerformanceMeasurements/test
cmsRun runForestAOD_PbPb_MIX_75X.py
```

Then, output files are merged (in the example below merged files are in `datafcr30/JetTree_fcr30.root`).

Then forest trees are converted to flat ones with an entry per jet

```sh
cd /data_CMS/cms/lisniak/btgtrain/CMSSW_7_5_8_patch3/src/RecoBTag/TagVarExtractor/test

cmsRun tagvarextractor_cfg.py outFilename=JetTaggingVariables_fcr30.root inputFiles=../../PerformanceMeasurements/test/datafcr30/JetTree_fcr30.root &
cmsRun tagvarextractor_cfg.py outFilename=JetTaggingVariables_qcd30.root inputFiles=../../PerformanceMeasurements/test/dataqcd30/JetTree_qcd30.root &
```

etc. (for every pt,hat-sample pair).

Copy `JetTaggingVariables_XYZ**.root` to local folder.

## Training

Combine data from .root files into two big DataFrames. Run in the shell:

```sh
python prepare.py
```

The result is two pickle files `fcr.pkl` and `qcd.pkl` which will be needed for the next step.

Now run the main training. In the shell from the folder containing the file `TrainAndTest.ipynb` run

```
jupyter notebook
```

This will open the browser window where you can select `TrainAndTest` file.

In the menu select `Cell->Run All`. This should load files, perform training, make some plots and output xml files. If something is wrong, you will see the error message under the cell which failed. To run only one cell press `Ctrl+Enter`. In order to run all cells below the selected one (e.g. you want continue executing all the notebook after fixing the problem), choose `Cell->Run All Below`. 

If everything worked properly, you should have a new `TMVA_weights.xml` file in the current folder - it contains the calibrations for CSVv2 tagger.

### a few tips

- In order to speedup the training, in the line 

```python
d,fcrtrainall,qcdtrainall,fcrtestall,qcdtestall = getdataset(0.5)
```

change splitting fraction from 0.5 to a small value, like 0.01. This will put only 1% of data into training set and the rest to test set. As a result, the training performance will be worse, but it's useful sometimes for debugging as it is much faster.

- In the plot `Loss` vs `Iteration` make sure training and testing losses are not miles apart (which hints to overfitting)
- All the plots go to `img/` folder (see `save` function in the first cell)
- At the moment, the weights are not saved by `sklearn_to_tmva` module, and as a result the good CSVv2 cut value may differ form the one indicated on `Threshold` vs `Purity` plot. It does not impact the performance though, only the cut value.

## Loading the new tagger

The file generated in the notebook is uploaded to `CMSSWXYZ/src/HeavyIonsAnalysis/JetAnalysis/data/bTagCSVv2PbPb_758p3_Jan2017_BDTG_weights.xml`. Now, add all necessary packages and add these lines to the forest:

```
#replace pp CSVv2 with PbPb CSVv2 (positive and negative taggers unchanged!)
process.load('RecoBTag.CSVscikit.csvscikitTagJetTags_cfi')
process.load('RecoBTag.CSVscikit.csvscikitTaggerProducer_cfi')
process.akPu4PFCombinedSecondaryVertexV2BJetTags = process.pfCSVscikitJetTags.clone()
process.akPu4PFCombinedSecondaryVertexV2BJetTags.tagInfos=cms.VInputTag(cms.InputTag("akPu4PFImpactParameterTagInfos"), cms.InputTag("akPu4PFSecondaryVertexTagInfos"))
process.CSVscikitTags.weightFile=cms.FileInPath('HeavyIonsAnalysis/JetAnalysis/data/bTagCSVv2PbPb_758p3_Jan2017_BDTG_weights.xml')
```

Should work :)
