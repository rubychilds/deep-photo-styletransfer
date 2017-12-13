import numpy as np


def sparse_to_csr(A, varargin):
  # SPARSE_TO_CSR Convert a sparse matrix into compressed row storage arrays
  #
  # [rp ci ai] = sparse_to_csr(A) returns the row pointer (rp), column index
  # (ci) and value index (ai) arrays of a compressed sparse representation of
  # the matrix A.
  #
  # [rp ci ai] = sparse_to_csr(i,j,v,n) returns a csr representation of the
  # index sets i,j,v with n rows.
  #
  # Example:
  #   A=sparse(6,6); A(1,1)=5; A(1,5)=2; A(2,3)=-1; A(4,1)=1; A(5,6)=1;
  #   [rp ci ai]=sparse_to_csr(A)
  #
  # See also CSR_TO_SPARSE, SPARSE

  # David F. Gleich
  # Copyright, Stanford University, 2008-2009

  # History
  # 2008-04-07: Initial version
  # 2008-04-24: Added triple array input
  # 2009-05-01: Added ncol output
  # 2009-05-15: Fixed triplet input

  error(nargchk(1, 5, nargin, 'struct'))
  retc = nargout > 1
  reta = nargout > 2

  if nargin > 1:
      if nargin > 4:
        ncol = varargin{4}
      nzi = A
      nzj = varargin{1}
      if reta && length(varargin) > 2:
          nzv = varargin{2}
      if nargin < 4:
          n = max(nzi)
      else:
          n = varargin{3}
      nz = length(A)
      if length(nzi) != length(nzj):
           error('gaimc:invalidInput',...
              'length of nzi (#i) not equal to length of nzj (#i)', nz, length(nzj))
      if reta && length(varargin) < 3:
          error('gaimc:invalidInput', 'no value array passed for triplet input, see usage')
      if not isscalar(n):
          error('gaimc:invalidInput',...
              ['the 4th input to sparse_to_csr with triple input was not a scalar'])
      if nargin < 5:
          ncol = max(nzj)
      elif ~isscalar(ncol):
          error('gaimc:invalidInput',...
              ['the 5th input to sparse_to_csr with triple input was not ' ...
               'a scalar'])

  else
      n = size(A,1)
      nz = nnz(A)
      ncol = size(A,2)
      retc = nargout > 1
      reta = nargout > 2
      if reta:
          [nzi, nzj, nzv] = find(A)
      else:
          [nzi, nzj] = find(A)

  if retc:
      ci = np.zeros(nz,1)
  if reta:
      ai = np.zeros(nz,1)
  rp = np.zeros(n+1,1)
  for i=1:nz
      rp(nzi(i)+1)=rp(nzi(i)+1)+1

  rp = cumsum(rp)
  if ~retc && ~reta:
      rp = rp+1
      return
  for i=1:nz
      if reta:
          ai(rp(nzi(i)) + 1) = nzv(i)
      ci(rp(nzi(i)) + 1) = nzj(i)
      rp(nzi(i)) = rp(nzi(i)) + 1

  for i=n:-1:1
      rp(i+1) = rp(i)

  rp(1) = 0
  rp = rp+1

  return [rp, ci, ai, ncol]
