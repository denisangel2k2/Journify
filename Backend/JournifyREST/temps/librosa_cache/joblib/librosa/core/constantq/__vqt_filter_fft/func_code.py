# first line: 1049
@cache(level=10)
def __vqt_filter_fft(
    sr,
    freqs,
    filter_scale,
    norm,
    sparsity,
    hop_length=None,
    window="hann",
    gamma=0.0,
    dtype=np.complex64,
    alpha=None,
):
    """Generate the frequency domain variable-Q filter basis."""
    basis, lengths = filters.wavelet(
        freqs=freqs,
        sr=sr,
        filter_scale=filter_scale,
        norm=norm,
        pad_fft=True,
        window=window,
        gamma=gamma,
        alpha=alpha,
    )

    # Filters are padded up to the nearest integral power of 2
    n_fft = basis.shape[1]

    if hop_length is not None and n_fft < 2.0 ** (1 + np.ceil(np.log2(hop_length))):
        n_fft = int(2.0 ** (1 + np.ceil(np.log2(hop_length))))

    # re-normalize bases with respect to the FFT window length
    basis *= lengths[:, np.newaxis] / float(n_fft)

    # FFT and retain only the non-negative frequencies
    fft = get_fftlib()
    fft_basis = fft.fft(basis, n=n_fft, axis=1)[:, : (n_fft // 2) + 1]

    # sparsify the basis
    fft_basis = util.sparsify_rows(fft_basis, quantile=sparsity, dtype=dtype)

    return fft_basis, n_fft, lengths
