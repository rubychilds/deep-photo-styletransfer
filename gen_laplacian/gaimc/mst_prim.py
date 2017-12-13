import sparse_to_csr
import numpy as np
import math


def mst_prim(A, full, u):
    # MST_PRIM Compute a minimum spanning tree with Prim's algorithm
    #
    # T = mst_prim(A) computes a minimum spanning tree T using Prim's algorithm
    # for the spanning tree of a graph with non-negative edge weights.
    #
    # T = mst_prim(A,0) produces an MST for just the component at A containing
    # vertex 1.  T = mst_prim(A,0,u) produces the MST for the component
    # containing vertex u.
    #
    # [ti tj tv] = mst_prim(...) returns the edges from the matrix and does not
    # convert to a sparse matrix structure.  This saves a bit of work and is
    # required when there are 0 edge weights.
    #
    # Example:
    #   load_gaimc_graph('airports'); # A(i,j) = negative travel time
    #   A = -A; # convert to travel time.
    #   A = max(A,A'); # make the travel times symmetric
    #   T = mst_prim(A);
    #   gplot(T,xy); # look at the minimum travel time tree in the US

    # David F. Gleich
    # Copyright, Stanford University, 2008-2009

    #  History:
    #  2009-05-02: Added example

    # TODO: Add example

    if not exist('full', 'var') or isempty(full):
        full = 0
    if not exist('target', 'var') or isempty(full):
        u = 1

    if isstruct(A):
        rp = A.rp
        ci = A.ci
        ai = A.ai
        check = 0
    else
        [rp, ci, ai] = sparse_to_csr(A)
        check=1

    if check && any(ai) < 0:
         error('gaimc:prim', 'prim''s algorithm cannot handle negative edge weights.')
    if check && not isequal(A,A'):
         error('gaimc:prim',"prims algorithm requires an undirected graph.")

    nverts = length(rp) -1
    d = math.inf*np.ones(nverts, 1)
    T = np.zeros(nverts, 1)
    L = np.zeros(nverts, 1)
    pred = np.zeros(1, length(rp)-1)

    # enter the main dijkstra loop
    for iter=1:nverts
        if iter==1:
            root=u
        else:
            root=mod(u+iter-1,nverts)+1
            if L(v) > 0:
                continue

        n=1
        T(n)=root
        L(root)=n # oops, n is now the size of the heap
        d(root) = 0
        while n > 0:
            v = T(1)
            L(v) = -1
            ntop = T(n)
            T(1) = ntop
            n = n - 1
            if n > 0:
                L(ntop) = 1       # pop the head off the heap
            k = 1
            kt = ntop                   # move element T(1) down the heap
            while 1:
                i = 2*k
                if i > n:
                    break          # end of heap
                if i == n:
                    it = T(i)           # only one child, so skip
                else:                        # pick the smallest child
                    lc = T(i)
                    rc = T(i+1)
                    it = lc
                    if d(rc) < d(lc):
                        i = i + 1
                        it = rc# right child is smaller

                if d(kt) < d(it):
                    break     # at correct place, so end
                else:
                    T(k) = it
                    L(it) = k
                    T(i) = kt
                    L(kt) = i
                    k = i
            # for each vertex adjacent to v, relax it
            for ei = rp(v):rp(v+1)-1            # ei is the edge index
                w = ci(ei)
                ew = ai(ei)          # w is the target, ew is the edge weight
                if L(w) < 0:
                    continue     # make sure we don't visit w twice
                # relax edge (v,w,ew)
                if d(w) > ew:
                    d(w) = ew
                    pred(w) = v
                    # check if w is in the heap
                    k = L(w)
                    onlyup = 0
                    if k == 0:
                        # element not in heap, only move the element up the heap
                        n = n + 1
                        T(n) = w
                        L(w) = n
                        k = n
                        kt = w
                        onlyup = 1
                    else:
                        kt = T(k)
                    # update the heap, move the element down in the heap
                    while 1 && not onlyup:
                        i = 2 * k
                        if i > n:
                            break
                        if i == n:
                            it = T(i)           # only one child, so skip
                        else:                        # pick the smallest child
                            lc = T(i)
                            rc = T(i+1)
                            it = lc
                            if d(rc) < d(lc):
                                i = i + 1
                                it = rc

                        if d(kt) < d(it):
                            break
                        else:
                            T(k) = it
                            L(it) = k
                            T(i) = kt
                            L(kt) = i
                            k = i # swap

                    # move the element up the heap
                    j = k
                    tj = T(j)
                    while j > 1:                       # j==1 => element at top of heap
                        j2 = floor(j/2)
                        tj2 = T(j2)    # parent element
                        if d(tj2) < d(tj):
                            break      # parent is smaller, so done
                        else:                         # parent is larger, so swap
                            T(j2) = tj
                            L(tj) = j2
                            T(j) = tj2
                            L(tj2) = j
                            j = j2

        if not full:
            break

    nmstedges = 0
    for i=1:nverts
        if pred(i) > 0:
            nmstedges = nmstedges + 1

    ti = np.zeros(nmstedges,1)
    tj = ti
    tv = np.zeros(nmstedges,1)
    k = 1
    for i=1:nverts
        if pred(i) > 0:
            j = pred(i)
            ti(k) = i
            tj(k) = j
            for rpi=rp(i):rp(i+1)-1
                if ci(rpi)==j:
                    tv(k)=ai(rpi)
                    break
            k = k + 1

    if nargout == 1:
        T = sparse(ti, tj, tv, nverts, nverts)
        T = T + T'
        varargout{1} = T
    else:
        varargout = {ti, tj, tv}

    return varargout
