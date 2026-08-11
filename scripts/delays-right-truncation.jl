#!/usr/bin/env julia
# Compute the right truncation bias shown in the delays talk.
#
# Every number comes from CensoredDistributions.jl, not from a sketch. The
# delay is double interval censored (primary window, daily secondary window)
# and then right truncated with Distributions.truncated at a cutoff C, which
# is what double_interval_censored(...; upper = C) composes internally.
#
# Run against the registered release the slide cites, not a dev checkout:
#
#     julia --project=/tmp/cdenv -e 'using Pkg; Pkg.add(
#         name = "CensoredDistributions", version = "0.2.22")'
#     julia --project=/tmp/cdenv scripts/delays-right-truncation.jl
#
# The last line printed is the version the numbers came from.

using CensoredDistributions, Distributions

const OUT = joinpath(@__DIR__, "..", "figures",
    "delays-right-truncation.csv")

delay = LogNormal(1.6, 0.6)
cutoffs = (7, 14)
days = 0:39

full = double_interval_censored(delay; interval = 1)
truncated_at(c) = double_interval_censored(delay; upper = c, interval = 1)

mean_of(d, xs) = sum(xs .* pdf.(d, xs)) / sum(pdf.(d, xs))

rows = String[]
push!(rows, "kind,series,x,y")

for k in days
    push!(rows, "pmf,full,$(k),$(pdf(full, k))")
end

for c in cutoffs
    d = truncated_at(c)
    for k in 0:(c - 1)
        push!(rows, "pmf,cut$(c),$(k),$(pdf(d, k))")
    end
end

for c in 3:40
    push!(rows, "mean,truncated,$(c),$(mean_of(truncated_at(c), 0:(c - 1)))")
end

push!(rows, "mean,full,0,$(mean_of(full, days))")

open(abspath(OUT), "w") do io
    println(io, join(rows, "\n"))
end

println(abspath(OUT))
println("true mean ", mean_of(full, days))
for c in cutoffs
    println("cutoff ", c, " mean ", mean_of(truncated_at(c), 0:(c - 1)))
end
println("CensoredDistributions v", pkgversion(CensoredDistributions))
