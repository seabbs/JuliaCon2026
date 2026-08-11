#!/usr/bin/env julia
# Print the type a composed delay comes back as, for the composable talk.
#
# The slide claims that composing a delay in CensoredDistributions.jl returns
# a plain distribution type, and draws that type as a tree. The tree is this
# script's output, not a sketch. The generic functions are called afterwards
# to show they still work on the composed type.
#
# Run against the registered release the slide cites, not a dev checkout:
#
#     julia --project=/tmp/cdenv -e 'using Pkg; Pkg.add(
#         name = "CensoredDistributions", version = "0.2.22")'
#     julia --project=/tmp/cdenv scripts/composable-composed-type.jl
#
# The last line printed is the version the type came from.

using CensoredDistributions, Distributions

generation_time = Gamma(2.0, 2.0)
incubation = LogNormal(1.6, 0.6)

si = double_interval_censored(
    convolve_distributions(generation_time, incubation);
    upper = 15, interval = 1)

println(typeof(si))
println("cdf(si, 5.0) = ", cdf(si, 5.0))
println("CensoredDistributions v", pkgversion(CensoredDistributions))
