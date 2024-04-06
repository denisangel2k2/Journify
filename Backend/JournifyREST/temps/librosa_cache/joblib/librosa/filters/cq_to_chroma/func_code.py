# first line: 994
@cache(level=10)
def cq_to_chroma(
    n_input: int,
    *,
    bins_per_octave: int = 12,
    n_chroma: int = 12,
    fmin: Optional[_FloatLike_co] = None,
    window: Optional[np.ndarray] = None,
    base_c: bool = True,
    dtype: DTypeLike = np.float32,
) -> np.ndarray:
    """Construct a linear transformation matrix to map Constant-Q bins
    onto chroma bins (i.e., pitch classes).

    Parameters
    ----------
    n_input : int > 0 [scalar]
        Number of input components (CQT bins)
    bins_per_octave : int > 0 [scalar]
        How many bins per octave in the CQT
    n_chroma : int > 0 [scalar]
        Number of output bins (per octave) in the chroma
    fmin : None or float > 0
        Center frequency of the first constant-Q channel.
        Default: 'C1' ~= 32.7 Hz
    window : None or np.ndarray
        If provided, the cq_to_chroma filter bank will be
        convolved with ``window``.
    base_c : bool
        If True, the first chroma bin will start at 'C'
        If False, the first chroma bin will start at 'A'
    dtype : np.dtype
        The data type of the output basis.
        By default, uses 32-bit (single-precision) floating point.

    Returns
    -------
    cq_to_chroma : np.ndarray [shape=(n_chroma, n_input)]
        Transformation matrix: ``Chroma = np.dot(cq_to_chroma, CQT)``

    Raises
    ------
    ParameterError
        If ``n_input`` is not an integer multiple of ``n_chroma``

    Notes
    -----
    This function caches at level 10.

    Examples
    --------
    Get a CQT, and wrap bins to chroma

    >>> y, sr = librosa.load(librosa.ex('trumpet'))
    >>> CQT = np.abs(librosa.cqt(y, sr=sr))
    >>> chroma_map = librosa.filters.cq_to_chroma(CQT.shape[0])
    >>> chromagram = chroma_map.dot(CQT)
    >>> # Max-normalize each time step
    >>> chromagram = librosa.util.normalize(chromagram, axis=0)

    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots(nrows=3, sharex=True)
    >>> imgcq = librosa.display.specshow(librosa.amplitude_to_db(CQT,
    ...                                                         ref=np.max),
    ...                                  y_axis='cqt_note', x_axis='time',
    ...                                  ax=ax[0])
    >>> ax[0].set(title='CQT Power')
    >>> ax[0].label_outer()
    >>> librosa.display.specshow(chromagram, y_axis='chroma', x_axis='time',
    ...                          ax=ax[1])
    >>> ax[1].set(title='Chroma (wrapped CQT)')
    >>> ax[1].label_outer()
    >>> chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    >>> imgchroma = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[2])
    >>> ax[2].set(title='librosa.feature.chroma_stft')
    """
    # How many fractional bins are we merging?
    n_merge = float(bins_per_octave) / n_chroma

    fmin_: _FloatLike_co
    if fmin is None:
        fmin_ = note_to_hz("C1")
    else:
        fmin_ = fmin

    if np.mod(n_merge, 1) != 0:
        raise ParameterError(
            "Incompatible CQ merge: "
            "input bins must be an "
            "integer multiple of output bins."
        )

    # Tile the identity to merge fractional bins
    cq_to_ch = np.repeat(np.eye(n_chroma), int(n_merge), axis=1)

    # Roll it left to center on the target bin
    cq_to_ch = np.roll(cq_to_ch, -int(n_merge // 2), axis=1)

    # How many octaves are we repeating?
    n_octaves = np.ceil(float(n_input) / bins_per_octave)

    # Repeat and trim
    cq_to_ch = np.tile(cq_to_ch, int(n_octaves))[:, :n_input]

    # What's the note number of the first bin in the CQT?
    # midi uses 12 bins per octave here
    midi_0 = np.mod(hz_to_midi(fmin_), 12)

    if base_c:
        # rotate to C
        roll = midi_0
    else:
        # rotate to A
        roll = midi_0 - 9

    # Adjust the roll in terms of how many chroma we want out
    # We need to be careful with rounding here
    roll = int(np.round(roll * (n_chroma / 12.0)))

    # Apply the roll
    cq_to_ch = np.roll(cq_to_ch, roll, axis=0).astype(dtype)

    if window is not None:
        cq_to_ch = scipy.signal.convolve(cq_to_ch, np.atleast_2d(window), mode="same")

    return cq_to_ch
