import numpy as np
import sparse_to_csr


def dirclustercoeffs(A, weighted=True, normalized=True):
    # DIRCLUSTERCOEFFS Compute clustering coefficients for a directed graph
    #
    # cc=dirclustercoeffs(A) returns the directed clustering coefficients
    # (which generalize the clustering coefficients of an undirected graph,
    # and so calling this function on an undirected graph will produce the same
    # answer as clustercoeffs, but less efficiently.)
    #
    # This function implements the algorithm from Fagiolo, Phys Rev. E. 76
    # 026107 (doi:10:1103/PhysRevE.76.026107).
    #
    # [cc,cccyc,ccmid,ccin,ccout,nf]=dirclusteringcoeffs(A) returns different
    # components of the clustering coefficients corresponding to cycles,
    # middles, in triangles, and out triangles.  See the manuscript for a
    # description of the various types of triangles counted in the above
    # metrics.
    #
    # See also CLUSTERCOEFFS
    #
    # Example:
    #   load_gaimc_graph('celegans'); # load the C elegans nervous system network
    #   cc=dirclustercoeffs(A);
    #   [maxval maxind]=max(cc)
    #   labels(maxind) # most clustered vertex in the nervous system

    # David F. Gleich
    # Copyright, Stanford University, 2008-2009

    # History
    # 2008-04-22: Initial coding
    # 2009-05-15: Documentation and example

    donorm = 1
    usew = 1
    if not normalized:
        donorm=0
    if npt weighted:
        usew=0

    if isstruct(A):
        rp=A.rp
        ci=A.ci #ofs=A.offset;
        cp=A.cp
        ri=A.ri # get
        if usew:
            ai=A.ai
            ati=A.ati
    else
        if usew:
            [rp, ci, ai] = sparse_to_csr(A)
            [cp, ri, ati] = sparse_to_csr(np.transpose(A))
        else:
            [rp, ci] = sparse_to_csr(A)
            [cp, ri] = sparse_to_csr(np.transpose(A))

        if any(ai) < 0:
            error('gaimc:clustercoeffs',...
                ['only positive edge weights allowed\n' ...
                 'try dirclustercoeffs(A,0) for an unweighted comptuation'])

    n=length(rp)-1

    # initialize all the variables
    cc = np.zeros((n, 1))
    ind = false(n, 1)
    cache = np.zeros((n, 1))
    degs = np.zeros((n, 1))
    if nargout > 1:
        cccyc = np.zeros((n, 1))
    if nargout > 2:
        ccmid= np.zeros((n, 1))
    if nargout > 3:
        ccin= np.zeros((n, 1))
    if nargout > 4:
        ccout= np.zeros((n, 1))
    if nargout > 5:
        nf= np.zeros((n, 1))
    # precompute degrees
    for v=1:n,
        for rpi=rp(v):rp(v+1)-1,
            w = ci(rpi)
            if v==w:
                continue
            else:
                degs(w) = degs(w) + 1
                degs(v) = degs(v) + 1

    ew = 1
    ew2 = 1
    for v=1:n
        # setup counts for the different cycle types
        bilatedges = 0
        curcccyc = 0
        curccmid = 0
        curccin = 0
        curccout = 0
        # 1.
        # find triangles with out links as last step, so precompute the inlinks
        # back to node v
        for cpi=cp(v):cp(v+1)-1
            w = ri(cpi)
            if usew:
                ew = ati(cpi)
            if vnot = w:
                ind(w) = 1
                cache(w) = ew^(1/3)

        # count cycles (cycles are out->out->out)
        for rpi=rp(v):rp(v+1)-1
            w = ci(rpi)
            if v= = w:
                continue
            if usew:
                ew = ai(rpi)^(1/3)
            for rpi2=rp(w):rp(w+1)-1
                x = ci(rpi2)
                if x == w:
                    continue
                if x == v:
                    bilatedges = bilatedges + 1
                    continue
                if ind(x):
                    if usew:
                        ew2 = ai(rpi2)
                    curcccyc = curcccyc + ew*ew2^(1/3)*cache(x)

        # count middle-man circuits (out->in->out)
        for rpi=rp(v):rp(v+1)-1
            w=ci(rpi);
            if v == w:
                continue
            if usew:
                ew = ai(rpi)^(1/3)
            for cpi=cp(w):cp(w+1)-1:
                x = ri(cpi)
                if x==w:
                    continue
                if ind(x):
                    if usew:
                        ew2 = ati(cpi)
                    curccmid = curccmid + ew*ew2^(1/3)*cache(x)

        # count in-link circuits (in->out->out)
        for cpi=cp(v):cp(v+1)-1
            w = ri(cpi)
            if v==w:
                continue
            if usew:
                ew = ati(cpi)^(1/3)
            for rpi2=rp(w):rp(w+1)-1
                x = ci(rpi2)
                if x==w:
                    continue
                if ind(x):
                    if usew:
                        ew2 = ai(rpi2)
                    curccin = curccin + ew*ew2^(1/3)*cache(x)

        # reset and reinit the cache for outlinks
        for cpi=cp(v):cp(v+1)-1,
            w = ri(cpi)
            ind(w) = 0

        for rpi=rp(v):rp(v+1)-1
            w = ci(rpi)
            if usew:
                ew = ai(rpi)
            if vnot = w:
                ind(w) = 1
                cache(w) = ew^(1/3)
        end
        # count out-link circuits (out->out->in)
        for rpi=rp(v):rp(v+1)-1:
            w = ci(rpi)
            if v==w:
                continue
            if usew:
                ew = ai(rpi)^(1/3)
            for rpi2=rp(w):rp(w+1)-1:
                x = ci(rpi2)
                if x==w:
                    continue
                if ind(x):
                    if usew:
                        ew2 = ai(rpi2)
                    curccout = curccout+ew*ew2^(1/3)*cache(x);

        for rpi=rp(v):rp(v+1)-1:
            w = ci(rpi)
            ind(w) = 0
        # store the values
        nf = degs(v)*(degs(v)-1) - 2*bilatedges
        curcc = curcccyc + curccmid + curccin + curccout
        if nf > 0 and donorm:
            curcc = curcc/nf
        cc(v) = curcc
        if nargout > 1:
            cccyc(v) = curcccyc
        if nargout > 2:
            ccmid(v) = curccmid
        if nargout > 3:
            ccin(v) = curccin
        if nargout > 4:
            ccout(v) = curccout
        if nargout > 5:
            nf(v) = nf

    return [cc, cccyc, ccmid, ccin, ccout, nf]
