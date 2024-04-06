# first line: 1122
@cache(level=10)
def window_bandwidth(window: _WindowSpec, n: int = 1000) -> float:
    """Get the equivalent noise bandwidth (ENBW) of a window function.

    The ENBW of a window is defined by [#]_ (equation 11) as the normalized
    ratio of the sum of squares to the square of sums::

        enbw = n * sum(window**2) / sum(window)**2

    .. [#] Harris, F. J.
        "On the use of windows for harmonic analysis with the discrete Fourier transform."
        Proceedings of the IEEE, 66(1), 51-83.  1978.

    Parameters
    ----------
    window : callable or string
        A window function, or the name of a window function,
        e.g.: `scipy.signal.hann` or `'boxcar'`
    n : int > 0
        The number of coefficients to use in estimating the
        window bandwidth

    Returns
    -------
    bandwidth : float
        The equivalent noise bandwidth (in FFT bins) of the
        given window function

    Notes
    -----
    This function caches at level 10.

    See Also
    --------
    get_window
    """
    if hasattr(window, "__name__"):
        key = window.__name__
    else:
        key = window

    if key not in WINDOW_BANDWIDTHS:
        win = get_window(window, n)
        WINDOW_BANDWIDTHS[key] = (
            n * np.sum(win**2) / (np.sum(win) ** 2 + util.tiny(win))
        )

    return WINDOW_BANDWIDTHS[key]
