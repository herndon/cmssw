# FFTJet pile-up processor module configuration for PFJets.
# This configuration file has a large number of Gausian filters configured.

import math
import FWCore.ParameterSet.Config as cms

from RecoJets.FFTJetProducers.fftjetcommon_cfi import *
import RecoJets.FFTJetProducers.pileup_shape_Summer11_PF_v1_cfi as pf_ps

# A good ratio is about 1.1 for PFJets, could be larger for CaloJets
fftjet_pileup_phi_to_eta_ratio = 1.1

# Note that for the grid below we do not really care that
# convolution results will wrap around in eta
fftjet_pileup_grid_pf = cms.PSet(
    nEtaBins = cms.uint32(pf_ps.fftjet_pileup_eta_bins),
    etaMin = cms.double(-pf_ps.fftjet_pileup_eta_max),
    etaMax = cms.double(pf_ps.fftjet_pileup_eta_max),
    nPhiBins = cms.uint32(pf_ps.fftjet_pileup_phi_bins),
    phiBin0Edge = cms.double(0.0),
    title = cms.untracked.string("FFTJet Pileup Grid")
)

fftjetPileupProcessorPf = cms.EDProducer(
    "FFTJetPileupProcessor",
    #
    # The main eta and phi scale factors for the filters
    kernelEtaScale = cms.double(math.sqrt(1.0/fftjet_pileup_phi_to_eta_ratio)),
    kernelPhiScale = cms.double(math.sqrt(fftjet_pileup_phi_to_eta_ratio)),
    #
    # Label for the produced objects
    outputLabel = cms.string("FFTJetPileupPFStudy"),
    #
    # Label for the input collection of Candidate objects
    src = cms.InputTag("particleFlow"),
    #
    # Label for the jets. Vertex correction may be done for "CaloJet" only.
    jetType = cms.string("PFJet"),
    #
    # Perform vertex correction?
    doPVCorrection = cms.bool(False),
    #
    # Label for the input collection of vertex objects. Meaningful
    # only when "doPVCorrection" is True
    srcPVs = cms.InputTag("offlinePrimaryVertices"),
    #
    # Eta-dependent magnitude factors for the data. These can be used
    # to flatten the expected pileup shape.
    etaDependentMagnutideFactors = cms.vdouble(pf_ps.fftjet_pileup_magnitude_factors),
    #
    # Configuration for the energy discretization grid
    GridConfiguration = fftjet_pileup_grid_pf,
    #
    # Convolution range
    convolverMinBin = cms.uint32(pf_ps.fftjet_pileup_min_eta_bin),
    convolverMaxBin = cms.uint32(pf_ps.fftjet_pileup_max_eta_bin),
    #
    # The set of scales used by the filters. The scales will be generated
    # uniformly in the log space. The settings below correspond to 5% 
    # bandwidth increase for each scale.
    nScales = cms.uint32(50),
    minScale = cms.double(0.05),
    maxScale = cms.double(0.546066656464),
    #
    # The number of percentile points to use
    nPercentiles = cms.uint32(50),
    #
    # Files for mixing in external grids
    externalGridFiles = cms.vstring(),
    #
    # Energy cutoff for external grids (removes some crazy grids)
    externalGridMaxEnergy = cms.double(20000.0),
    #
    # Anomalous calo tower definition (comes from JetProducers default)
    anomalous = fftjet_anomalous_tower_default,
    #
    # Some parameters inherited from FFTJetInterface which no longer
    # play any role
    insertCompleteEvent = cms.bool(fftjet_insert_complete_event),
    completeEventScale = cms.double(fftjet_complete_event_scale),
    #
    # Parameters related to accessing the table of flattening factors from DB
    flatteningTableRecord = cms.string("flatteningTableRecord"),
    flatteningTableName = cms.string("flatteningTableName"),
    flatteningTableCategory = cms.string("flatteningTableCategory"),
    loadFlatteningFactorsFromDB = cms.bool(False)
)
