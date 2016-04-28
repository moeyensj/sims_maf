#!/usr/bin/env python

from __future__ import print_function, division

import os
import argparse
import inspect
import numpy as np
import numpy.ma as ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Needs MafSSO branch from sims_maf.
import lsst.sims.maf.metrics as metrics
import lsst.sims.maf.slicers as slicers
import lsst.sims.maf.stackers as stackers
import lsst.sims.maf.plots as plots
import lsst.sims.maf.db as db
import lsst.sims.maf.metricBundles as mmb

# Assumes you have already created observation file,
# using make_movingObject_obs.py.

nyears = [2, 4, 6, 8, 10]
bins = np.arange(5, 95, 10.)
windows = np.arange(1, 200, 15)

def readObservations(orbitFile, obsFile, Hrange):
    # Read the orbit file and set the H values for the slicer.
    slicer = slicers.MoObjSlicer()
    slicer.readOrbits(orbitFile, Hrange=Hrange)
    slicer.readObs(obsFile)
    return slicer


def setupMetrics(slicer, runName, metadata, albedo, Hmark):
    # Set up the metrics.
    allBundles = {}

    basicPlotDict = {'albedo': albedo, 'Hmark': Hmark}
    summaryMetrics = [metrics.MoCompletenessMetric(),
                      metrics.MoCumulativeCompletenessMetric()]
    plotFuncs = [plots.MetricVsH()]
    # Basic discovery/completeness metric, calculate at several years.
    allBundles['discoveryChances'] = {}
    for nyr in nyears:
        # 3 nights in 15
        constraint = 'night < %d' %(nyr * 365 + 1)
        md = metadata + ' year %d, 3 pairs in 15 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Discovery Chances %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryChancesMetric(nObsPerNight=2, tNight=90./60./24.,
                                                nNightsPerWindow=3, tWindow=15)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    plotDict=plotDict, plotFuncs=plotFuncs,
                                    summaryMetrics=summaryMetrics)
        allBundles['discoveryChances'][md] = bundle
        # 3 nights in 30
        constraint = 'night < %d' %(nyr * 365 + 1)
        md = metadata + ' year %d, 3 pairs in 30 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Discovery Chances %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryChancesMetric(nObsPerNight=2, tNight=90./60./24.,
                                                nNightsPerWindow=3, tWindow=30)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    plotDict=plotDict, plotFuncs=plotFuncs,
                                    summaryMetrics=summaryMetrics)
        allBundles['discoveryChances'][md] = bundle
        # 4 nights in 20
        constraint = 'night < %d' %(nyr * 365 + 1)
        md = metadata + ' year %d, 4 pairs in 20 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Discovery Chances %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryChancesMetric(nObsPerNight=2, tNight=90./60./24.,
                                                nNightsPerWindow=4, tWindow=20)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    plotDict=plotDict, plotFuncs=plotFuncs,
                                    summaryMetrics=summaryMetrics)
        allBundles['discoveryChances'][md] = bundle
        # 3 triplets in 30
        constraint = 'night < %d' %(nyr * 365 + 1)
        md = metadata + ' year %d, 3 triplets in 30 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Discovery Chances %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryChancesMetric(nObsPerNight=3, tNight=120./60./24.,
                                                nNightsPerWindow=3, tWindow=30)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    plotDict=plotDict, plotFuncs=plotFuncs,
                                    summaryMetrics=summaryMetrics)
        allBundles['discoveryChances'][md] = bundle
        # 3 quads in 30
        constraint = 'night < %d' % (nyr * 365 + 1)
        md = metadata + ' year %d, 3 quads in 30 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Discovery Chances %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryChancesMetric(nObsPerNight=4, tNight=150. / 60. / 24.,
                                                nNightsPerWindow=3, tWindow=30)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    plotDict=plotDict, plotFuncs=plotFuncs,
                                    summaryMetrics=summaryMetrics)
        allBundles['discoveryChances'][md] = bundle

    """
    # More complicated discovery metric, with child metrics.
    allBundles['discovery'] = {}
    for nyr in nyears:
        # 3 pairs in 15
        constraint = 'night < %d' %(nyr * 365 + 1)
        md = metadata + ' year %d, 3 pairs in 15 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryMetric(nObsPerNight=2, tMin=0, tMax=90./60./24.,
                                         nNightsPerWindow=3, tWindow=15)
        childMetrics = {'Time': metrics.Discovery_TimeMetric(metric, i=0, tStart=59580),
                        'N_Chances': metrics.Discovery_N_ChancesMetric(metric)}
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    childMetrics=childMetrics,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        bundle.childBundles['N_Chances'].setSummaryMetrics(summaryMetrics)
        allBundles['discovery'][md] = bundle
        # 3 pairs in 30
        constraint = 'night < %d' % (nyr * 365 + 1)
        md = metadata + ' year %d, 3 pairs in 30 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryMetric(nObsPerNight=2, tMin=0, tMax=90. / 60. / 24.,
                                         nNightsPerWindow=3, tWindow=30)
        childMetrics = {'Time': metrics.Discovery_TimeMetric(metric, i=0, tStart=59580),
                        'N_Chances': metrics.Discovery_N_ChancesMetric(metric)}
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    childMetrics=childMetrics,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        bundle.childBundles['N_Chances'].setSummaryMetrics(summaryMetrics)
        allBundles['discovery'][md] = bundle
        # 4 pairs in 20
        constraint = 'night < %d' % (nyr * 365 + 1)
        md = metadata + ' year %d, 4 pairs in 20 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryMetric(nObsPerNight=2, tMin=0, tMax=90. / 60. / 24.,
                                         nNightsPerWindow=4, tWindow=20)
        childMetrics = {'Time': metrics.Discovery_TimeMetric(metric, i=0, tStart=59580),
                        'N_Chances': metrics.Discovery_N_ChancesMetric(metric)}
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    childMetrics=childMetrics,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        bundle.childBundles['N_Chances'].setSummaryMetrics(summaryMetrics)
        allBundles['discovery'][md] = bundle
        # 3 triplets in 30
        constraint = 'night < %d' % (nyr * 365 + 1)
        md = metadata + ' year %d, 4 pairs in 20 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryMetric(nObsPerNight=3, tMin=0, tMax=120. / 60. / 24.,
                                         nNightsPerWindow=3, tWindow=30)
        childMetrics = {'Time': metrics.Discovery_TimeMetric(metric, i=0, tStart=59580),
                        'N_Chances': metrics.Discovery_N_ChancesMetric(metric)}
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    childMetrics=childMetrics,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        bundle.childBundles['N_Chances'].setSummaryMetrics(summaryMetrics)
        allBundles['discovery'][md] = bundle
        # 3 quads in 30
        constraint = 'night < %d' % (nyr * 365 + 1)
        md = metadata + ' year %d, 3 quads in 30 nights' % nyr
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: %s' % (runName, md)}
        plotDict.update(basicPlotDict)
        metric = metrics.DiscoveryMetric(nObsPerNight=4, tMin=0, tMax=150. / 60. / 24.,
                                         nNightsPerWindow=3, tWindow=30)
        childMetrics = {'Time': metrics.Discovery_TimeMetric(metric, i=0, tStart=59580),
                        'N_Chances': metrics.Discovery_N_ChancesMetric(metric)}
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=md,
                                    childMetrics=childMetrics,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        bundle.childBundles['N_Chances'].setSummaryMetrics(summaryMetrics)
        allBundles['discovery'][md] = bundle
    """

    allBundles['nObs'] = {}
    constraint = None
    md = metadata
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Number of observations %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.NObsMetric()
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['nObs'][md] = bundle

    allBundles['obsArc'] = {}
    constraint = None
    md = metadata
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Observational Arc Length %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.ObsArcMetric()
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['obsArc'][md] = bundle

    allBundles['ActivityTime'] = {}
    for w in windows:
        constraint = None
        md = metadata + ' activity lasting %.0f days' % w
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Chances of detecting %s' % (runName, md),
                    'ylabel': 'Probability of detection per %.0f day window' % w}
        metricName = 'Chances of detecting activity lasting %.0f days' % w
        metric = metrics.ActivityOverTimeMetric(w, metricName=metricName)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=metadata,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        allBundles['ActivityTime'][w] = bundle

    allBundles['ActivityPeriod'] = {}
    for b in bins:
        constraint = None
        md = metadata + ' activity lasting %.2f of period' % (b/360.)
        plotDict = {'nxbins': 200, 'nybins': 200,
                    'title': '%s: Chances of detecting %s' % (runName, md),
                    'ylabel': 'Probability of detection per %.2f deg window' % b}
        metricName = 'Chances of detecting activity lasting %.2f of the period' % (b/360.)
        metric = metrics.ActivityOverPeriodMetric(b, metricName=metricName)
        bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                    runName=runName, metadata=metadata,
                                    plotDict=plotDict, plotFuncs=plotFuncs)
        allBundles['ActivityPeriod'][b] = bundle

    allBundles['lightcurveInversion'] = {}
    constraint = None
    md = metadata
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Fraction with potential lightcurve inversion %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.LightcurveInversionMetric(snrLimit=20, nObs=100, nDays=5*365)
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['lightcurveInversion'][md] = bundle

    allBundles['colorDetermination'] = {}
    constraint = None
    md = metadata + ' u-g color'
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Fraction with potential u-g color measurement %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.ColorDeterminationMetric(nPairs=1, snrLimit=10, nHours=2.0, bOne='u', bTwo='g')
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['colorDetermination'][md] = bundle

    constraint = None
    md = metadata + ' g-r color'
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Fraction with potential g-r color measurement %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.ColorDeterminationMetric(nPairs=1, snrLimit=10, nHours=2.0, bOne='g', bTwo='r')
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['colorDetermination'][md] = bundle

    constraint = None
    md = metadata + ' r-i color'
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Fraction with potential r-i color measurement %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.ColorDeterminationMetric(nPairs=1, snrLimit=10, nHours=2.0, bOne='r', bTwo='i')
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['colorDetermination'][md] = bundle

    constraint = None
    md = metadata + ' i-z color'
    plotDict = {'nxbins': 200, 'nybins': 200,
                'title': '%s: Fraction with potential i-z color measurement %s' % (runName, md)}
    plotDict.update(basicPlotDict)
    metric = metrics.ColorDeterminationMetric(nPairs=1, snrLimit=10, nHours=2.0, bOne='i', bTwo='z')
    bundle = mmb.MoMetricBundle(metric, slicer, constraint,
                                runName=runName, metadata=md,
                                plotDict=plotDict, plotFuncs=plotFuncs,
                                summaryMetrics=None)
    allBundles['colorDetermination'][md] = bundle

    return allBundles


def runMetrics(allBundles, outDir):
    # Run metrics, write basic output in outDir.
    # Un-nest dictionaries to run all at once.
    bundleDict = {}
    count = 0
    for k, v in allBundles.iteritems():
        if isinstance(v, dict):
            for k2, v2 in v.iteritems():
                bundleDict[count] = v2
                count += 1
        else:
            bundleDict[count] = v
            count += 1
    print("Counted %d top-level metric bundles." % count)

    # Set up resultsDb.
    resultsDb = db.ResultsDb(outDir=outDir)

    bg = mmb.MoMetricBundleGroup(bundleDict, outDir=outDir, resultsDb=resultsDb)
    bg.runAll()
    bg.summaryAll()
    bg.writeAll()
    bg.plotAll()
    return allBundles, resultsDb


def makeCompletenessBundle(bundle, summaryName='CumulativeCompleteness'):
    # Make a 'mock' metric bundle from a bundle which had the MO_Completeness or MO_CumulativeCompleteness
    # summary metrics run. This lets us use a normal plotHandler to generate combined plots.
    completeness = ma.MaskedArray(data=bundle.summaryValues[summaryName]['value'],
                                  mask=np.zeros(len(bundle.summaryValues[summaryName]['value'])),
                                  fill_value=0)
    plotDict = {}
    plotDict.update(bundle.plotDict)
    plotDict['label'] = bundle.metadata
    mb = mmb.MoMetricBundle(metrics.MoCompletenessMetric(metricName=summaryName),
                            bundle.slicer, constraint=None, metadata=bundle.metadata,
                            runName=bundle.runName, plotDict=plotDict)
    mb.metricValues = completeness
    return mb


def plotMoreMetrics(allBundles, outDir, resultsDb, metadata, Hmark):
    # Combine differential completeness summary values, over multiple years for discoveryChances.
    ph = plots.PlotHandler(outDir=outDir, savefig=True, resultsDb=resultsDb,
                           figformat='pdf', dpi=600, thumbnail=True)

    # Plot all of the differential completeness values, for each year, for standard discovery strategy.
    plotbundles = []
    k = 'discoveryChances'
    strategy = '3 pairs in 15 nights'
    mdmatch = ['%s year %d, %s' % (metadata, nyr, strategy) for nyr in nyears]
    for md in mdmatch:
        b = allBundles[k][md]
        plotbundles.append(makeCompletenessBundle(b, summaryName='Completeness'))
    ph.setMetricBundles(plotbundles)
    plotDict = {'title': '%s Differential Completeness - %s' % (b.runName, b.metadata.split(',')[1]),
                'ylabel': 'Completeness @ H', 'yMin': 0, 'yMax': 1,
                'albedo': b.plotDict['albedo'], 'Hmark': b.plotDict['Hmark'],
                'legendloc': 'lower left'}
    ph.plot(plotFunc=plots.MetricVsH(), plotDicts=plotDict)
    plt.close()

    # Plot all of the cumulative completeness values, for each year, for standard discovery strategy.
    plotbundles = []
    k = 'discoveryChances'
    strategy = '3 pairs in 15 nights'
    mdmatch = ['%s year %d, %s' % (metadata, nyr, strategy) for nyr in nyears]
    for md in mdmatch:
        b = allBundles[k][md]
        plotbundles.append(makeCompletenessBundle(b, summaryName='CumulativeCompleteness'))
    ph.setMetricBundles(plotbundles)
    plotDict = {'title': '%s Cumulative Completeness - %s' % (b.runName, b.metadata.split(',')[1]),
                'ylabel': 'Completeness <= H', 'yMin': 0, 'yMax': 1,
                'albedo': b.plotDict['albedo'], 'Hmark': b.plotDict['Hmark'],
                'legendloc': 'lower left'}
    ph.plot(plotFunc=plots.MetricVsH(), plotDicts=plotDict)
    plt.close()

    # Plot the cumulative completeness as a function of years.
    k = 'discoveryChances'
    strategy = '3 pairs in 15 nights'
    completeness_at_year = np.zeros(len(nyears), float)
    b = allBundles[k]['%s year 10, %s' % (metadata, strategy)]
    # Pick a point to 'count' the completeness at.
    if Hmark is not None:
        hIdx = np.abs(b.slicer.Hrange - Hmark).argmin()
    else:
        hIdx = int(len(b.slicer.Hrange) / 3)
    for i, nyr in enumerate(nyears):
        md = '%s year %d, %s' % (metadata, nyr, strategy)
        b = allBundles[k][md]
        completeness_at_year[i] = b.summaryValues['CumulativeCompleteness']['value'][hIdx]
    fig = plt.figure()
    plt.plot(nyears, completeness_at_year, label='%s H<=%.2f' % (metadata, b.slicer.Hrange[hIdx]))
    plt.xlabel('Years into survey')
    plt.ylabel('Completeness @ H <= %.2f' % (b.slicer.Hrange[hIdx]))
    plt.title('Cumulative completeness as a function of time')
    plt.legend(loc=(0.7, 0.1), fancybox=True, fontsize='smaller')
    plotmetadata = 'years %s' % (' '.join(['%d' % nyr for nyr in nyears]))
    filename = '%s_%s_CompletenessOverTime_%.2f' % (b.runName, metadata, b.slicer.Hrange[hIdx])
    ph.saveFig(fig.number, filename, 'Completeness', 'Cumulative completeness as a function of time',
               b.slicer.slicerName, b.runName, b.constraint, plotmetadata)

    # Plot all of the cumulative completeness values, for year 10, for different discovery strategies.
    plotbundles = []
    k = 'discoveryChances'
    for mdmatch in ['%s year 10, 3 pairs in 15 nights' % metadata,
                    '%s year 10, 3 pairs in 30 nights' % metadata,
                    '%s year 10, 4 pairs in 20 nights' % metadata,
                    '%s year 10, 3 triplets in 30 nights' % metadata,
                    '%s year 10, 3 quads in 30 nights' % metadata]:
        b = allBundles[k][mdmatch]
        plotbundles.append(makeCompletenessBundle(b, summaryName='CumulativeCompleteness'))
    ph.setMetricBundles(plotbundles)
    plotDict = {'title': '%s Cumulative Completeness - %s' % (b.runName, b.metadata.split(',')[0]),
                'ylabel': 'Completeness <= H', 'yMin': 0, 'yMax': 1,
                'albedo': b.plotDict['albedo'], 'Hmark': b.plotDict['Hmark'],
                'legendloc': 'lower left'}
    ph.plot(plotFunc=plots.MetricVsH(), plotDicts=plotDict)
    plt.close()

    # Make joint 'chance of detecting activity over time' plots, for the brightest objects.
    meanFraction = np.zeros(len(windows), float)
    minFraction = np.zeros(len(windows), float)
    maxFraction = np.zeros(len(windows), float)
    Hidx = 0
    for i, win in enumerate(windows):
        b = allBundles['ActivityTime'][win]
        meanFraction[i] = np.mean(b.metricValues.swapaxes(0, 1)[Hidx])
        minFraction[i] = np.min(b.metricValues.swapaxes(0, 1)[Hidx])
        maxFraction[i] = np.max(b.metricValues.swapaxes(0, 1)[Hidx])
    fig = plt.figure()
    plt.plot(windows, meanFraction, 'r', label='Mean')
    plt.plot(windows, minFraction, 'b:', label='Min')
    plt.plot(windows, maxFraction, 'g--', label='Max')
    plt.xlabel('Length of activity (days)')
    plt.ylabel('Probability of detecting activity')
    plt.title('Chances of detecting activity (for H=%.1f %s)' % (b.slicer.Hrange[Hidx],
                                                                 metadata))
    plt.grid()
    plotmetadata = 'windows from %.1f to %.1f days' % (windows[0], windows[-1])
    filename = '%s_%s_Activity_%s' % (b.runName, metadata, plotmetadata)
    ph.saveFig(fig.number, filename, 'Activity', 'Chances of detecting Activity lasting X days',
               b.slicer.slicerName, b.runName, b.constraint, plotmetadata)

    # Make a joint 'chance of detecting activity over period' plots, for the brightest objects.
    meanFraction = np.zeros(len(bins), float)
    minFraction = np.zeros(len(bins), float)
    maxFraction = np.zeros(len(bins), float)
    Hidx = 0
    for i, bin in enumerate(bins):
        b = allBundles['ActivityPeriod'][bin]
        meanFraction[i] = np.mean(b.metricValues.swapaxes(0, 1)[Hidx])
        minFraction[i] = np.min(b.metricValues.swapaxes(0, 1)[Hidx])
        maxFraction[i] = np.max(b.metricValues.swapaxes(0, 1)[Hidx])
    fig = plt.figure()
    plt.plot(bins / 360., meanFraction, 'r', label='Mean')
    plt.plot(bins / 360., minFraction, 'b:', label='Min')
    plt.plot(bins / 360., maxFraction, 'g--', label='Max')
    plt.xlabel('Length of activity (fraction of period)')
    plt.ylabel('Probabilty of detecting activity')
    plt.title('Chances of detecting activity (for H=%.1f %s)' % (b.slicer.Hrange[Hidx],
                                                                                  metadata))
    plt.grid()
    plotmetadata = 'bins from %.2f to %.2f' % (bins[0], bins[-1])
    filename = '%s_%s_Activity_%s' % (b.runName, metadata, plotmetadata)
    ph.saveFig(fig.number, filename, 'Activity', 'Chances of detecting Activity lasting X of period',
               b.slicer.slicerName, b.runName, b.constraint, plotmetadata)

    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run moving object metrics for a particular opsim run.")
    parser.add_argument("--orbitFile", type=str, help="File containing the moving object orbits.")
    parser.add_argument("--obsFile", type=str,
                        help="File containing the observations of the moving objects.")
    parser.add_argument("--opsimRun", type=str, default=None,
                        help="Name of opsim run. Will attempt to extract from obsFile if not specified.")
    parser.add_argument("--outDir", type=str, default='.',
                        help="Output directory for moving object metrics. Default '.'")
    parser.add_argument("--hMin", type=float, default=5.0, help="Minimum H value. Default 5.")
    parser.add_argument("--hMax", type=float, default=27.0, help="Maximum H value. Default 27.")
    parser.add_argument("--hStep", type=float, default=0.25, help="Stepsizes in H values.")
    parser.add_argument("--metadata", type=str, default='',
                        help="Base string to add to all metric metadata.")
    parser.add_argument("--albedo", type=float, default=None,
                        help="Albedo value, to add diameters to upper scales on plots. Default None.")
    parser.add_argument("--hMark", type=float, default=None,
                        help="Add vertical lines at H=hMark on plots. Default None.")
    args = parser.parse_args()

    if args.orbitFile is None:
        print('Must specify an orbitFile')
        exit()
    if args.obsFile is None:
        print('Must specify an obsFile')
        exit()
    if args.opsimRun is None:
        if len(args.obsFile.split('__')) == 2:
            args.opsimRun = args.obsFile.split('__')[0]
        else:
            args.opsimRun = '_'.join(args.obsFile.split('_')[0:2])
        print('opsimRun name was not specified, using %s' % (args.opsimRun))

    print('Output directory %s' % (args.outDir))
    if not (os.path.isdir(args.outDir)):
        os.makedirs(args.outDir)

    Hrange = np.arange(args.hMin, args.hMax + args.hStep, args.hStep)
    slicer = readObservations(args.orbitFile, args.obsFile, Hrange)

    allBundles = setupMetrics(slicer, runName=args.opsimRun, metadata=args.metadata,
                              albedo=args.albedo, Hmark=args.hMark)

    allBundles, resultsDb = runMetrics(allBundles, args.outDir)

    plotMoreMetrics(allBundles, args.outDir, resultsDb, args.metadata, args.hMark)
