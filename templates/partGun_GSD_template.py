import FWCore.ParameterSet.Config as cms

from reco_prodtools.templates.GSD_fragment import process

process.maxEvents.input = cms.untracked.int32(DUMMYEVTSPERJOB)

# random seeds
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(DUMMYSEED)
process.RandomNumberGeneratorService.VtxSmeared.initialSeed = cms.untracked.uint32(DUMMYSEED)
process.RandomNumberGeneratorService.mix.initialSeed = cms.untracked.uint32(DUMMYSEED)
process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = cms.untracked.uint32(DUMMYSEED)

# Input source
process.source.firstLuminosityBlock = cms.untracked.uint32(DUMMYSEED)

# Output definition
process.FEVTDEBUGHLToutput.fileName = cms.untracked.string('file:DUMMYFILENAME')

#DUMMYPUSECTION

gunmode = 'GUNMODE'

if gunmode == 'default':
    process.generator = cms.EDProducer("GUNPRODUCERTYPE",
        AddAntiParticle = cms.bool(True),
        PGunParameters = cms.PSet(
            MaxEta = cms.double(DUMMYETAMAX),
            MaxPhi = cms.double(3.14159265359),
            MAXTHRESHSTRING = cms.double(DUMMYTHRESHMAX),
            MinEta = cms.double(DUMMYETAMIN),
            MinPhi = cms.double(-3.14159265359),
            MINTHRESHSTRING = cms.double(DUMMYTHRESHMIN),
            #DUMMYINCONESECTION
            PartID = cms.vint32(DUMMYIDs)
        ),
        Verbosity = cms.untracked.int32(0),
        firstRun = cms.untracked.uint32(1),
        psethack = cms.string('multiple particles predefined pT/E eta 1p479 to 3')
    )
elif gunmode == 'pythia8':
    process.generator = cms.EDFilter("GUNPRODUCERTYPE",
        maxEventsToPrint = cms.untracked.int32(1),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        pythiaHepMCVerbosity = cms.untracked.bool(True),
        PGunParameters = cms.PSet(
          ParticleID = cms.vint32(DUMMYIDs),
          AddAntiParticle = cms.bool(True),
          MinPhi = cms.double(-3.14159265359),
          MaxPhi = cms.double(3.14159265359),
          MINTHRESHSTRING = cms.double(DUMMYTHRESHMIN),
          MAXTHRESHSTRING = cms.double(DUMMYTHRESHMAX),
          MinEta = cms.double(DUMMYETAMIN),
          MaxEta = cms.double(DUMMYETAMAX)
          ),
        PythiaParameters = cms.PSet(parameterSets = cms.vstring())
    )
elif gunmode == 'closeby':
    process.generator = cms.EDProducer("GUNPRODUCERTYPE",
        AddAntiParticle = cms.bool(False),
        PGunParameters = cms.PSet(
            PartID = cms.vint32(DUMMYIDs),
            EnMin = cms.double(DUMMYTHRESHMIN),
            EnMax = cms.double(DUMMYTHRESHMAX),
            RMin = cms.double(DUMMYRMIN),
            RMax = cms.double(DUMMYRMAX),
            ZMin = cms.double(DUMMYZMIN),
            ZMax = cms.double(DUMMYZMAX),
            Delta = cms.double(DUMMYDELTA),
            Pointing = cms.bool(DUMMYPOINTING),
            Overlapping = cms.bool(DUMMYOVERLAPPING),
            RandomShoot = cms.bool(DUMMYRANDOMSHOOT),
            NParticles = cms.int32(DUMMYNRANDOMPARTICLES),
            MaxEta = cms.double(DUMMYETAMAX),
            MinEta = cms.double(DUMMYETAMIN),
            MaxPhi = cms.double(3.14159265359),
            MinPhi = cms.double(-3.14159265359)
        ),
        Verbosity = cms.untracked.int32(10),
        psethack = cms.string('single or multiple particles predefined E moving vertex'),
        firstRun = cms.untracked.uint32(1)
    )
elif gunmode == 'physproc':

    # GUNPRODUCERTYPE is a string in the form of proc[:jetColl:threshold:min_jets]
    physicsProcess = 'GUNPRODUCERTYPE'
    proc_cfg = physicsProcess.split(':')
    proc = proc_cfg[0]

    # phase space cuts
    ptMin = DUMMYTHRESHMIN
    ptMax = DUMMYTHRESHMAX

    from reco_prodtools.templates.hgcBiasedGenProcesses_cfi import *

    #define the process
    print 'Setting process to', proc
    defineProcessGenerator(process, proc=proc, ptMin=ptMin, ptMax=ptMax)

    #set a filter path if it's available
    if len(proc_cfg)==4:
        jetColl = proc_cfg[1]
        thr = float(proc_cfg[2])
        minObj = int(proc_cfg[3])
        print 'Adding a filter with the following settings:'
        print '\tgen-jet collection for filtering:', jetColl
        print '\tpT threshold [GeV]:', thr
        print '\tmin. number of jets with the above threshold:', minObj
        filterPath = defineJetBasedBias(process, jetColl=jetColl, thr=thr, minObj=minObj)
        process.schedule.extend([filterPath])
        process.FEVTDEBUGHLToutput.SelectEvents.SelectEvents=cms.vstring(filterPath.label())


elif gunmode == 'gridpack':
    
    process.generator = cms.EDFilter("Pythia8HadronizerFilter",
        PythiaParameters = cms.PSet(
            parameterSets = cms.vstring(
                'pythia8CommonSettings',
                'pythia8CUEP8M1Settings'
            ),
            pythia8CUEP8M1Settings = cms.vstring(
                'Tune:pp 14',
                'Tune:ee 7',
                'MultipartonInteractions:pT0Ref=2.4024',
                'MultipartonInteractions:ecmPow=0.25208',
                'MultipartonInteractions:expPow=1.6'
            ),
            pythia8CommonSettings = cms.vstring(
                'Tune:preferLHAPDF = 2',
                'Main:timesAllowErrors = 10000',
                'Check:epTolErr = 0.01',
                'Beams:setProductionScalesFromLHEF = off',
                'SLHA:keepSM = on',
                'SLHA:minMassSM = 1000.',
                'ParticleDecays:limitTau0 = on',
                'ParticleDecays:tau0Max = 10',
                'ParticleDecays:allowPhotonRadiation = on'
            )
        ),
        comEnergy = cms.double(14000.0),
        filterEfficiency = cms.untracked.double(1.0),
        maxEventsToPrint = cms.untracked.int32(1),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        pythiaPylistVerbosity = cms.untracked.int32(1)
    )


    process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring(DUMMYGP),
    nEvents = cms.untracked.uint32(DUMMYEVTSPERJOB),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
    )

    process.lhe_step = cms.Path(process.externalLHEProducer)

    # Path and EndPath definitions
    process.lhe_step = cms.Path(process.externalLHEProducer)
    process.generation_step = cms.Path(process.pgen)
    process.simulation_step = cms.Path(process.psim)
    process.digitisation_step = cms.Path(process.pdigi_valid)
    process.L1simulation_step = cms.Path(process.SimL1Emulator)
    process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
    process.digi2raw_step = cms.Path(process.DigiToRaw)
    process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
    process.endjob_step = cms.EndPath(process.endOfProcess)
    process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

    # Schedule definition
    process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.L1TrackTrigger_step,process.digi2raw_step)
    process.schedule.extend(process.HLTSchedule)
    process.schedule.extend([process.endjob_step,process.FEVTDEBUGHLToutput_step])
    from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
    associatePatAlgosToolsTask(process)
    # filter all path with the production filter sequence
    for path in process.paths:
	    if path in ['lhe_step']: continue
	    getattr(process,path).insert(0, process.ProductionFilterSequence)
